"""
RentSight Combined API — Prediction Module
============================================
Unified prediction interface that wraps both the **occupancy predictor** and
the **price predictor** into a single module.

Two primary workflows:

1. **Price provided**     → predict occupancy at that price, then derive
                            revenue / positioning metrics.
2. **Price NOT provided** → predict market & optimal prices first, then
                            predict occupancy at those prices, then derive
                            revenue / positioning metrics.

Usage:
    from predict import load_all_models, predict_with_price, predict_without_price
    models = load_all_models()
    result = predict_with_price(listing, models)
    result = predict_without_price(listing, models)
"""

import os
import pickle
import numpy as np
import pandas as pd

# ==============================================================================
# PATHS — all models live in this directory
# ==============================================================================

MODEL_DIR = os.path.dirname(__file__)


# ==============================================================================
# MODEL LOADING
# ==============================================================================

def load_all_models() -> dict:
    """
    Load all artefacts from both predictors.

    Returns a dict with:
        price_model, price_meta          — XGBoost price model + metadata
        occ_model, occ_encoders          — XGBoost occupancy model + metadata
    """
    # --- Price model ---
    with open(os.path.join(MODEL_DIR, 'xgb_price_model.pkl'), 'rb') as f:
        price_model = pickle.load(f)
    with open(os.path.join(MODEL_DIR, 'price_model_meta.pkl'), 'rb') as f:
        price_meta = pickle.load(f)

    # --- Occupancy model ---
    with open(os.path.join(MODEL_DIR, 'xgb_occupancy_model.pkl'), 'rb') as f:
        occ_model = pickle.load(f)
    with open(os.path.join(MODEL_DIR, 'label_encoders.pkl'), 'rb') as f:
        occ_encoders = pickle.load(f)

    return {
        'price_model': price_model,
        'price_meta': price_meta,
        'occ_model': occ_model,
        'occ_encoders': occ_encoders,
    }


# ==============================================================================
# FEATURE BUILDING — Price Model  (NO price features)
# ==============================================================================

def _build_price_features(listing: dict, meta: dict) -> pd.DataFrame:
    """Build the feature vector expected by the price-prediction model."""
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
# FEATURE BUILDING — Occupancy Model  (INCLUDES price features)
# ==============================================================================

def _build_occupancy_features(listing: dict, encoders: dict) -> pd.DataFrame:
    """Build the feature vector expected by the occupancy-prediction model."""
    le_listing = encoders['listing_type']
    le_room = encoders['room_type']
    feature_cols = encoders['feature_cols']
    top_amenities = encoders['top_amenities']
    amenity_categories = encoders['amenity_categories']
    market_stats = encoders['market_stats']
    market = encoders['market_data']

    location = listing.get('location') or {}
    amenities = set(listing.get('amenities') or [])

    # --- Encode categoricals ---
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
    price = listing.get('price', 0) or 0
    max_guests = max(listing.get('max_guests', 1) or 1, 1)
    bedrooms = max(listing.get('bedrooms', 1) or 1, 1)
    beds = max(listing.get('beds', 1) or 1, 1)
    baths = max(listing.get('baths', 1) or 1, 1)
    lat = location.get('lat', market_stats['center_lat'])
    lng = location.get('lng', market_stats['center_lng'])

    total_cap = bedrooms + beds + baths
    amenity_count = len(amenities)

    # --- Neighborhood stats ---
    dists = np.sqrt(
        (market['coords'][:, 0] - lat) ** 2 + (market['coords'][:, 1] - lng) ** 2
    )
    nearby = dists < 0.01
    n_count = int(nearby.sum())
    if n_count > 0:
        n_avg_price = float(np.mean(market['prices'][nearby]))
        n_avg_cap = float(np.mean(market['capacities'][nearby]))
        n_price_rank = float(np.mean(market['prices'][nearby] <= price))
        n_avg_amenities = float(np.mean(market['amenity_counts'][nearby]))
    else:
        n_avg_price = max(price, 1)
        n_avg_cap = total_cap
        n_price_rank = 0.5
        n_avg_amenities = max(amenity_count, 1)

    # --- Price tier ---
    if price <= market_stats['price_q25']:
        price_tier = 0.0
    elif price <= market_stats['price_median']:
        price_tier = 1.0
    elif price <= market_stats['price_q75']:
        price_tier = 2.0
    else:
        price_tier = 3.0

    # --- Amenity binary flags ---
    amenity_flags = {f'am_{am}': int(am in amenities) for am in top_amenities}

    # --- Amenity category counts ---
    category_counts = {}
    for cat, keywords in amenity_categories.items():
        category_counts[f'cat_{cat}'] = sum(1 for k in keywords if k in amenities)

    max_amenity_count = market_stats.get('max_amenity_count', 50)

    features = {
        'price': price,
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
        'price_per_guest': price / max_guests,
        'price_per_bedroom': price / bedrooms,
        'price_per_bed': price / beds,
        'guests_per_bedroom': max_guests / bedrooms,
        'beds_per_bedroom': beds / bedrooms,
        'baths_per_bedroom': baths / bedrooms,
        'beds_to_guests': beds / max_guests,
        'total_capacity': total_cap,
        'size_score': bedrooms * 2 + beds + baths * 1.5,
        'is_sweet_spot': int(2 <= bedrooms <= 3 and 4 <= max_guests <= 6),
        'log_price': np.log1p(price),
        'price_squared': price ** 2,
        'price_tier': price_tier,
        'dist_from_center': np.sqrt(
            (lat - market_stats['center_lat']) ** 2 + (lng - market_stats['center_lng']) ** 2
        ),
        'lat_lng_interaction': lat * lng,
        'neighbor_count': n_count,
        'neighbor_avg_price': n_avg_price,
        'neighbor_avg_capacity': n_avg_cap,
        'neighbor_price_rank': n_price_rank,
        'price_vs_neighborhood': price / max(n_avg_price, 1),
        'neighbor_avg_amenities': n_avg_amenities,
        'amenities_vs_neighborhood': amenity_count / max(n_avg_amenities, 1),
        'amenity_count': amenity_count,
        'amenity_richness': amenity_count / max(max_amenity_count, 1),
        'amenity_per_guest': amenity_count / max_guests,
        'amenity_per_bedroom': amenity_count / bedrooms,
        'amenity_per_price': amenity_count / max(price, 1),
    }

    features.update(amenity_flags)
    features.update(category_counts)

    return pd.DataFrame([features])[feature_cols]


# ==============================================================================
# CORE PREDICTION HELPERS
# ==============================================================================

def _predict_market_price(listing: dict, models: dict) -> float:
    """Predict the market-rate price using the price XGBoost model."""
    X = _build_price_features(listing, models['price_meta'])
    log_price = models['price_model'].predict(X)[0]
    price = float(np.expm1(log_price))
    return round(max(price, 1.0), 2)


def _predict_occupancy(listing: dict, price: float, models: dict) -> float:
    """Predict occupancy rate at a given price using the occupancy XGBoost model."""
    listing_copy = dict(listing)
    listing_copy['price'] = price
    X = _build_occupancy_features(listing_copy, models['occ_encoders'])
    prediction = models['occ_model'].predict(X)[0]
    return round(float(np.clip(prediction, 10, 95)), 1)


def _get_neighborhood_prices(listing: dict, models: dict) -> dict:
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
# REVENUE OPTIMISATION (price sweep)
# ==============================================================================

def _compute_price_sensitivity(listing: dict, models: dict) -> float:
    """
    Compute a price-sensitivity coefficient (beta) for this listing.

    Higher beta = more price-sensitive (budget/standard listings).
    Lower beta  = less price-sensitive (premium/luxury listings).

    Range: 0.5 (luxury) → 1.2 (budget).
    """
    amenities = set(listing.get('amenities') or [])
    bedrooms = max(listing.get('bedrooms', 1) or 1, 1)
    location = listing.get('location') or {}
    lt = listing.get('listing_type', '').lower()

    market_stats = models['price_meta']['market_stats']
    max_am = market_stats.get('max_amenity_count', 50)

    amenity_richness = min(len(amenities) / max(max_am, 1), 1.0)
    is_large = min(bedrooms / 4.0, 1.0)
    is_entire = 1.0 if 'entire' in lt else 0.0
    is_premium_type = 1.0 if any(k in lt for k in ['villa', 'home', 'condo']) else 0.0

    lat = location.get('lat', market_stats['center_lat'])
    lng = location.get('lng', market_stats['center_lng'])
    dist = np.sqrt((lat - market_stats['center_lat']) ** 2 + (lng - market_stats['center_lng']) ** 2)
    centrality = max(0, 1.0 - dist / 0.1)

    premium_score = (
        0.25 * amenity_richness +
        0.20 * is_large +
        0.15 * is_entire +
        0.15 * is_premium_type +
        0.25 * centrality
    )
    beta = 1.2 - 0.7 * premium_score
    return float(np.clip(beta, 0.5, 1.2))


def _estimate_occupancy_at_price(price: float, base_occupancy: float,
                                  market_price: float, beta: float) -> float:
    """Exponential demand model for revenue sweep."""
    if market_price <= 0:
        return base_occupancy
    ratio = price / market_price - 1.0
    occ = base_occupancy * np.exp(-beta * ratio)
    return float(np.clip(occ, 3.0, 95.0))


def _find_optimal_price(listing: dict, models: dict,
                        steps: int = 100) -> dict:
    """
    Sweep price points and find the one that maximises estimated monthly
    revenue = price × (occupancy_rate / 100) × 30.
    """
    market_price = _predict_market_price(listing, models)
    neighborhood = _get_neighborhood_prices(listing, models)

    # Base occupancy at market price (from the occupancy model)
    base_occupancy = _predict_occupancy(listing, market_price, models)

    # Price sensitivity
    beta = _compute_price_sensitivity(listing, models)

    # Search range
    price_low = max(market_price * 0.4, 3.0)
    price_high = max(market_price * 3.5, neighborhood['q75'] * 2.5)

    # Sweep
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

    best = max(results, key=lambda r: r['monthly_revenue'])

    return {
        'market_price': market_price,
        'optimal_price': best['price'],
        'base_occupancy': round(base_occupancy, 1),
        'expected_occupancy_at_optimal': best['occupancy'],
        'expected_monthly_revenue': best['monthly_revenue'],
        'price_sensitivity': round(beta, 3),
        'neighborhood': neighborhood,
    }


# ==============================================================================
# DERIVED FIELDS  (computed once we have both price & occupancy)
# ==============================================================================

def _compute_derived_fields(price: float, occupancy: float,
                            listing: dict, models: dict) -> dict:
    """
    Given a final price and occupancy rate, produce all derived metrics:
      - expected monthly revenue
      - expected annual revenue
      - daily earnings estimate
      - price positioning vs market & neighbourhood
      - booked nights per month / year
      - human-readable recommendation
    """
    neighborhood = _get_neighborhood_prices(listing, models)
    market_price = _predict_market_price(listing, models)

    booked_nights_month = round(30 * (occupancy / 100), 1)
    booked_nights_year = round(365 * (occupancy / 100), 0)
    monthly_revenue = round(price * booked_nights_month, 2)
    annual_revenue = round(price * booked_nights_year, 2)
    daily_earnings = round(monthly_revenue / 30, 2)

    # Positioning
    if price > market_price * 1.15:
        positioning = "above market rate (premium positioning)"
    elif price < market_price * 0.85:
        positioning = "below market rate (competitive positioning)"
    else:
        positioning = "at market rate"

    # Price range recommendation (±15% of given price)
    price_range = {
        'low': round(price * 0.85, 2),
        'high': round(price * 1.15, 2),
    }

    recommendation = (
        f"At ${price:.2f}/night ({positioning}), expect ~{occupancy:.0f}% occupancy "
        f"(~{booked_nights_month:.0f} nights/month). "
        f"Estimated monthly revenue: ${monthly_revenue:,.0f}. "
        f"Comparable listings in your area charge "
        f"${neighborhood['q25']:.0f}–${neighborhood['q75']:.0f}/night."
    )

    return {
        'market_price': market_price,
        'price': price,
        'occupancy_rate': occupancy,
        'positioning': positioning,
        'booked_nights_per_month': booked_nights_month,
        'booked_nights_per_year': int(booked_nights_year),
        'monthly_revenue': monthly_revenue,
        'annual_revenue': annual_revenue,
        'daily_earnings': daily_earnings,
        'price_range': price_range,
        'neighborhood': neighborhood,
        'recommendation': recommendation,
    }


# ==============================================================================
# PUBLIC API — Endpoint 1: PRICE PROVIDED
# ==============================================================================

def predict_with_price(listing: dict, models: dict) -> dict:
    """
    When the user provides a price along with all listing fields:
      1. Predict occupancy at that exact price.
      2. Compute all derived revenue / positioning metrics.

    Args:
        listing: dict with keys:
            price, max_guests, bedrooms, beds, baths,
            listing_type, room_type,
            location: {lat, lng},
            amenities: [str, ...]
        models: dict from load_all_models()

    Returns:
        dict with occupancy_rate, revenue metrics, neighbourhood stats,
        positioning, and recommendation.
    """
    price = listing['price']

    # Step 1: predict occupancy at the given price
    occupancy = _predict_occupancy(listing, price, models)

    # Step 2: derive all fields from price + occupancy
    result = _compute_derived_fields(price, occupancy, listing, models)

    # Remove fields not needed for this endpoint
    result.pop('neighborhood', None)
    result.pop('price_range', None)

    return result


# ==============================================================================
# PUBLIC API — Endpoint 2: PRICE NOT PROVIDED
# ==============================================================================

def predict_without_price(listing: dict, models: dict) -> dict:
    """
    When the user does NOT provide a price:
      1. Predict market & optimal price.
      2. Predict occupancy at the optimal price.
      3. Compute all derived revenue / positioning metrics.

    Args:
        listing: dict with keys:
            max_guests, bedrooms, beds, baths,
            listing_type, room_type,
            location: {lat, lng},
            amenities: [str, ...]
        models: dict from load_all_models()

    Returns:
        dict with optimal_price, market_price, occupancy, revenue metrics,
        neighbourhood stats, positioning, and recommendation.
    """
    # Step 1: find best price
    optimization = _find_optimal_price(listing, models)

    optimal_price = optimization['optimal_price']
    market_price = optimization['market_price']

    # Step 2: predict occupancy at optimal price using the occupancy model
    occupancy_at_optimal = _predict_occupancy(listing, optimal_price, models)

    # Also predict occupancy at market price for comparison
    occupancy_at_market = _predict_occupancy(listing, market_price, models)

    # Step 3: derive all fields using optimal price + occupancy
    result = _compute_derived_fields(optimal_price, occupancy_at_optimal, listing, models)

    # Add price-prediction-specific extras
    result['optimal_price'] = optimal_price
    result['occupancy_at_market_price'] = occupancy_at_market
    result['price_sensitivity'] = optimization['price_sensitivity']
    result['amenity_count'] = len(listing.get('amenities') or [])

    # Market-price comparison block
    market_booked = round(30 * (occupancy_at_market / 100), 1)
    market_monthly_rev = round(market_price * market_booked, 2)
    result['market_price_analysis'] = {
        'market_price': market_price,
        'occupancy_at_market_price': occupancy_at_market,
        'booked_nights_per_month': market_booked,
        'monthly_revenue_at_market': market_monthly_rev,
    }

    return result


# ==============================================================================
# INTERACTIVE DEMO
# ==============================================================================

if __name__ == "__main__":
    print("Loading all models...")
    models = load_all_models()
    print("Models loaded!\n")

    sample = {
        "max_guests": 4,
        "bedrooms": 2,
        "beds": 2,
        "baths": 1,
        "listing_type": "Entire rental unit",
        "room_type": "Entire rental unit",
        "location": {"lat": 33.65, "lng": 73.06},
        "amenities": [
            "Wifi", "Kitchen", "Air conditioning", "TV",
            "Free parking on premises", "Washer", "Essentials", "Hot water",
        ],
    }

    print("=" * 60)
    print("  Scenario 1: Price NOT provided")
    print("=" * 60)
    r1 = predict_without_price(sample, models)
    print(f"  Market price:        ${r1['market_price']:.2f}/night")
    print(f"  Optimal price:       ${r1['optimal_price']:.2f}/night")
    print(f"  Occupancy:           {r1['occupancy_rate']:.0f}%")
    print(f"  Monthly revenue:     ${r1['monthly_revenue']:,.0f}")
    print(f"  Annual revenue:      ${r1['annual_revenue']:,.0f}")
    print(f"  >> {r1['recommendation']}")

    print()

    sample_with_price = {**sample, "price": 35.0}
    print("=" * 60)
    print("  Scenario 2: Price PROVIDED ($35)")
    print("=" * 60)
    r2 = predict_with_price(sample_with_price, models)
    print(f"  Price:               ${r2['price']:.2f}/night")
    print(f"  Occupancy:           {r2['occupancy_rate']:.0f}%")
    print(f"  Monthly revenue:     ${r2['monthly_revenue']:,.0f}")
    print(f"  Annual revenue:      ${r2['annual_revenue']:,.0f}")
    print(f"  >> {r2['recommendation']}")
