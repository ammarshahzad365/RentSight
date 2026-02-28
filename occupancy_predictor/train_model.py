import os
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

# ==============================================================================
# CONFIG
# ==============================================================================
SANITIZED_DIR = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')
MODEL_DIR = os.path.dirname(__file__)
RANDOM_STATE = 42
TEST_SIZE = 0.2

# ==============================================================================
# AMENITY DEFINITIONS
# ==============================================================================

# Top amenities used as individual binary features (appearing in 100+ listings)
TOP_AMENITIES = [
    'Wifi', 'Kitchen', 'Free parking on premises', 'TV', 'Air conditioning',
    'Fire extinguisher', 'Dedicated workspace', 'First aid kit', 'Washer',
    'Smoke alarm', 'Exterior security cameras on property', 'Iron',
    'Smoking allowed', 'Hot water', 'Self check-in', 'Hangers',
    'Cooking basics', 'Essentials', 'Dishes and silverware', 'Microwave',
    'Heating', 'Bed linens', 'Extra pillows and blankets',
    'Carbon monoxide alarm', 'Shampoo', 'Cleaning products', 'Refrigerator',
    'Pets allowed', 'Ceiling fan', 'Long term stays allowed', 'Body soap',
    'Freezer', 'Room-darkening shades', 'Private entrance', 'Hot water kettle',
    'Free street parking', 'Outdoor dining area', 'Elevator', 'Hair dryer',
    'Mini fridge', 'Building staff', 'Lock on bedroom door',
    'Shower gel', 'Dining table', 'Luggage dropoff allowed',
    'Cleaning available during stay', 'Conditioner', 'Stove',
    'Drying rack for clothing', 'BBQ grill', 'Oven', 'Bathtub',
    'Safe', 'Host greets you', 'Bidet', 'Ethernet connection', 'Coffee',
    'Dishwasher', 'Hot tub', 'Exercise equipment', 'Breakfast',
    'Indoor fireplace', 'Fire pit', 'Dryer', 'Blender', 'Pool',
]

# Amenity categories for aggregate features
AMENITY_CATEGORIES = {
    'safety': [
        'Fire extinguisher', 'First aid kit', 'Smoke alarm',
        'Carbon monoxide alarm', 'Exterior security cameras on property',
        'Lock on bedroom door', 'Safe', 'Window guards', 'Baby safety gates',
        'Fireplace guards', 'Table corner guards', 'Outlet covers',
    ],
    'kitchen': [
        'Kitchen', 'Cooking basics', 'Dishes and silverware', 'Microwave',
        'Refrigerator', 'Freezer', 'Hot water kettle', 'Stove', 'Oven',
        'Blender', 'Mini fridge', 'Coffee', 'Coffee maker', 'Toaster',
        'Dishwasher', 'Bread maker', 'Rice maker', 'Wine glasses',
        'Gas stove', 'Electric stove', 'Kitchenette',
    ],
    'comfort': [
        'Air conditioning', 'Heating', 'Bed linens', 'Extra pillows and blankets',
        'Room-darkening shades', 'Hair dryer', 'Iron', 'Hangers',
        'Essentials', 'Shampoo', 'Body soap', 'Conditioner', 'Shower gel',
        'Cleaning products', 'Hot water', 'Ceiling fan', 'Bathtub', 'Bidet',
        'Drying rack for clothing', 'Clothing storage',
    ],
    'entertainment': [
        'TV', 'Wifi', 'Ethernet connection', 'Pool', 'Hot tub',
        'Exercise equipment', 'BBQ grill', 'Fire pit', 'Indoor fireplace',
        'Books and reading material', 'Board games', 'Sound system',
        'Pool table', 'Ping pong table', 'Arcade games', 'Piano',
        'Movie theater', 'Game console', 'Life size games',
    ],
    'convenience': [
        'Free parking on premises', 'Free street parking', 'Dedicated workspace',
        'Washer', 'Dryer', 'Self check-in', 'Elevator', 'Private entrance',
        'Luggage dropoff allowed', 'Cleaning available during stay',
        'Long term stays allowed', 'Host greets you', 'Building staff',
        'Breakfast', 'Outdoor dining area', 'Dining table', 'Lockbox',
        'Smart lock', 'Keypad',
    ],
    'outdoor': [
        'Outdoor dining area', 'BBQ grill', 'Fire pit', 'Backyard',
        'Private patio or balcony', 'Patio or balcony', 'Outdoor furniture',
        'Outdoor shower', 'Garden view', 'Mountain view', 'City skyline view',
        'Pool', 'Hot tub', 'Lake access', 'Waterfront',
    ],
    'family': [
        'High chair', 'Crib', 'Baby safety gates', 'Baby bath',
        "Children's dinnerware", "Children's books and toys",
        "Children's playroom", 'Changing table', 'Window guards',
        'Outlet covers', 'Table corner guards', 'Fireplace guards',
        'Baby monitor', 'Mosquito net', 'Outdoor playground',
    ],
}

# ==============================================================================
# DATA LOADING
# ==============================================================================

def load_listings():
    """Load all sanitized listings into a pandas DataFrame."""
    records = []
    for filename in os.listdir(SANITIZED_DIR):
        if not filename.endswith('.json'):
            continue
        try:
            with open(os.path.join(SANITIZED_DIR, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)

            location = data.get('location') or {}
            amenities = set(data.get('amenities') or [])

            record = {
                'price':        data.get('price'),
                'max_guests':   data.get('max_guests'),
                'bedrooms':     data.get('bedrooms'),
                'beds':         data.get('beds'),
                'baths':        data.get('baths'),
                'listing_type': data.get('listing_type', 'Unknown'),
                'room_type':    data.get('room_type', 'Unknown'),
                'lat':          location.get('lat'),
                'lng':          location.get('lng'),
                'occ_rate':     data.get('occ_rate'),
                'amenity_count': len(amenities),
            }

            # Binary flags for top amenities
            for am in TOP_AMENITIES:
                record[f'am_{am}'] = int(am in amenities)

            # Category counts
            for cat, keywords in AMENITY_CATEGORIES.items():
                record[f'cat_{cat}'] = sum(1 for k in keywords if k in amenities)

            records.append(record)
        except Exception as e:
            print(f"  Skipping {filename}: {e}")

    df = pd.DataFrame(records)
    print(f"Loaded {len(df)} listings")
    return df

# ==============================================================================
# FEATURE ENGINEERING
# ==============================================================================

def compute_neighborhood_stats(df):
    """
    For each listing, compute stats of nearby listings within ~1km radius.
    Captures neighborhood-level market signals.
    """
    from scipy.spatial import cKDTree

    coords = df[['lat', 'lng']].values
    tree = cKDTree(coords)
    radius = 0.01  # ~1km at this latitude

    neighbor_counts = []
    neighbor_avg_prices = []
    neighbor_avg_capacity = []
    neighbor_price_rank = []
    neighbor_avg_amenities = []

    for i in range(len(df)):
        indices = tree.query_ball_point(coords[i], radius)
        indices = [j for j in indices if j != i]

        neighbor_counts.append(len(indices))

        if indices:
            n_prices = df['price'].iloc[indices].values
            neighbor_avg_prices.append(np.nanmean(n_prices))
            neighbor_avg_capacity.append(np.nanmean(df['total_capacity_raw'].iloc[indices].values))
            own_price = df['price'].iloc[i]
            rank = np.nanmean(n_prices <= own_price)
            neighbor_price_rank.append(rank)
            neighbor_avg_amenities.append(np.nanmean(df['amenity_count'].iloc[indices].values))
        else:
            neighbor_avg_prices.append(df['price'].iloc[i])
            neighbor_avg_capacity.append(df['total_capacity_raw'].iloc[i])
            neighbor_price_rank.append(0.5)
            neighbor_avg_amenities.append(df['amenity_count'].iloc[i])

    df['neighbor_count'] = neighbor_counts
    df['neighbor_avg_price'] = neighbor_avg_prices
    df['neighbor_avg_capacity'] = neighbor_avg_capacity
    df['neighbor_price_rank'] = neighbor_price_rank
    df['neighbor_avg_amenities'] = neighbor_avg_amenities
    df['price_vs_neighborhood'] = df['price'] / df['neighbor_avg_price'].clip(lower=1)
    df['amenities_vs_neighborhood'] = df['amenity_count'] / df['neighbor_avg_amenities'].clip(lower=1)

    return df


def engineer_features(df):
    """
    Create features from raw listing data.

    Groups:
      1. Ratio features    — value metrics per guest/bedroom
      2. Size features     — total capacity, size category
      3. Price features    — log price, price bins
      4. Location features — distance from center, lat/lng interactions
      5. Neighborhood      — competitor density, local comparisons
      6. Categorical       — label-encoded types + flags
      7. Amenity features  — binary flags, counts, category scores, derived ratios
    """
    bedrooms = df['bedrooms'].clip(lower=1)
    max_guests = df['max_guests'].clip(lower=1)

    # --- 1. Ratio features ---
    df['price_per_guest'] = df['price'] / max_guests
    df['price_per_bedroom'] = df['price'] / bedrooms
    df['price_per_bed'] = df['price'] / df['beds'].clip(lower=1)
    df['guests_per_bedroom'] = df['max_guests'] / bedrooms
    df['beds_per_bedroom'] = df['beds'] / bedrooms
    df['baths_per_bedroom'] = df['baths'] / bedrooms
    df['beds_to_guests'] = df['beds'] / max_guests

    # --- 2. Size features ---
    df['total_capacity_raw'] = df['bedrooms'] + df['beds'] + df['baths']
    df['total_capacity'] = df['total_capacity_raw']
    df['size_score'] = df['bedrooms'] * 2 + df['beds'] + df['baths'] * 1.5
    df['is_sweet_spot'] = ((df['bedrooms'].between(2, 3)) & (df['max_guests'].between(4, 6))).astype(int)

    # --- 3. Price features ---
    df['log_price'] = np.log1p(df['price'])
    df['price_squared'] = df['price'] ** 2
    price_median = df['price'].median()
    price_q25 = df['price'].quantile(0.25)
    price_q75 = df['price'].quantile(0.75)
    df['price_tier'] = pd.cut(
        df['price'],
        bins=[0, price_q25, price_median, price_q75, float('inf')],
        labels=[0, 1, 2, 3]
    ).astype(float)

    # --- 4. Location features ---
    center_lat = df['lat'].median()
    center_lng = df['lng'].median()
    df['dist_from_center'] = np.sqrt((df['lat'] - center_lat)**2 + (df['lng'] - center_lng)**2)
    df['lat_lng_interaction'] = df['lat'] * df['lng']

    # --- 5. Neighborhood features ---
    df = compute_neighborhood_stats(df)

    # --- 6. Categorical encoding ---
    le_listing = LabelEncoder()
    le_room = LabelEncoder()
    df['listing_type_enc'] = le_listing.fit_transform(df['listing_type'].fillna('Unknown'))
    df['room_type_enc'] = le_room.fit_transform(df['room_type'].fillna('Unknown'))
    df['is_entire'] = df['listing_type'].str.lower().str.contains('entire', na=False).astype(int)
    df['is_room'] = df['listing_type'].str.lower().str.contains('room', na=False).astype(int)

    # --- 7. Amenity-derived features ---
    df['amenity_richness'] = df['amenity_count'] / df['amenity_count'].max()
    df['amenity_per_guest'] = df['amenity_count'] / max_guests
    df['amenity_per_bedroom'] = df['amenity_count'] / bedrooms
    df['amenity_per_price'] = df['amenity_count'] / df['price'].clip(lower=1)

    # Store stats for prediction-time use
    df.attrs['price_q25'] = price_q25
    df.attrs['price_median'] = price_median
    df.attrs['price_q75'] = price_q75
    df.attrs['center_lat'] = center_lat
    df.attrs['center_lng'] = center_lng
    df.attrs['max_amenity_count'] = int(df['amenity_count'].max())

    return df, le_listing, le_room

# ==============================================================================
# FEATURE COLUMNS
# ==============================================================================

BASE_FEATURES = [
    # Raw
    'price', 'max_guests', 'bedrooms', 'beds', 'baths', 'lat', 'lng',
    # Categorical
    'listing_type_enc', 'room_type_enc', 'is_entire', 'is_room',
    # Ratios
    'price_per_guest', 'price_per_bedroom', 'price_per_bed',
    'guests_per_bedroom', 'beds_per_bedroom', 'baths_per_bedroom', 'beds_to_guests',
    # Size
    'total_capacity', 'size_score', 'is_sweet_spot',
    # Price derived
    'log_price', 'price_squared', 'price_tier',
    # Location derived
    'dist_from_center', 'lat_lng_interaction',
    # Neighborhood
    'neighbor_count', 'neighbor_avg_price', 'neighbor_avg_capacity',
    'neighbor_price_rank', 'price_vs_neighborhood',
    'neighbor_avg_amenities', 'amenities_vs_neighborhood',
    # Amenity aggregate
    'amenity_count', 'amenity_richness', 'amenity_per_guest',
    'amenity_per_bedroom', 'amenity_per_price',
]

AMENITY_FEATURE_COLS = [f'am_{am}' for am in TOP_AMENITIES]
CATEGORY_FEATURE_COLS = [f'cat_{cat}' for cat in AMENITY_CATEGORIES]
FEATURE_COLS = BASE_FEATURES + AMENITY_FEATURE_COLS + CATEGORY_FEATURE_COLS
TARGET_COL = 'occ_rate'

# ==============================================================================
# MODEL TRAINING
# ==============================================================================

def train_model(df):
    """Train an XGBoost regressor with cross-validated early stopping."""

    df = df.dropna(subset=[TARGET_COL]).copy()
    df[FEATURE_COLS] = df[FEATURE_COLS].fillna(df[FEATURE_COLS].median())

    print(f"Training on {len(df)} listings with {len(FEATURE_COLS)} features")
    print(f"  - Base features:    {len(BASE_FEATURES)}")
    print(f"  - Amenity flags:    {len(AMENITY_FEATURE_COLS)}")
    print(f"  - Category scores:  {len(CATEGORY_FEATURE_COLS)}")

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    y_bins = pd.cut(y, bins=5, labels=False)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_bins
    )

    print(f"Split: {len(X_train)} train / {len(X_test)} test")
    print("\nRunning 5-fold cross-validation...")

    base_params = dict(
        max_depth=7,
        learning_rate=0.03,
        subsample=0.75,
        colsample_bytree=0.55,   # lower — forces selection among many amenity features
        colsample_bylevel=0.55,
        min_child_weight=5,
        reg_alpha=1.0,
        reg_lambda=3.0,
        gamma=0.2,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbosity=0,
    )

    # Find best n_estimators via early stopping
    cv_model = XGBRegressor(n_estimators=2000, early_stopping_rounds=50, **base_params)
    cv_model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
    best_n = cv_model.best_iteration + 1
    print(f"  Best n_estimators: {best_n}")

    # Train final model
    model = XGBRegressor(n_estimators=best_n, **base_params)
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    # Cross-validation score
    kf = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(
        XGBRegressor(n_estimators=best_n, **base_params),
        X, y, cv=kf, scoring='r2', n_jobs=-1
    )
    print(f"  5-Fold CV R²: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")

    return model, X_train, X_test, y_train, y_test


def evaluate_model(model, X_train, X_test, y_train, y_test):
    """Evaluate model performance and print metrics."""

    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    print("\n" + "=" * 60)
    print("MODEL PERFORMANCE")
    print("=" * 60)

    print(f"\n{'Metric':<25} {'Train':>10} {'Test':>10}")
    print("-" * 47)
    print(f"{'MAE (%)' :<25} {mean_absolute_error(y_train, y_pred_train):>10.2f} {mean_absolute_error(y_test, y_pred_test):>10.2f}")
    print(f"{'RMSE (%)':<25} {np.sqrt(mean_squared_error(y_train, y_pred_train)):>10.2f} {np.sqrt(mean_squared_error(y_test, y_pred_test)):>10.2f}")
    print(f"{'R² Score':<25} {r2_score(y_train, y_pred_train):>10.4f} {r2_score(y_test, y_pred_test):>10.4f}")

    errors = np.abs(y_test.values - y_pred_test)
    print(f"\nTest Set Error Distribution:")
    print(f"  Within  5%: {(errors <= 5).sum():>5d} / {len(errors)} ({(errors <= 5).mean()*100:.1f}%)")
    print(f"  Within 10%: {(errors <= 10).sum():>5d} / {len(errors)} ({(errors <= 10).mean()*100:.1f}%)")
    print(f"  Within 15%: {(errors <= 15).sum():>5d} / {len(errors)} ({(errors <= 15).mean()*100:.1f}%)")
    print(f"  Within 20%: {(errors <= 20).sum():>5d} / {len(errors)} ({(errors <= 20).mean()*100:.1f}%)")

    # Feature importance — top 25
    importance = model.feature_importances_
    feat_imp = sorted(zip(FEATURE_COLS, importance), key=lambda x: x[1], reverse=True)
    print(f"\nTop 25 Feature Importance:")
    for name, imp in feat_imp[:25]:
        bar = '█' * int(imp * 50)
        print(f"  {name:<30s} {imp:.4f}  {bar}")

    # Show amenity-related features specifically
    am_features = [(n, i) for n, i in feat_imp if n.startswith('am_') or n.startswith('cat_') or 'amenity' in n]
    print(f"\nAmenity-Related Feature Importance (top 15):")
    for name, imp in am_features[:15]:
        bar = '█' * int(imp * 100)
        print(f"  {name:<30s} {imp:.4f}  {bar}")


def save_artifacts(model, le_listing, le_room, df):
    """Save model, encoders, and market stats to disk."""
    model_path = os.path.join(MODEL_DIR, 'xgb_occupancy_model.pkl')
    encoders_path = os.path.join(MODEL_DIR, 'label_encoders.pkl')

    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    with open(encoders_path, 'wb') as f:
        pickle.dump({
            'listing_type': le_listing,
            'room_type': le_room,
            'feature_cols': FEATURE_COLS,
            'top_amenities': TOP_AMENITIES,
            'amenity_categories': AMENITY_CATEGORIES,
            'market_stats': {
                'price_q25': float(df.attrs.get('price_q25', df['price'].quantile(0.25))),
                'price_median': float(df.attrs.get('price_median', df['price'].median())),
                'price_q75': float(df.attrs.get('price_q75', df['price'].quantile(0.75))),
                'center_lat': float(df.attrs.get('center_lat', df['lat'].median())),
                'center_lng': float(df.attrs.get('center_lng', df['lng'].median())),
                'max_amenity_count': int(df.attrs.get('max_amenity_count', df['amenity_count'].max())),
            }
        }, f)

    print(f"\nModel saved to: {model_path}")
    print(f"Encoders saved to: {encoders_path}")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 60)
    print("OCCUPANCY RATE PREDICTOR — Training Pipeline (v2 + Amenities)")
    print("=" * 60)

    print("\n[1/4] Loading listings...")
    df = load_listings()

    print("\n[2/4] Engineering features...")
    df, le_listing, le_room = engineer_features(df)
    print(f"  Total features: {len(FEATURE_COLS)}")
    print(f"  Samples:        {len(df)}")

    print("\n[3/4] Training XGBoost model...")
    model, X_train, X_test, y_train, y_test = train_model(df)

    print("\n[4/4] Evaluating...")
    evaluate_model(model, X_train, X_test, y_train, y_test)

    save_artifacts(model, le_listing, le_room, df)

    print("\n" + "=" * 60)
    print("Training complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
