# Occupancy Rate Prediction - Usage Guide

## Overview
This module provides a trained machine learning model to predict occupancy rates for rental listings based on their features.

**Best Model:** Random Forest with PCA  
**Performance:** RMSE 17.01, MAE 13.54  
**Category Accuracy:** 48.08%

---

## Quick Start

### 1. Interactive Prediction (Single Listing)
```bash
python predict_occupancy.py
```

You'll be prompted to enter listing details:
- Listing Type (see valid values below)
- Price per night ($)
- Maximum guests
- Number of bedrooms
- Number of beds
- Number of bathrooms
- Latitude
- Longitude

### 2. Example Prediction
```bash
python predict_occupancy.py --example
```

Runs a prediction with sample data to verify the model is working.

### 3. Batch Prediction
```bash
python predict_occupancy.py --batch
```

Demonstrates how to predict multiple listings at once.

---

## Using the Prediction API

### Python Code Example

```python
from predict_occupancy import predict_occupancy

# Define your listing
listing = {
    'listing_type': 'Entire rental unit',
    'room_type': 'Entire rental unit',
    'price': 150.0,
    'max_guests': 4,
    'bedrooms': 2,
    'beds': 2,
    'baths': 1.5,
    'lat': 40.7128,
    'lng': -74.0060
}

# Get prediction
occupancy_rate = predict_occupancy(listing)
print(f"Predicted Occupancy: {occupancy_rate:.2f}%")
```

### Batch Predictions

```python
from predict_occupancy import predict_batch

listings = [
    {
        'listing_type': 'Entire rental unit',
        'room_type': 'Entire rental unit',
        'price': 150.0,
        'max_guests': 4,
        'bedrooms': 2,
        'beds': 2,
        'baths': 1.5,
        'lat': 40.7128,
        'lng': -74.0060
    },
    {
        'listing_type': 'Private room',
        'room_type': 'Private room',
        'price': 75.0,
        'max_guests': 2,
        'bedrooms': 1,
        'beds': 1,
        'baths': 1.0,
        'lat': 40.7580,
        'lng': -73.9855
    }
]

results = predict_batch(listings)
for result in results:
    print(f"Listing {result['listing_id']}: {result['occupancy_rate']:.2f}% - {result['category']}")
```

---

## Valid Listing Types

Based on the training data, the following listing/room types are recognized:

- `Entire rental unit`
- `Entire home`
- `Entire serviced apartment`
- `Entire condo`
- `Entire guest suite`
- `Entire villa`
- `Entire bungalow`
- `Entire bed and breakfast`
- `Private room`
- `Room`
- `Treehouse`

**Note:** `listing_type` and `room_type` should typically be the same value.

---

## Input Features

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `listing_type` | string | Type of rental (see valid values above) | `'Entire rental unit'` |
| `room_type` | string | Room type (usually same as listing_type) | `'Entire rental unit'` |
| `price` | float | Nightly price in dollars | `150.0` |
| `max_guests` | int | Maximum number of guests | `4` |
| `bedrooms` | int | Number of bedrooms | `2` |
| `beds` | int | Number of beds | `2` |
| `baths` | float | Number of bathrooms (can be decimal) | `1.5` |
| `lat` | float | Latitude coordinate | `40.7128` |
| `lng` | float | Longitude coordinate | `-74.0060` |

### Feature Importance

The model considers these features with the following importance:
1. **Longitude (lng)** - 31.5%
2. **Price** - 26.6%
3. **Latitude (lat)** - 22.4%
4. **Max Guests** - 6.9%
5. **Room Type** - 3.4%
6. **Listing Type** - 3.1%
7. **Beds** - 2.7%
8. **Bathrooms** - 2.3%
9. **Bedrooms** - 0.9%

---

## Output Categories

Predictions are binned into four occupancy categories:

| Category | Range | Description |
|----------|-------|-------------|
| Low | 0-40% | Below average occupancy |
| Medium | 40-60% | Average occupancy |
| High | 60-80% | Above average occupancy |
| Very High | 80-100% | Excellent occupancy |

---

## Model Files

The following files are required for predictions (located in `models/` directory):

| File | Description |
|------|-------------|
| `random_forest_pca_only.pkl` | Trained Random Forest model |
| `pca_transformer.pkl` | PCA dimensionality reduction (9→5 features) |
| `preprocessor_pca_only.pkl` | Feature preprocessing pipeline |

### Regenerating the Model

If you need to retrain the model:

```bash
python save_best_model.py
```

This will:
1. Load all 256 listings from `listings-sanitized/`
2. Preprocess features
3. Apply PCA (reducing to 5 components, 96.74% variance)
4. Train Random Forest (200 trees)
5. Save all model files

---

## Technical Details

### Model Architecture
- **Algorithm:** Random Forest Regressor
- **Trees:** 200
- **Max Depth:** 15
- **Min Samples Split:** 3
- **Min Samples Leaf:** 1

### Preprocessing Pipeline
1. **Label Encoding:** Converts categorical features (listing_type, room_type) to integers
2. **Scaling:** StandardScaler normalizes all features
3. **PCA:** Reduces 9 features to 5 principal components
4. **Feature Weighting:** Applies importance-based weights

### Performance Metrics
- **RMSE:** 17.01 (Root Mean Squared Error)
- **MAE:** 13.54 (Mean Absolute Error)
- **R²:** -0.13 (explained variance)
- **Category Accuracy:** 48.08%

---

## Error Handling

Common errors and solutions:

### 1. Model Not Found
```
✗ Error: No trained model found. Please train the model first.
```
**Solution:** Run `python save_best_model.py`

### 2. Unknown Listing Type
```
ValueError: y contains previously unseen labels: 'apartment'
```
**Solution:** Use one of the valid listing types (see list above)

### 3. Missing Features
```
KeyError: 'price'
```
**Solution:** Ensure all required fields are included in your input dictionary

---

## Examples

### Example 1: Luxury Rental
```python
luxury_listing = {
    'listing_type': 'Entire villa',
    'room_type': 'Entire villa',
    'price': 500.0,
    'max_guests': 8,
    'bedrooms': 4,
    'beds': 6,
    'baths': 3.5,
    'lat': 40.7589,
    'lng': -73.9851
}
# Expected: High occupancy (60-80%)
```

### Example 2: Budget Room
```python
budget_room = {
    'listing_type': 'Private room',
    'room_type': 'Private room',
    'price': 45.0,
    'max_guests': 1,
    'bedrooms': 1,
    'beds': 1,
    'baths': 0.5,
    'lat': 40.7282,
    'lng': -73.9942
}
# Expected: Medium occupancy (40-60%)
```

### Example 3: Mid-Range Apartment
```python
mid_range = {
    'listing_type': 'Entire rental unit',
    'room_type': 'Entire rental unit',
    'price': 120.0,
    'max_guests': 3,
    'bedrooms': 1,
    'beds': 2,
    'baths': 1.0,
    'lat': 40.7614,
    'lng': -73.9776
}
# Expected: Medium-High occupancy
```

---

## Integration Guide

### REST API Integration

To integrate with a web application:

```python
from flask import Flask, request, jsonify
from predict_occupancy import predict_occupancy

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    listing_data = request.json
    try:
        occupancy = predict_occupancy(listing_data)
        return jsonify({
            'success': True,
            'occupancy_rate': float(occupancy),
            'category': get_occupancy_category(occupancy)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
```

### JavaScript Integration

```javascript
// Example POST request from frontend
async function predictOccupancy(listingData) {
    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(listingData)
    });
    
    const result = await response.json();
    return result;
}

// Usage
const listing = {
    listing_type: 'Entire rental unit',
    room_type: 'Entire rental unit',
    price: 150.0,
    max_guests: 4,
    bedrooms: 2,
    beds: 2,
    baths: 1.5,
    lat: 40.7128,
    lng: -74.0060
};

const prediction = await predictOccupancy(listing);
console.log(`Predicted: ${prediction.occupancy_rate}%`);
```

---

## Troubleshooting

### Check Model Status
```bash
python -c "from predict_occupancy import load_model; load_model()"
```

### Verify Input Data
```python
from predict_occupancy import predict_occupancy

# Test with known good data
test_listing = {
    'listing_type': 'Entire rental unit',
    'room_type': 'Entire rental unit',
    'price': 100.0,
    'max_guests': 2,
    'bedrooms': 1,
    'beds': 1,
    'baths': 1.0,
    'lat': 40.7128,
    'lng': -74.0060
}

result = predict_occupancy(test_listing)
print(f"Test prediction: {result:.2f}%")
```

---

## Support

For issues or questions:
1. Check that all model files exist in `models/` directory
2. Verify input data matches the expected format
3. Ensure Python 3.12+ is installed
4. Check that all dependencies are installed: `pandas`, `numpy`, `scikit-learn`, `pickle`

---

**Last Updated:** December 11, 2025  
**Model Version:** 1.0  
**Best Model:** Random Forest with PCA Only
