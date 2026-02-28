# Occupancy Rate Prediction Model

This module trains machine learning models to predict the occupancy rate of Airbnb listings based on their features.

## Features Used
- `listing_type`: Type of listing (Entire home, Private room, etc.)
- `room_type`: Room type
- `price`: Nightly price
- `max_guests`: Maximum number of guests
- `bedrooms`: Number of bedrooms
- `beds`: Number of beds
- `baths`: Number of bathrooms
- `lat`, `lng`: Geographic coordinates

## Models Implemented
1. **Random Forest Regressor** (Default/Best)
2. **Gradient Boosting Regressor**
3. **Ridge Regression**
4. **Lasso Regression**

## Usage

### 1. Prepare Data
```bash
python data_loader.py
```
Converts JSON listings to CSV format (`listings_data.csv`)

### 2. Train Models
```bash
python train_model.py
```
- Trains and compares all models
- Saves best model to `best_model.pkl`
- Saves preprocessor to `preprocessor.pkl`
- Generates prediction plot and feature importance plot

### 3. Make Predictions
```python
from predict import predict_occupancy

# Single prediction
listing = {
    'listing_type': 'Entire home',
    'room_type': 'Entire home',
    'price': 50.0,
    'max_guests': 4.0,
    'bedrooms': 2.0,
    'beds': 2.0,
    'baths': 1.5,
    'lat': 33.6,
    'lng': 73.1
}

predicted_rate = predict_occupancy(listing)
print(f"Predicted Occupancy Rate: {predicted_rate:.2f}%")
```

## Data Split
- Training: 80% (205 listings)
- Testing: 20% (51 listings)

## Evaluation Metrics
- **RMSE**: Root Mean Squared Error
- **MAE**: Mean Absolute Error
- **R²**: Coefficient of Determination
- **MAPE**: Mean Absolute Percentage Error

## Files
- `data_loader.py`: Load and convert JSON to CSV
- `preprocess.py`: Data preprocessing and feature engineering
- `train_model.py`: Model training and evaluation
- `predict.py`: Make predictions on new data
- `listings_data.csv`: Processed data (generated)
- `best_model.pkl`: Trained model (generated)
- `preprocessor.pkl`: Fitted preprocessor (generated)
