"""
RentSight Price Predictor — Model Training Pipeline
=====================================================
Trains an XGBoost model to predict the *market price* of a listing based on its
features (room type, capacity, location, amenities).  A second optimisation pass
uses the companion occupancy-predictor model to find the revenue-maximising
price for any new listing.

Usage:
    python train_model.py
"""

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
# AMENITY DEFINITIONS (shared with occupancy predictor)
# ==============================================================================

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
    For each listing compute stats of nearby listings within ~1 km.
    These are purely structural — no price leakage because we compute
    neighbourhood *feature* averages, not price directly.
    """
    from scipy.spatial import cKDTree

    coords = df[['lat', 'lng']].values
    tree = cKDTree(coords)
    radius = 0.01  # ~1 km

    neighbor_counts = []
    neighbor_avg_capacity = []
    neighbor_avg_amenities = []

    for i in range(len(df)):
        indices = tree.query_ball_point(coords[i], radius)
        indices = [j for j in indices if j != i]

        neighbor_counts.append(len(indices))

        if indices:
            neighbor_avg_capacity.append(np.nanmean(df['total_capacity'].iloc[indices].values))
            neighbor_avg_amenities.append(np.nanmean(df['amenity_count'].iloc[indices].values))
        else:
            neighbor_avg_capacity.append(df['total_capacity'].iloc[i])
            neighbor_avg_amenities.append(df['amenity_count'].iloc[i])

    df['neighbor_count'] = neighbor_counts
    df['neighbor_avg_capacity'] = neighbor_avg_capacity
    df['neighbor_avg_amenities'] = neighbor_avg_amenities
    df['amenities_vs_neighborhood'] = df['amenity_count'] / df['neighbor_avg_amenities'].clip(lower=1)

    return df


def engineer_features(df):
    """
    Create features from raw listing data.
    IMPORTANT: These features must NOT use price (the target) or occ_rate.
    """
    bedrooms = df['bedrooms'].clip(lower=1)
    max_guests = df['max_guests'].clip(lower=1)

    # --- Size / capacity features ---
    df['total_capacity'] = df['bedrooms'] + df['beds'] + df['baths']
    df['size_score'] = df['bedrooms'] * 2 + df['beds'] + df['baths'] * 1.5
    df['guests_per_bedroom'] = df['max_guests'] / bedrooms
    df['beds_per_bedroom'] = df['beds'] / bedrooms
    df['baths_per_bedroom'] = df['baths'] / bedrooms
    df['beds_to_guests'] = df['beds'] / max_guests
    df['is_sweet_spot'] = (
        (df['bedrooms'].between(2, 3)) & (df['max_guests'].between(4, 6))
    ).astype(int)

    # --- Location features ---
    center_lat = df['lat'].median()
    center_lng = df['lng'].median()
    df['dist_from_center'] = np.sqrt(
        (df['lat'] - center_lat) ** 2 + (df['lng'] - center_lng) ** 2
    )
    df['lat_lng_interaction'] = df['lat'] * df['lng']

    # --- Neighborhood features ---
    df = compute_neighborhood_stats(df)

    # --- Categorical encoding ---
    le_listing = LabelEncoder()
    le_room = LabelEncoder()
    df['listing_type_enc'] = le_listing.fit_transform(df['listing_type'].fillna('Unknown'))
    df['room_type_enc'] = le_room.fit_transform(df['room_type'].fillna('Unknown'))
    df['is_entire'] = df['listing_type'].str.lower().str.contains('entire', na=False).astype(int)
    df['is_room'] = df['listing_type'].str.lower().str.contains('room', na=False).astype(int)

    # --- Amenity-derived features ---
    df['amenity_richness'] = df['amenity_count'] / df['amenity_count'].max()
    df['amenity_per_guest'] = df['amenity_count'] / max_guests
    df['amenity_per_bedroom'] = df['amenity_count'] / bedrooms

    # --- Store stats ---
    df.attrs['center_lat'] = center_lat
    df.attrs['center_lng'] = center_lng
    df.attrs['max_amenity_count'] = int(df['amenity_count'].max())

    return df, le_listing, le_room


# ==============================================================================
# FEATURE COLUMNS  (no price, no occ_rate — these are prediction targets)
# ==============================================================================

BASE_FEATURES = [
    # Raw capacity
    'max_guests', 'bedrooms', 'beds', 'baths', 'lat', 'lng',
    # Categorical
    'listing_type_enc', 'room_type_enc', 'is_entire', 'is_room',
    # Size / capacity ratios
    'total_capacity', 'size_score', 'guests_per_bedroom',
    'beds_per_bedroom', 'baths_per_bedroom', 'beds_to_guests', 'is_sweet_spot',
    # Location derived
    'dist_from_center', 'lat_lng_interaction',
    # Neighborhood
    'neighbor_count', 'neighbor_avg_capacity',
    'neighbor_avg_amenities', 'amenities_vs_neighborhood',
    # Amenity aggregate
    'amenity_count', 'amenity_richness', 'amenity_per_guest', 'amenity_per_bedroom',
]

AMENITY_FEATURE_COLS = [f'am_{am}' for am in TOP_AMENITIES]
CATEGORY_FEATURE_COLS = [f'cat_{cat}' for cat in AMENITY_CATEGORIES]
FEATURE_COLS = BASE_FEATURES + AMENITY_FEATURE_COLS + CATEGORY_FEATURE_COLS
TARGET_COL = 'price'


# ==============================================================================
# MODEL TRAINING
# ==============================================================================

def train_model(df):
    """Train XGBoost regressor on log-price with cross-validated early stopping."""

    df = df.dropna(subset=[TARGET_COL]).copy()

    # Remove extreme outliers (bottom 0.5% and top 0.5%)
    low = df[TARGET_COL].quantile(0.005)
    high = df[TARGET_COL].quantile(0.995)
    df = df[(df[TARGET_COL] >= low) & (df[TARGET_COL] <= high)].copy()
    print(f"After outlier removal: {len(df)} listings (price {low:.1f} – {high:.1f})")

    df[FEATURE_COLS] = df[FEATURE_COLS].fillna(df[FEATURE_COLS].median())

    X = df[FEATURE_COLS]
    y = np.log1p(df[TARGET_COL])  # Train on log(price) for better distribution

    print(f"Training on {len(df)} listings with {len(FEATURE_COLS)} features")
    print(f"  - Base features:    {len(BASE_FEATURES)}")
    print(f"  - Amenity flags:    {len(AMENITY_FEATURE_COLS)}")
    print(f"  - Category scores:  {len(CATEGORY_FEATURE_COLS)}")

    # Stratified split on price bins
    price_bins = pd.cut(y, bins=5, labels=False)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=price_bins
    )
    print(f"Split: {len(X_train)} train / {len(X_test)} test")

    base_params = dict(
        max_depth=7,
        learning_rate=0.03,
        subsample=0.8,
        colsample_bytree=0.6,
        colsample_bylevel=0.6,
        min_child_weight=5,
        reg_alpha=1.0,
        reg_lambda=3.0,
        gamma=0.2,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbosity=0,
    )

    # Early stopping to find best iteration
    print("\nFinding optimal n_estimators with early stopping...")
    cv_model = XGBRegressor(n_estimators=3000, early_stopping_rounds=50, **base_params)
    cv_model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
    best_n = cv_model.best_iteration + 1
    print(f"  Best n_estimators: {best_n}")

    # Final model
    model = XGBRegressor(n_estimators=best_n, **base_params)
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    # Cross-validation
    print("Running 5-fold cross-validation...")
    kf = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(
        XGBRegressor(n_estimators=best_n, **base_params),
        X, y, cv=kf, scoring='r2', n_jobs=-1
    )
    print(f"  5-Fold CV R² (log-price): {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")

    return model, X_train, X_test, y_train, y_test


def evaluate_model(model, X_train, X_test, y_train, y_test):
    """Evaluate model and print metrics in both log-space and dollar-space."""

    y_pred_train_log = model.predict(X_train)
    y_pred_test_log = model.predict(X_test)

    # Convert back to dollar values
    y_train_usd = np.expm1(y_train)
    y_test_usd = np.expm1(y_test)
    y_pred_train_usd = np.expm1(y_pred_train_log)
    y_pred_test_usd = np.expm1(y_pred_test_log)

    print("\n" + "=" * 60)
    print("MODEL PERFORMANCE (Dollar Space)")
    print("=" * 60)

    train_mae = mean_absolute_error(y_train_usd, y_pred_train_usd)
    test_mae = mean_absolute_error(y_test_usd, y_pred_test_usd)
    train_rmse = np.sqrt(mean_squared_error(y_train_usd, y_pred_train_usd))
    test_rmse = np.sqrt(mean_squared_error(y_test_usd, y_pred_test_usd))
    train_r2 = r2_score(y_train_usd, y_pred_train_usd)
    test_r2 = r2_score(y_test_usd, y_pred_test_usd)

    print(f"\n{'Metric':<25} {'Train':>10} {'Test':>10}")
    print("-" * 47)
    print(f"{'MAE ($)':<25} {train_mae:>10.2f} {test_mae:>10.2f}")
    print(f"{'RMSE ($)':<25} {train_rmse:>10.2f} {test_rmse:>10.2f}")
    print(f"{'R² Score':<25} {train_r2:>10.4f} {test_r2:>10.4f}")

    # Percentage error distribution
    pct_errors = np.abs(y_test_usd.values - y_pred_test_usd) / y_test_usd.values * 100
    print(f"\nTest Set % Error Distribution:")
    for thresh in [10, 20, 30, 50]:
        within = (pct_errors <= thresh).sum()
        print(f"  Within {thresh:>2d}%: {within:>5d} / {len(pct_errors)} ({within / len(pct_errors) * 100:.1f}%)")

    # MAPE
    mape = np.mean(pct_errors)
    print(f"\n  MAPE: {mape:.1f}%")

    # Feature importance — top 25
    importance = model.feature_importances_
    feat_imp = sorted(zip(FEATURE_COLS, importance), key=lambda x: x[1], reverse=True)
    print(f"\nTop 25 Feature Importance:")
    for name, imp in feat_imp[:25]:
        bar = '█' * int(imp * 50)
        print(f"  {name:<30s} {imp:.4f}  {bar}")


def build_market_data(df):
    """
    Build a market data snapshot used at prediction time for neighbourhood
    comparisons and revenue optimisation.
    """
    return {
        'coords': df[['lat', 'lng']].values.astype(np.float32),
        'prices': df['price'].values.astype(np.float32),
        'capacities': df['total_capacity'].values.astype(np.float32),
        'amenity_counts': df['amenity_count'].values.astype(np.float32),
        'occ_rates': df['occ_rate'].values.astype(np.float32),
    }


def save_artifacts(model, le_listing, le_room, df):
    """Save model, encoders, and market stats to disk."""
    model_path = os.path.join(MODEL_DIR, 'xgb_price_model.pkl')
    encoders_path = os.path.join(MODEL_DIR, 'price_model_meta.pkl')

    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    meta = {
        'listing_type': le_listing,
        'room_type': le_room,
        'feature_cols': FEATURE_COLS,
        'top_amenities': TOP_AMENITIES,
        'amenity_categories': AMENITY_CATEGORIES,
        'market_stats': {
            'center_lat': float(df.attrs.get('center_lat', df['lat'].median())),
            'center_lng': float(df.attrs.get('center_lng', df['lng'].median())),
            'max_amenity_count': int(df.attrs.get('max_amenity_count', df['amenity_count'].max())),
            'price_median': float(df['price'].median()),
            'price_mean': float(df['price'].mean()),
            'price_q25': float(df['price'].quantile(0.25)),
            'price_q75': float(df['price'].quantile(0.75)),
        },
        'market_data': build_market_data(df),
    }

    with open(encoders_path, 'wb') as f:
        pickle.dump(meta, f)

    print(f"\nModel saved to: {model_path}")
    print(f"Meta saved to:  {encoders_path}")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 60)
    print("RENTSIGHT — Optimal Price Predictor Training Pipeline")
    print("=" * 60)

    print("\n[1/4] Loading listings...")
    df = load_listings()

    print("\n[2/4] Engineering features...")
    df, le_listing, le_room = engineer_features(df)
    print(f"  Total features: {len(FEATURE_COLS)}")
    print(f"  Samples:        {len(df)}")

    print("\n[3/4] Training XGBoost model (target = log price)...")
    model, X_train, X_test, y_train, y_test = train_model(df)

    print("\n[4/4] Evaluating...")
    evaluate_model(model, X_train, X_test, y_train, y_test)

    save_artifacts(model, le_listing, le_room, df)

    print("\n" + "=" * 60)
    print("Training complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
