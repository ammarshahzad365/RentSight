import json, os, statistics
from collections import Counter

d = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')
files = [f for f in os.listdir(d) if f.endswith('.json')]
print(f'Total files: {len(files)}')

prices = []
occ_rates = []
amenity_counts = []
null_prices = 0
null_occ = 0
all_amenities = set()

for f in files:
    with open(os.path.join(d, f), 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    p = data.get('price')
    o = data.get('occ_rate')
    a = data.get('amenities', [])
    amenity_counts.append(len(a))
    for am in a:
        all_amenities.add(am)
    if p is not None:
        prices.append(p)
    else:
        null_prices += 1
    if o is not None:
        occ_rates.append(o)
    else:
        null_occ += 1

print(f'Null prices: {null_prices}, Null occ_rate: {null_occ}')
print(f'Price - min: {min(prices)}, max: {max(prices)}, mean: {statistics.mean(prices):.2f}, median: {statistics.median(prices):.2f}')
print(f'Occ rate - min: {min(occ_rates)}, max: {max(occ_rates)}, mean: {statistics.mean(occ_rates):.2f}, median: {statistics.median(occ_rates):.2f}')
print(f'Amenity counts - min: {min(amenity_counts)}, max: {max(amenity_counts)}, mean: {statistics.mean(amenity_counts):.2f}')
print(f'Total unique amenities: {len(all_amenities)}')

buckets = Counter()
for p in prices:
    if p < 10: buckets['0-10'] += 1
    elif p < 25: buckets['10-25'] += 1
    elif p < 50: buckets['25-50'] += 1
    elif p < 100: buckets['50-100'] += 1
    elif p < 200: buckets['100-200'] += 1
    elif p < 500: buckets['200-500'] += 1
    else: buckets['500+'] += 1

for k in sorted(buckets.keys()):
    print(f'  ${k}: {buckets[k]}')
