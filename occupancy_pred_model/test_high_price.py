"""Test model predictions with high prices"""
from predict_multimodal import predict_with_breakdown

# Test with extremely high price (150,000)
test_cases = [
    {'price': 30, 'label': 'Normal price (30)'},
    {'price': 50, 'label': 'Above average price (50)'},
    {'price': 150, 'label': 'High price (150)'},
    {'price': 500, 'label': 'Very high price (500)'},
    {'price': 1000, 'label': 'Extremely high price (1000)'},
    {'price': 150000, 'label': 'Unrealistic price (150000)'},
]

base_listing = {
    'listing_type': 'Entire rental unit',
    'room_type': 'Entire home',
    'max_guests': 4,
    'bedrooms': 2,
    'beds': 2,
    'baths': 1,
    'lat': 33.7,
    'lng': 73.05
}

print("Testing model predictions with varying prices:\n")
print("-" * 80)

for test in test_cases:
    listing = base_listing.copy()
    listing['price'] = test['price']
    
    result = predict_with_breakdown(listing)
    print(f"{test['label']:40} => Occupancy: {result['final_prediction']:6.2f}% ({result['category']})")
    
print("-" * 80)
