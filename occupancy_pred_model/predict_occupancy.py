"""
Predict Occupancy Rate using the best trained model (Random Forest with PCA).
This script allows you to input listing features and get occupancy rate predictions.
"""

import pickle
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

def load_model():
    """Load the trained Random Forest model with PCA."""
    try:
        # Try to load the PCA-specific model first
        with open('models/random_forest_pca_only.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('models/preprocessor_pca_only.pkl', 'rb') as f:
            preprocessor = pickle.load(f)
        print("✓ Loaded Random Forest with PCA model")
        return model, preprocessor, True
    except FileNotFoundError:
        # Fall back to regular model
        try:
            with open('models/occupancy_model.pkl', 'rb') as f:
                model = pickle.load(f)
            with open('models/preprocessor.pkl', 'rb') as f:
                preprocessor = pickle.load(f)
            print("✓ Loaded default Random Forest model")
            return model, preprocessor, False
        except FileNotFoundError:
            print("✗ Error: No trained model found. Please train the model first.")
            return None, None, False

def predict_occupancy(listing_data, model=None, preprocessor=None, use_pca=False):
    """
    Predict occupancy rate for a given listing.
    
    Parameters:
    -----------
    listing_data : dict
        Dictionary containing listing features:
        - listing_type: str ('Entire rental unit', 'Private room in rental unit', 'Shared room in rental unit', etc.)
        - room_type: str (same as listing_type)
        - price: float (nightly price)
        - max_guests: int (maximum number of guests)
        - bedrooms: int (number of bedrooms)
        - beds: int (number of beds)
        - baths: float (number of bathrooms)
        - lat: float (latitude)
        - lng: float (longitude)
    
    Returns:
    --------
    float : Predicted occupancy rate (0-100)
    """
    # Load model if not provided
    if model is None or preprocessor is None:
        model, preprocessor, use_pca = load_model()
        if model is None:
            return None
    
    # Create DataFrame from input
    df = pd.DataFrame([listing_data])
    
    # Preprocess the data
    X_processed = preprocessor.transform(df)
    
    # Apply PCA if the model uses it
    if use_pca:
        # Load or create PCA transformer
        try:
            with open('models/pca_transformer.pkl', 'rb') as f:
                pca = pickle.load(f)
            X_processed = pca.transform(X_processed)
        except FileNotFoundError:
            # If PCA transformer not saved separately, create it
            # This should match the training configuration (5 components for 95% variance)
            pca = PCA(n_components=5)
            # Note: In production, PCA should be fitted during training and saved
            print("⚠ Warning: PCA transformer not found. Using model without PCA.")
    
    # Make prediction
    occupancy_rate = model.predict(X_processed)[0]
    
    # Ensure the prediction is within valid range
    occupancy_rate = np.clip(occupancy_rate, 0, 100)
    
    return occupancy_rate

def get_occupancy_category(occupancy_rate):
    """Categorize occupancy rate into bins."""
    if occupancy_rate < 40:
        return "Low (0-40%)"
    elif occupancy_rate < 60:
        return "Medium (40-60%)"
    elif occupancy_rate < 80:
        return "High (60-80%)"
    else:
        return "Very High (80-100%)"

def predict_from_user_input():
    """Interactive function to get user input and predict occupancy."""
    print("\n" + "="*60)
    print("OCCUPANCY RATE PREDICTOR")
    print("="*60)
    
    # Load model once
    model, preprocessor, use_pca = load_model()
    if model is None:
        return
    
    print("\nEnter listing details:")
    print("-" * 60)
    
    try:
        # Get user input
        listing_type = input("Listing Type (Entire rental unit/Private room in rental unit/Shared room in rental unit): ").strip()
        room_type = listing_type  # Usually the same
        price = float(input("Price per night ($): "))
        max_guests = int(input("Maximum guests: "))
        bedrooms = int(input("Number of bedrooms: "))
        beds = int(input("Number of beds: "))
        baths = float(input("Number of bathrooms: "))
        lat = float(input("Latitude: "))
        lng = float(input("Longitude: "))
        
        # Create listing data
        listing_data = {
            'listing_type': listing_type,
            'room_type': room_type,
            'price': price,
            'max_guests': max_guests,
            'bedrooms': bedrooms,
            'beds': beds,
            'baths': baths,
            'lat': lat,
            'lng': lng
        }
        
        # Predict
        occupancy = predict_occupancy(listing_data, model, preprocessor, use_pca)
        
        if occupancy is not None:
            category = get_occupancy_category(occupancy)
            
            print("\n" + "="*60)
            print("PREDICTION RESULT")
            print("="*60)
            print(f"Predicted Occupancy Rate: {occupancy:.2f}%")
            print(f"Category: {category}")
            print("="*60)
        
    except ValueError as e:
        print(f"\n✗ Error: Invalid input. {str(e)}")
    except KeyboardInterrupt:
        print("\n\nPrediction cancelled.")

def predict_batch(listings):
    """
    Predict occupancy for multiple listings.
    
    Parameters:
    -----------
    listings : list of dict
        List of listing dictionaries with the same structure as predict_occupancy
    
    Returns:
    --------
    list : List of predicted occupancy rates
    """
    model, preprocessor, use_pca = load_model()
    if model is None:
        return None
    
    predictions = []
    for i, listing_data in enumerate(listings):
        try:
            occupancy = predict_occupancy(listing_data, model, preprocessor, use_pca)
            predictions.append({
                'listing_id': i + 1,
                'occupancy_rate': occupancy,
                'category': get_occupancy_category(occupancy)
            })
        except Exception as e:
            print(f"✗ Error predicting listing {i+1}: {str(e)}")
            predictions.append({
                'listing_id': i + 1,
                'occupancy_rate': None,
                'category': None,
                'error': str(e)
            })
    
    return predictions

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--example':
        # Example prediction with sample data
        print("\n" + "="*60)
        print("EXAMPLE PREDICTION")
        print("="*60)
        
        sample_listing = {
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
        
        print("\nSample Listing:")
        for key, value in sample_listing.items():
            print(f"  {key}: {value}")
        
        occupancy = predict_occupancy(sample_listing)
        
        if occupancy is not None:
            category = get_occupancy_category(occupancy)
            print(f"\nPredicted Occupancy Rate: {occupancy:.2f}%")
            print(f"Category: {category}")
        
    elif len(sys.argv) > 1 and sys.argv[1] == '--batch':
        # Example batch prediction
        print("\n" + "="*60)
        print("BATCH PREDICTION EXAMPLE")
        print("="*60)
        
        sample_listings = [
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
            },
            {
                'listing_type': 'Entire rental unit',
                'room_type': 'Entire rental unit',
                'price': 250.0,
                'max_guests': 6,
                'bedrooms': 3,
                'beds': 4,
                'baths': 2.0,
                'lat': 40.7489,
                'lng': -73.9680
            }
        ]
        
        predictions = predict_batch(sample_listings)
        
        print("\nPredictions:")
        print("-" * 60)
        for pred in predictions:
            if pred['occupancy_rate'] is not None:
                print(f"Listing {pred['listing_id']}: {pred['occupancy_rate']:.2f}% - {pred['category']}")
            else:
                print(f"Listing {pred['listing_id']}: Error - {pred.get('error', 'Unknown')}")
    
    else:
        # Interactive mode
        predict_from_user_input()
        
        # Ask if user wants to predict another
        while True:
            another = input("\nPredict another listing? (y/n): ").strip().lower()
            if another == 'y':
                predict_from_user_input()
            else:
                print("\nThank you for using the Occupancy Rate Predictor!")
                break
