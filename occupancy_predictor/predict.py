import os
import pickle
import numpy as np
import pandas as pd

MODEL_DIR = os.path.dirname(__file__)


def load_model():
    """Load the trained model, encoders, and baked-in market data."""
    model_path = os.path.join(MODEL_DIR, 'xgb_occupancy_model.pkl')
    encoders_path = os.path.join(MODEL_DIR, 'label_encoders.pkl')

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    with open(encoders_path, 'rb') as f:
        encoders = pickle.load(f)

    return model, encoders


def predict_occupancy(listing: dict, model=None, encoders=None) -> float:
    """
    Predict occupancy rate for a single listing.

    Args:
        listing: Dictionary with keys:
            price, max_guests, bedrooms, beds, baths,
            listing_type, room_type,
            location (dict with lat, lng),
            amenities (list of amenity strings)
        model: Pre-loaded model (optional, will load from disk if not provided)
        encoders: Pre-loaded encoders (optional)

    Returns:
        Predicted occupancy rate (10-95%)
    """
    if model is None or encoders is None:
        model, encoders = load_model()

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
        (market['coords'][:, 0] - lat)**2 + (market['coords'][:, 1] - lng)**2
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

    # --- Build feature dict ---
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
            (lat - market_stats['center_lat'])**2 + (lng - market_stats['center_lng'])**2
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

    # Merge amenity flags and category counts
    features.update(amenity_flags)
    features.update(category_counts)

    df = pd.DataFrame([features])[feature_cols]
    prediction = model.predict(df)[0]
    return round(float(np.clip(prediction, 10, 95)), 1)


# ==============================================================================
# INTERACTIVE DEMO
# ==============================================================================

if __name__ == "__main__":
    print("Loading model...")
    model, encoders = load_model()
    print("Model loaded!\n")

    samples = [
        {
            "title": "Budget Studio Apartment",
            "price": 15.0, "max_guests": 2, "bedrooms": 1, "beds": 1, "baths": 1,
            "listing_type": "Entire rental unit", "room_type": "Entire rental unit",
            "location": {"lat": 33.65, "lng": 73.04},
            "amenities": ["Wifi", "Kitchen", "Air conditioning", "TV", "Free parking on premises",
                          "Washer", "Essentials", "Hot water"]
        },
        {
            "title": "Luxury 3BR Villa",
            "price": 120.0, "max_guests": 8, "bedrooms": 3, "beds": 4, "baths": 3,
            "listing_type": "Entire home", "room_type": "Entire home",
            "location": {"lat": 33.55, "lng": 73.10},
            "amenities": ["Wifi", "Kitchen", "Air conditioning", "TV", "Free parking on premises",
                          "Pool", "Hot tub", "BBQ grill", "Fire pit", "Dedicated workspace",
                          "Washer", "Dryer", "Dishwasher", "Essentials", "Shampoo", "Body soap",
                          "Hot water", "Bed linens", "Extra pillows and blankets",
                          "Fire extinguisher", "First aid kit", "Smoke alarm",
                          "Exterior security cameras on property", "Self check-in",
                          "Elevator", "Iron", "Hair dryer", "Coffee", "Breakfast"]
        },
        {
            "title": "Cozy Private Room",
            "price": 10.0, "max_guests": 2, "bedrooms": 1, "beds": 1, "baths": 1,
            "listing_type": "Private room", "room_type": "Private room",
            "location": {"lat": 33.70, "lng": 73.05},
            "amenities": ["Wifi", "Air conditioning", "TV", "Hot water", "Essentials"]
        },
        {
            "title": "Mid-Range 2BR — Well Equipped",
            "price": 40.0, "max_guests": 4, "bedrooms": 2, "beds": 2, "baths": 1,
            "listing_type": "Entire rental unit", "room_type": "Entire rental unit",
            "location": {"lat": 33.65, "lng": 73.06},
            "amenities": ["Wifi", "Kitchen", "Air conditioning", "TV", "Free parking on premises",
                          "Washer", "Microwave", "Refrigerator", "Cooking basics",
                          "Dishes and silverware", "Iron", "Hair dryer", "Shampoo",
                          "Body soap", "Hot water", "Bed linens", "Essentials",
                          "Fire extinguisher", "Smoke alarm", "Self check-in",
                          "Dedicated workspace", "Hangers", "Cleaning products"]
        },
    ]

    print(f"{'Listing':<35s} {'Price':>6s} {'Guests':>6s} {'Amenities':>9s} {'Predicted':>10s}")
    print("-" * 70)
    for s in samples:
        occ = predict_occupancy(s, model, encoders)
        n_am = len(s.get('amenities', []))
        print(f"{s['title']:<35s} ${s['price']:>5.0f} {s['max_guests']:>6d} {n_am:>9d} {occ:>9.1f}%")
