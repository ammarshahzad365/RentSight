"""
Prediction interface for Multi-Modal Ensemble Model
"""

import pickle
import numpy as np
from train_multimodal_ensemble import MultiModalEnsemble

def load_ensemble(filepath='models/multimodal_ensemble.pkl'):
    """Load the trained multi-modal ensemble."""
    return MultiModalEnsemble.load(filepath)

def predict_with_breakdown(listing_data, model_path='models/multimodal_ensemble.pkl'):
    """
    Make a prediction with detailed breakdown showing each model's contribution.
    
    Args:
        listing_data: Dictionary with keys: listing_type, room_type, max_guests, 
                     price, bedrooms, beds, baths, lat, lng
        model_path: Path to saved ensemble model
    
    Returns:
        Dictionary with final prediction and breakdown by model
    """
    import pandas as pd
    
    # Load ensemble
    ensemble = load_ensemble(model_path)
    
    # Prepare input data as DataFrame
    input_df = pd.DataFrame([listing_data])
    input_processed = ensemble.preprocessor.transform(input_df)
    
    # Get predictions with breakdown
    final_pred, base_predictions = ensemble.predict(input_processed)
    
    # Get meta-model weights
    weights = ensemble.meta_model.coef_
    intercept = ensemble.meta_model.intercept_
    
    result = {
        'final_prediction': float(final_pred[0]),
        'category': get_occupancy_category(final_pred[0]),
        'breakdown': {
            'location_model_knn': {
                'prediction': float(base_predictions['location'][0]),
                'weight': float(weights[0]),
                'contribution': float(weights[0] * base_predictions['location'][0])
            },
            'property_model_rf': {
                'prediction': float(base_predictions['property'][0]),
                'weight': float(weights[1]),
                'contribution': float(weights[1] * base_predictions['property'][0])
            },
            'guest_model_gb': {
                'prediction': float(base_predictions['guest'][0]),
                'weight': float(weights[2]),
                'contribution': float(weights[2] * base_predictions['guest'][0])
            },
            'intercept': float(intercept)
        }
    }
    
    return result

def get_occupancy_category(rate):
    """Categorize occupancy rate into bins."""
    if rate < 40:
        return "Low (0-40%)"
    elif rate < 60:
        return "Medium (40-60%)"
    elif rate < 80:
        return "High (60-80%)"
    else:
        return "Very High (80-100%)"

def predict_interactive():
    """Interactive prediction mode."""
    print("\n" + "="*70)
    print("MULTI-MODAL ENSEMBLE - INTERACTIVE PREDICTION")
    print("="*70)
    
    # Load model
    print("\nLoading multi-modal ensemble...")
    ensemble = load_ensemble()
    
    print("\nEnter listing details:")
    
    listing_data = {
        'listing_type': input("Listing type (e.g., 'Entire rental unit'): "),
        'room_type': input("Room type (e.g., 'Entire home/apt'): "),
        'max_guests': int(input("Max guests: ")),
        'price': float(input("Price per night ($): ")),
        'bedrooms': float(input("Number of bedrooms: ")),
        'beds': float(input("Number of beds: ")),
        'baths': float(input("Number of bathrooms: ")),
        'lat': float(input("Latitude: ")),
        'lng': float(input("Longitude: "))
    }
    
    # Make prediction
    result = predict_with_breakdown(listing_data)
    
    # Display results
    print("\n" + "="*70)
    print("PREDICTION RESULTS")
    print("="*70)
    print(f"\nFinal Prediction: {result['final_prediction']:.2f}%")
    print(f"Category: {result['category']}")
    
    print("\n" + "-"*70)
    print("MODEL CONTRIBUTIONS:")
    print("-"*70)
    
    breakdown = result['breakdown']
    
    print(f"\n1. Location Model (KNN):")
    print(f"   Prediction: {breakdown['location_model_knn']['prediction']:.2f}%")
    print(f"   Weight: {breakdown['location_model_knn']['weight']:.4f}")
    print(f"   Contribution: {breakdown['location_model_knn']['contribution']:.2f}%")
    
    print(f"\n2. Property Model (Random Forest):")
    print(f"   Prediction: {breakdown['property_model_rf']['prediction']:.2f}%")
    print(f"   Weight: {breakdown['property_model_rf']['weight']:.4f}")
    print(f"   Contribution: {breakdown['property_model_rf']['contribution']:.2f}%")
    
    print(f"\n3. Guest Model (Gradient Boosting):")
    print(f"   Prediction: {breakdown['guest_model_gb']['prediction']:.2f}%")
    print(f"   Weight: {breakdown['guest_model_gb']['weight']:.4f}")
    print(f"   Contribution: {breakdown['guest_model_gb']['contribution']:.2f}%")
    
    print(f"\n4. Intercept: {breakdown['intercept']:.2f}%")
    
    total_contribution = (breakdown['location_model_knn']['contribution'] + 
                          breakdown['property_model_rf']['contribution'] + 
                          breakdown['guest_model_gb']['contribution'] + 
                          breakdown['intercept'])
    
    print(f"\nTotal: {total_contribution:.2f}%")
    print("="*70)

def example_prediction():
    """Example prediction with sample data."""
    print("\n" + "="*70)
    print("MULTI-MODAL ENSEMBLE - EXAMPLE PREDICTION")
    print("="*70)
    
    sample_listing = {
        'listing_type': 'Entire rental unit',
        'room_type': 'Entire home',
        'max_guests': 4,
        'price': 15.0,
        'bedrooms': 1,
        'beds': 2,
        'baths': 1.5,
        'lat': 40.7580,
        'lng': -73.9855
    }
    
    print("\nSample Listing:")
    for key, value in sample_listing.items():
        print(f"  {key}: {value}")
    
    result = predict_with_breakdown(sample_listing)
    
    print("\n" + "="*70)
    print("PREDICTION RESULTS")
    print("="*70)
    print(f"\nFinal Prediction: {result['final_prediction']:.2f}%")
    print(f"Category: {result['category']}")
    
    print("\nModel Breakdown:")
    breakdown = result['breakdown']
    print(f"  Location (KNN): {breakdown['location_model_knn']['prediction']:.2f}% × {breakdown['location_model_knn']['weight']:.3f} = {breakdown['location_model_knn']['contribution']:.2f}%")
    print(f"  Property (RF):  {breakdown['property_model_rf']['prediction']:.2f}% × {breakdown['property_model_rf']['weight']:.3f} = {breakdown['property_model_rf']['contribution']:.2f}%")
    print(f"  Guest (GB):     {breakdown['guest_model_gb']['prediction']:.2f}% × {breakdown['guest_model_gb']['weight']:.3f} = {breakdown['guest_model_gb']['contribution']:.2f}%")
    print(f"  Intercept:      {breakdown['intercept']:.2f}%")
    print("="*70)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--example':
        example_prediction()
    else:
        predict_interactive()
