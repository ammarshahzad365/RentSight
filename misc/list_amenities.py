import json, os, sys
from collections import Counter

sys.stdout = open(r'C:\Users\PMYLS\Desktop\Final Year Project\RentSight\all_amenities.txt', 'w', encoding='utf-8')

d = r'C:\Users\PMYLS\Desktop\Final Year Project\RentSight\listings-sanitized'
c = Counter()
total = 0
for f in os.listdir(d):
    if f.endswith('.json'):
        total += 1
        data = json.load(open(os.path.join(d, f), encoding='utf-8'))
        for a in data.get('amenities', []):
            c[a] += 1

print(f'Total unique amenities: {len(c)}')
print(f'Total listings: {total}')
print()
for amenity, count in c.most_common():
    print(f'{count:>6}  {amenity}')

sys.stdout.close()
