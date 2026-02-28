"""
RentSight Price Predictor — Prediction Module
===============================================
Provides three pricing strategies:

1. **Market Price**  — What similar listings charge (XGBoost regression).
2. **Revenue-Optimised Price** — Price that maximises  price × occupancy
   using the companion occupancy-predictor model.
3. **Price Range** — Recommended low / high bracket based on neighborhood
   comparable analysis.

Usage:
    from predict import load_models, predict_optimal_price
    models = load_models()
    result = predict_optimal_price(listing_dict, models)
"""

import os
import sys
import pickle
import numpy as np
import pandas as pd

# ==============================================================================
# PATHS
# ==============================================================================
PRICE_MODEL_DIR = os.path.dirname(__file__)
OCCUPANCY_MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'occupancy_predictor')


# ==============================================================================
# MODEL LOADING
# ==============================================================================

def load_models():
    """
    Load:
      - Price prediction model + meta
      - Occupancy prediction model + meta  (optional — for revenue optimisation)
    """
    # --- Price model ---
    price_model_path = os.path.join(PRICE_MODEL_DIR, 'xgb_price_model.pkl')
    price_meta_path = os.path.join(PRICE_MODEL_DIR, 'price_model_meta.pkl')

    with open(price_model_path, 'rb') as f:
        price_model = pickle.load(f)
    with open(price_meta_path, 'rb') as f:
        price_meta = pickle.load(f)

    # --- Occupancy model (optional) ---
    occ_model = None
    occ_encoders = None
    occ_model_path = os.path.join(OCCUPANCY_MODEL_DIR, 'xgb_occupancy_model.pkl')
    occ_enc_path = os.path.join(OCCUPANCY_MODEL_DIR, 'label_encoders.pkl')

    if os.path.exists(occ_model_path) and os.path.exists(occ_enc_path):
        with open(occ_model_path, 'rb') as f:
            occ_model = pickle.load(f)
        with open(occ_enc_path, 'rb') as f:
            occ_encoders = pickle.load(f)

    return {
        'price_model': price_model,
        'price_meta': price_meta,
        'occ_model': occ_model,
        'occ_encoders': occ_encoders,
    }


# ==============================================================================
# FEATURE BUILDING  (mirrors train_model.py — NO price features)
# ==============================================================================

def _build_price_features(listing: dict, meta: dict) -> pd.DataFrame:
    """Build the feature vector expected by the price model."""
    le_listing = meta['listing_type']
    le_room = meta['room_type']
    feature_cols = meta['feature_cols']
    top_amenities = meta['top_amenities']
    amenity_categories = meta['amenity_categories']
    market_stats = meta['market_stats']
    market = meta['market_data']

    location = listing.get('location') or {}
    amenities = set(listing.get('amenities') or [])

    # --- Categoricals ---
    lt = listing.get('listing_type', 'Unknown')
    try:
        lt_enc = le_listing.transform([lt])[0]
    except ValueError:
        lt_enc = 0

    rt = listing.get('room_type', 'Unknown')
    try:
        rt_enc = le_room.transform([rt])[0]
    except ValueError:
        rt_enc = 0

    # --- Raw values ---
    max_guests = max(listing.get('max_guests', 1) or 1, 1)
    bedrooms = max(listing.get('bedrooms', 1) or 1, 1)
    beds = max(listing.get('beds', 1) or 1, 1)
    baths = max(listing.get('baths', 1) or 1, 1)
    lat = location.get('lat', market_stats['center_lat'])
    lng = location.get('lng', market_stats['center_lng'])

    total_cap = bedrooms + beds + baths
    amenity_count = len(amenities)

    # --- Neighborhood (structural features only) ---
    dists = np.sqrt(
        (market['coords'][:, 0] - lat) ** 2 + (market['coords'][:, 1] - lng) ** 2
    )
    nearby = dists < 0.01
    n_count = int(nearby.sum())
    if n_count > 0:
        n_avg_cap = float(np.mean(market['capacities'][nearby]))
        n_avg_amenities = float(np.mean(market['amenity_counts'][nearby]))
    else:
        n_avg_cap = total_cap
        n_avg_amenities = max(amenity_count, 1)

    max_amenity_count = market_stats.get('max_amenity_count', 50)

    # --- Amenity binary flags ---
    amenity_flags = {f'am_{am}': int(am in amenities) for am in top_amenities}

    # --- Category counts ---
    category_counts = {}
    for cat, keywords in amenity_categories.items():
        category_counts[f'cat_{cat}'] = sum(1 for k in keywords if k in amenities)

    features = {
        'max_guests': max_guests,
        'bedrooms': bedrooms,
        'beds': beds,
        'baths': baths,
        'lat': lat,
        'lng': lng,
        'listing_type_enc': lt_enc,
        'room_type_enc': rt_enc,
        'is_entire': int('entire' in lt.lower()),
        'is_room': int('room' in lt.lower()),
        'total_capacity': total_cap,
        'size_score': bedrooms * 2 + beds + baths * 1.5,
        'guests_per_bedroom': max_guests / bedrooms,
        'beds_per_bedroom': beds / bedrooms,
        'baths_per_bedroom': baths / bedrooms,
        'beds_to_guests': beds / max_guests,
        'is_sweet_spot': int(2 <= bedrooms <= 3 and 4 <= max_guests <= 6),
        'dist_from_center': np.sqrt(
            (lat - market_stats['center_lat']) ** 2 + (lng - market_stats['center_lng']) ** 2
        ),
        'lat_lng_interaction': lat * lng,
        'neighbor_count': n_count,
        'neighbor_avg_capacity': n_avg_cap,
        'neighbor_avg_amenities': n_avg_amenities,
        'amenities_vs_neighborhood': amenity_count / max(n_avg_amenities, 1),
        'amenity_count': amenity_count,
        'amenity_richness': amenity_count / max(max_amenity_count, 1),
        'amenity_per_guest': amenity_count / max_guests,
        'amenity_per_bedroom': amenity_count / bedrooms,
    }
    features.update(amenity_flags)
    features.update(category_counts)

    return pd.DataFrame([features])[feature_cols]


# ==============================================================================
# MARKET PRICE PREDICTION
# ==============================================================================

def predict_market_price(listing: dict, models: dict) -> float:
    """
    Predict the market-rate price for a listing using the XGBoost model.
    Returns price in USD (per night).
    """
    X = _build_price_features(listing, models['price_meta'])
    log_price = models['price_model'].predict(X)[0]
    price = float(np.expm1(log_price))
    return round(max(price, 1.0), 2)


# ==============================================================================
# NEIGHBORHOOD COMPARABLE ANALYSIS
# ==============================================================================

def get_neighborhood_prices(listing: dict, models: dict) -> dict:
    """
    Find comparable listings in the same neighbourhood and return
    price statistics for context.
    """
    market = models['price_meta']['market_data']
    location = listing.get('location') or {}
    lat = location.get('lat', models['price_meta']['market_stats']['center_lat'])
    lng = location.get('lng', models['price_meta']['market_stats']['center_lng'])

    dists = np.sqrt(
        (market['coords'][:, 0] - lat) ** 2 + (market['coords'][:, 1] - lng) ** 2
    )

    # Try ~1 km radius first, expand if too few comparables
    for radius in [0.01, 0.02, 0.05]:
        nearby_mask = dists < radius
        if nearby_mask.sum() >= 5:
            break

    nearby_prices = market['prices'][nearby_mask]

    if len(nearby_prices) == 0:
        nearby_prices = market['prices']  # fallback to all listings

    return {
        'comparable_count': int(len(nearby_prices)),
        'min': round(float(np.min(nearby_prices)), 2),
        'q25': round(float(np.percentile(nearby_prices, 25)), 2),
        'median': round(float(np.median(nearby_prices)), 2),
        'q75': round(float(np.percentile(nearby_prices, 75)), 2),
        'max': round(float(np.max(nearby_prices)), 2),
        'mean': round(float(np.mean(nearby_prices)), 2),
    }


# ==============================================================================
# REVENUE-OPTIMISED PRICE (uses occupancy predictor)
# ==============================================================================

def _predict_occupancy_at_price(listing: dict, price: float, models: dict) -> float:
    """Predict occupancy rate at a given price using the occupancy model."""
    # Lazy import — only needed when occupancy model is available
    sys.path.insert(0, OCCUPANCY_MODEL_DIR)
    from predict import predict_occupancy

    listing_copy = dict(listing)
    listing_copy['price'] = price
    return predict_occupancy(
        listing_copy,
        model=models['occ_model'],
        encoders=models['occ_encoders'],
    )


def _compute_price_sensitivity(listing: dict, models: dict) -> float:
    """
    Compute a price-sensitivity coefficient (beta) for this listing.

    Higher beta = more price-sensitive (budget/standard listings).
    Lower beta  = less price-sensitive (premium/luxury listings).

    The optimal price ends up at approximately (1/beta) × market_price.
    Range: 0.5 (luxury) to 1.2 (budget).
    """
    amenities = set(listing.get('amenities') or [])
    max_guests = max(listing.get('max_guests', 1) or 1, 1)
    bedrooms = max(listing.get('bedrooms', 1) or 1, 1)
    location = listing.get('location') or {}
    lt = listing.get('listing_type', '').lower()

    market_stats = models['price_meta']['market_stats']
    max_am = market_stats.get('max_amenity_count', 50)

    # Factors that reduce sensitivity (lower beta → higher optimal price)
    amenity_richness = min(len(amenities) / max(max_am, 1), 1.0)  # 0-1
    is_large = min(bedrooms / 4.0, 1.0)           # Scaled 0-1
    is_entire = 1.0 if 'entire' in lt else 0.0
    is_premium_type = 1.0 if any(k in lt for k in ['villa', 'home', 'condo']) else 0.0

    # Centrality (closer to center = less sensitive)
    lat = location.get('lat', market_stats['center_lat'])
    lng = location.get('lng', market_stats['center_lng'])
    dist = np.sqrt((lat - market_stats['center_lat'])**2 + (lng - market_stats['center_lng'])**2)
    centrality = max(0, 1.0 - dist / 0.1)  # 0-1, 1=very central

    # Combine: base beta = 1.0, adjusted down for premium features
    premium_score = (
        0.25 * amenity_richness +
        0.20 * is_large +
        0.15 * is_entire +
        0.15 * is_premium_type +
        0.25 * centrality
    )
    beta = 1.2 - 0.7 * premium_score  # Range: 0.5 to 1.2

    return float(np.clip(beta, 0.5, 1.2))


def _estimate_occupancy_at_price(price: float, base_occupancy: float,
                                  market_price: float, beta: float) -> float:
    """
    Estimate occupancy at a given price using an exponential decay model.

    occ(price) = base_occ × exp(-beta × (price/market_price - 1))

    This model:
    - At market_price: returns base_occ exactly
    - Below market: occupancy increases (capped at 95%)
    - Above market: occupancy decays exponentially
    - beta controls how fast occupancy drops as price rises

    The revenue-maximising price is at (1/beta) × market_price.
    """
    if market_price <= 0:
        return base_occupancy

    ratio = price / market_price - 1.0  # 0 at market price
    occ = base_occupancy * np.exp(-beta * ratio)
    return float(np.clip(occ, 3.0, 95.0))


def find_optimal_price(listing: dict, models: dict,
                       price_low: float = None, price_high: float = None,
                       steps: int = 100) -> dict:
    """
    Sweep price points and find the one that maximises estimated monthly
    revenue = price × (occupancy_rate / 100) × 30.

    Uses an exponential demand model calibrated to each listing:
    1. Predict market price from the XGBoost model
    2. Predict base occupancy at market price (occupancy model or data)
    3. Compute listing-specific price sensitivity (beta)
    4. Sweep prices and find revenue maximum

    The theoretical optimum is at price* = market_price / beta, which is
    typically 1.0× – 2.0× the market price depending on listing quality.

    Returns dict with optimal_price, expected_occupancy, expected_monthly_revenue,
    and the full price-revenue curve.
    """
    market_price = predict_market_price(listing, models)
    neighborhood = get_neighborhood_prices(listing, models)

    # Step 1: Get base occupancy at market price
    if models['occ_model'] is not None:
        base_occupancy = _predict_occupancy_at_price(listing, market_price, models)
    else:
        # Fallback: neighbourhood median occupancy
        market = models['price_meta']['market_data']
        location = listing.get('location') or {}
        lat = location.get('lat', models['price_meta']['market_stats']['center_lat'])
        lng = location.get('lng', models['price_meta']['market_stats']['center_lng'])
        dists = np.sqrt(
            (market['coords'][:, 0] - lat) ** 2 + (market['coords'][:, 1] - lng) ** 2
        )
        nearby = dists < 0.02
        if nearby.sum() > 0:
            base_occupancy = float(np.median(market['occ_rates'][nearby]))
        else:
            base_occupancy = float(np.median(market['occ_rates']))

    # Step 2: Compute listing-specific price sensitivity
    beta = _compute_price_sensitivity(listing, models)

    # Step 3: Define search range
    if price_low is None:
        price_low = max(market_price * 0.4, 3.0)
    if price_high is None:
        price_high = max(market_price * 3.5, neighborhood['q75'] * 2.5)

    # Step 4: Sweep prices
    prices = np.linspace(price_low, price_high, steps)
    results = []

    for p in prices:
        occ = _estimate_occupancy_at_price(float(p), base_occupancy, market_price, beta)
        monthly_rev = p * (occ / 100) * 30
        results.append({
            'price': round(float(p), 2),
            'occupancy': round(float(occ), 1),
            'monthly_revenue': round(float(monthly_rev), 2),
        })

    # Find maximum revenue
    best = max(results, key=lambda r: r['monthly_revenue'])

    return {
        'optimal_price': best['price'],
        'expected_occupancy': best['occupancy'],
        'expected_monthly_revenue': best['monthly_revenue'],
        'base_occupancy_at_market_price': round(base_occupancy, 1),
        'price_sensitivity': round(beta, 3),
        'price_range_tested': {'low': round(float(price_low), 2), 'high': round(float(price_high), 2)},
        'curve': results,
    }


# ==============================================================================
# MAIN PREDICTION FUNCTION
# ==============================================================================

def predict_optimal_price(listing: dict, models: dict) -> dict:
    """
    Full price recommendation for a new listing.

    Args:
        listing: dict with keys:
            max_guests, bedrooms, beds, baths,
            listing_type, room_type,
            location: {lat, lng},
            amenities: [str, ...]
        models: dict from load_models()

    Returns:
        dict with:
            market_price         — model-predicted market rate
            neighborhood         — comparable price stats
            optimal_price        — revenue-maximised price (if occupancy model available)
            expected_occupancy   — occupancy at optimal price
            expected_monthly_rev — monthly revenue at optimal price
            recommendation       — human-readable recommendation
    """
    market_price = predict_market_price(listing, models)
    neighborhood = get_neighborhood_prices(listing, models)

    result = {
        'market_price': market_price,
        'neighborhood': neighborhood,
    }

    # Revenue optimisation
    optimization = find_optimal_price(listing, models)
    result['optimal_price'] = optimization['optimal_price']
    result['expected_occupancy'] = optimization['expected_occupancy']
    result['expected_monthly_revenue'] = optimization['expected_monthly_revenue']
    result['base_occupancy'] = optimization['base_occupancy_at_market_price']
    result['price_sensitivity'] = optimization['price_sensitivity']

    # Price range recommendation (±15% of optimal)
    opt = optimization['optimal_price']
    result['price_range'] = {
        'low': round(opt * 0.85, 2),
        'high': round(opt * 1.15, 2),
    }

    # Human-readable recommendation
    if opt > market_price * 1.15:
        positioning = "above market rate (premium positioning)"
    elif opt < market_price * 0.85:
        positioning = "below market rate (competitive positioning)"
    else:
        positioning = "at market rate"

    result['recommendation'] = (
        f"Set your nightly price to ${opt:.2f} ({positioning}). "
        f"At this price, expect ~{optimization['expected_occupancy']:.0f}% occupancy "
        f"and ~${optimization['expected_monthly_revenue']:.0f}/month revenue. "
        f"Comparable listings in your area charge "
        f"${neighborhood['q25']:.0f}–${neighborhood['q75']:.0f}/night."
    )

    result['revenue_curve'] = optimization['curve']

    return result


# ==============================================================================
# INTERACTIVE DEMO
# ==============================================================================

if __name__ == "__main__":
    print("Loading models...")
    models = load_models()
    print("Models loaded!\n")

    samples = [
        {
            "title": "Budget Studio Apartment",
            "max_guests": 2, "bedrooms": 1, "beds": 1, "baths": 1,
            "listing_type": "Entire rental unit", "room_type": "Entire rental unit",
            "location": {"lat": 33.65, "lng": 73.04},
            "amenities": ["Wifi", "Kitchen", "Air conditioning", "TV",
                          "Free parking on premises", "Washer", "Essentials", "Hot water"],
        },
        {
            "title": "Luxury 3BR Villa",
            "max_guests": 8, "bedrooms": 3, "beds": 4, "baths": 3,
            "listing_type": "Entire home", "room_type": "Entire home",
            "location": {"lat": 33.55, "lng": 73.10},
            "amenities": ["Wifi", "Kitchen", "Air conditioning", "TV",
                          "Free parking on premises", "Pool", "Hot tub", "BBQ grill",
                          "Fire pit", "Dedicated workspace", "Washer", "Dryer",
                          "Dishwasher", "Essentials", "Shampoo", "Body soap",
                          "Hot water", "Bed linens", "Extra pillows and blankets",
                          "Fire extinguisher", "First aid kit", "Smoke alarm",
                          "Exterior security cameras on property", "Self check-in",
                          "Iron", "Hair dryer", "Coffee", "Breakfast"],
        },
        {
            "title": "Cozy Private Room",
            "max_guests": 2, "bedrooms": 1, "beds": 1, "baths": 1,
            "listing_type": "Private room", "room_type": "Private room",
            "location": {"lat": 33.70, "lng": 73.05},
            "amenities": ["Wifi", "Air conditioning", "TV", "Hot water", "Essentials"],
        },
        {
            "title": "Mid-Range 2BR — Well Equipped",
            "max_guests": 4, "bedrooms": 2, "beds": 2, "baths": 1,
            "listing_type": "Entire rental unit", "room_type": "Entire rental unit",
            "location": {"lat": 33.65, "lng": 73.06},
            "amenities": ["Wifi", "Kitchen", "Air conditioning", "TV",
                          "Free parking on premises", "Washer", "Microwave",
                          "Refrigerator", "Cooking basics", "Dishes and silverware",
                          "Iron", "Hair dryer", "Shampoo", "Body soap", "Hot water",
                          "Bed linens", "Essentials", "Fire extinguisher",
                          "Smoke alarm", "Self check-in", "Dedicated workspace",
                          "Hangers", "Cleaning products"],
        },
    ]

    for s in samples:
        print("=" * 60)
        print(f"  {s['title']}")
        print("=" * 60)
        result = predict_optimal_price(s, models)
        print(f"  Market Price:          ${result['market_price']:.2f}/night")
        print(f"  Optimal Price:         ${result['optimal_price']:.2f}/night")
        if 'expected_occupancy' in result:
            print(f"  Expected Occupancy:    {result['expected_occupancy']:.0f}%")
            print(f"  Expected Monthly Rev:  ${result['expected_monthly_revenue']:.0f}")
        print(f"  Price Range:           ${result['price_range']['low']:.2f} – ${result['price_range']['high']:.2f}")
        print(f"  Neighborhood Median:   ${result['neighborhood']['median']:.2f}")
        print(f"  Comparable Listings:   {result['neighborhood']['comparable_count']}")
        print(f"\n  >> {result['recommendation']}")
        print()
