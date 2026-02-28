"""
Prediction interface for Improved Multi-Modal Ensemble Model
"""

import pickle
import numpy as np
import pandas as pd
from train_improved_model import ImprovedMultiModalEnsemble

def load_ensemble(filepath='models/improved_ensemble.pkl'):
    """Load the trained improved ensemble."""
    return ImprovedMultiModalEnsemble.load(filepath)

def get_occupancy_category(occupancy):
    """Convert occupancy rate to category."""
    if occupancy < 40:
        return "Low (0-40%)"
    elif occupancy < 60:
        return "Medium (40-60%)"
    elif occupancy < 80:
        return "High (60-80%)"
    else:
        return "Very High (80-100%)"

def predict_with_breakdown(listing_data, model_path='models/improved_ensemble.pkl'):
    """
    Make a prediction with detailed breakdown showing each model's contribution.
    
    Args:
        listing_data: Dictionary with keys: listing_type, room_type, max_guests, 
                     price, bedrooms, beds, baths, lat, lng
        model_path: Path to saved ensemble model
    
    Returns:
        Dictionary with final prediction and breakdown by model
    """
    # Load ensemble
    ensemble = load_ensemble(model_path)
    
    # Prepare input data as DataFrame
    input_df = pd.DataFrame([listing_data])
    
    # Get predictions with breakdown
    final_pred, base_predictions = ensemble.predict(input_df)
    
    # Get meta-model weights
    weights = ensemble.meta_model.coef_
    intercept = ensemble.meta_model.intercept_
    
    # Calculate price penalty info
    price = listing_data['price']
    median_price = 30.81
    
    if price <= median_price * 2:
        penalty_info = "No penalty (price within normal range)"
    elif price <= median_price * 5:
        penalty_pct = (1 - (0.7 + 0.3 * (1 - (price - median_price * 2) / (median_price * 3)))) * 100
        penalty_info = f"Moderate penalty applied: ~{penalty_pct:.0f}% reduction"
    elif price <= median_price * 10:
        penalty_pct = (1 - (0.4 + 0.3 * (1 - (price - median_price * 5) / (median_price * 5)))) * 100
        penalty_info = f"High penalty applied: ~{penalty_pct:.0f}% reduction"
    else:
        penalty_pct = (1 - max(0.2, 0.4 - 0.2 * min(1, (price - median_price * 10) / (median_price * 100)))) * 100
        penalty_info = f"Severe penalty applied: ~{penalty_pct:.0f}% reduction"
    
    result = {
        'final_prediction': float(final_pred[0]),
        'category': get_occupancy_category(final_pred[0]),
        'price_penalty': penalty_info,
        'breakdown': {
            'location_model_knn': {
                'prediction': float(base_predictions['location'][0]),
                'weight': float(weights[0]),
                'contribution': float(weights[0] * base_predictions['location'][0])
            },
            'property_model_gb': {
                'prediction': float(base_predictions['property'][0]),
                'weight': float(weights[1]),
                'contribution': float(weights[1] * base_predictions['property'][0])
            },
            'guest_model_rf': {
                'prediction': float(base_predictions['guest'][0]),
                'weight': float(weights[2]),
                'contribution': float(weights[2] * base_predictions['guest'][0])
            },
            'price_model_gb': {
                'prediction': float(base_predictions['price'][0]),
                'weight': float(weights[3]),
                'contribution': float(weights[3] * base_predictions['price'][0])
            },
            'intercept': {
                'value': float(intercept),
                'contribution': float(intercept)
            }
        }
    }
    
    return result


def example_prediction():
    """Run an example prediction."""
    print("\n" + "=" * 80)
    print("IMPROVED MODEL - EXAMPLE PREDICTIONS")
    print("=" * 80)
    
    # Example listing
    listing = {
        'listing_type': 'Entire rental unit',
        'room_type': 'Entire rental unit',
        'max_guests': 4,
        'price': 35,
        'bedrooms': 2,
        'beds': 2,
        'baths': 1,
        'lat': 33.7,
        'lng': 73.05
    }
    
    print("\n📍 Input Listing:")
    for key, value in listing.items():
        print(f"   {key:15}: {value}")
    
    # Test with different prices
    test_prices = [30, 50, 100, 200, 500, 1000, 5000, 150000]
    
    print("\n" + "=" * 80)
    print("PRICE SENSITIVITY ANALYSIS")
    print("=" * 80)
    print(f"\n{'Price ($)':>12} | {'Predicted Occ (%)':>18} | {'Category':>20} | {'Penalty':>30}")
    print("-" * 90)
    
    for price in test_prices:
        listing['price'] = price
        result = predict_with_breakdown(listing)
        
        # Shorten penalty message for table
        penalty_short = result['price_penalty'].split(':')[0] if ':' in result['price_penalty'] else result['price_penalty']
        
        print(f"${price:>10,.0f} | {result['final_prediction']:>16.2f}% | {result['category']:>20} | {penalty_short:>30}")
    
    print("-" * 90)
    
    print("\n💡 As expected, high prices result in lower occupancy predictions!")
    

if __name__ == '__main__':
    example_prediction()
