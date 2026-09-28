import json
import os
from collections import Counter, defaultdict

LISTINGS_DIR = os.path.join(os.path.dirname(__file__), '..', 'listings')

# Collect all data
rating_fields = [
    'rating_overall', 'rating_cleanliness', 'rating_accuracy',
    'rating_checkin', 'rating_communication', 'rating_location', 'rating_value'
]
numeric_fields = ['bedrooms', 'beds', 'baths', 'max_guests']

ratings_data = {f: [] for f in rating_fields}
ratings_null_count = {f: 0 for f in rating_fields}
ratings_nonnull_count = {f: 0 for f in rating_fields}

numeric_data = {f: [] for f in numeric_fields}
numeric_null_count = {f: 0 for f in numeric_fields}

review_counts = []
amenity_category_counter = Counter()
listings_with_amenities = 0
listings_without_amenities = 0
listing_type_counter = Counter()
room_type_counter = Counter()

total_files = 0
errors = 0

for fname in os.listdir(LISTINGS_DIR):
    if not fname.endswith('.json'):
        continue
    total_files += 1
    try:
        with open(os.path.join(LISTINGS_DIR, fname), 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        errors += 1
        continue

    # Ratings
    for rf in rating_fields:
        val = data.get(rf)
        if val is None:
            ratings_null_count[rf] += 1
        else:
            try:
                ratings_data[rf].append(float(val))
                ratings_nonnull_count[rf] += 1
            except (ValueError, TypeError):
                ratings_null_count[rf] += 1

    # Numeric fields
    for nf in numeric_fields:
        val = data.get(nf)
        if val is None:
            numeric_null_count[nf] += 1
        else:
            try:
                numeric_data[nf].append(float(val))
            except (ValueError, TypeError):
                numeric_null_count[nf] += 1

    # Reviews
    reviews = data.get('reviews', [])
    if reviews is None:
        reviews = []
    review_counts.append(len(reviews))

    # Amenities
    amenities = data.get('amenities', {})
    if amenities and isinstance(amenities, dict) and len(amenities) > 0:
        listings_with_amenities += 1
        for cat in amenities.keys():
            amenity_category_counter[cat] += 1
    else:
        listings_without_amenities += 1

    # Listing type & room type
    lt = data.get('listing_type', None)
    listing_type_counter[lt] += 1
    rt = data.get('room_type', None)
    room_type_counter[rt] += 1

# ---- PRINT RESULTS ----
print("=" * 70)
print(f"LISTING ANALYSIS REPORT — {total_files} total files ({errors} read errors)")
print("=" * 70)

# Ratings
print("\n--- RATINGS ---")
for rf in rating_fields:
    vals = ratings_data[rf]
    null_c = ratings_null_count[rf]
    nonnull_c = ratings_nonnull_count[rf]
    if vals:
        avg = sum(vals) / len(vals)
        print(f"  {rf}:  null={null_c}  non-null={nonnull_c}  min={min(vals):.2f}  max={max(vals):.2f}  avg={avg:.2f}")
    else:
        print(f"  {rf}:  null={null_c}  non-null={nonnull_c}  (no values)")

# Reviews distribution
print("\n--- REVIEWS DISTRIBUTION ---")
buckets = {'0': 0, '1-5': 0, '6-10': 0, '11-20': 0, '21-50': 0, '50+': 0}
for rc in review_counts:
    if rc == 0:
        buckets['0'] += 1
    elif rc <= 5:
        buckets['1-5'] += 1
    elif rc <= 10:
        buckets['6-10'] += 1
    elif rc <= 20:
        buckets['11-20'] += 1
    elif rc <= 50:
        buckets['21-50'] += 1
    else:
        buckets['50+'] += 1
for b, c in buckets.items():
    print(f"  {b:>5} reviews: {c} listings ({c/total_files*100:.1f}%)")
print(f"  Total reviews across all listings: {sum(review_counts)}")
if review_counts:
    print(f"  Avg reviews per listing: {sum(review_counts)/len(review_counts):.2f}")
    print(f"  Max reviews on a single listing: {max(review_counts)}")

# Amenities
print("\n--- AMENITIES ---")
print(f"  Listings WITH amenities: {listings_with_amenities}")
print(f"  Listings WITHOUT amenities: {listings_without_amenities}")
print(f"\n  Amenity categories (sorted by frequency):")
for cat, cnt in amenity_category_counter.most_common():
    print(f"    {cat}: {cnt} listings ({cnt/total_files*100:.1f}%)")

# Listing type
print("\n--- LISTING TYPE ---")
for lt, cnt in listing_type_counter.most_common():
    print(f"  {lt}: {cnt} ({cnt/total_files*100:.1f}%)")

# Room type
print("\n--- ROOM TYPE ---")
for rt, cnt in room_type_counter.most_common():
    print(f"  {rt}: {cnt} ({cnt/total_files*100:.1f}%)")

# Numeric fields
print("\n--- NUMERIC FIELDS (bedrooms, beds, baths, max_guests) ---")
for nf in numeric_fields:
    vals = numeric_data[nf]
    null_c = numeric_null_count[nf]
    if vals:
        avg = sum(vals) / len(vals)
        print(f"  {nf}:  null={null_c}  non-null={len(vals)}  min={min(vals):.1f}  max={max(vals):.1f}  avg={avg:.2f}")
    else:
        print(f"  {nf}:  null={null_c}  non-null=0  (no values)")

# Price (raw strings - just show a sample)
print("\n--- PRICE (raw strings in original files) ---")
print("  Prices are raw text strings in original files. Skipping numeric analysis.")
print("  Sample prices from first 3 files:")
sample_count = 0
for fname in sorted(os.listdir(LISTINGS_DIR)):
    if not fname.endswith('.json'):
        continue
    if sample_count >= 3:
        break
    with open(os.path.join(LISTINGS_DIR, fname), 'r', encoding='utf-8') as f:
        data = json.load(f)
    price = data.get('price', 'N/A')
    print(f"    {fname}: {repr(price[:80] if price else price)}...")
    sample_count += 1

print("\n" + "=" * 70)
print("DONE")
