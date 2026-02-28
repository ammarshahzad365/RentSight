"""
Simple prediction interface for Occupancy Rate Model
Usage: python predict.py

Edit the listing properties in the code below to get predictions.
"""

import pandas as pd
from train_improved_model import ImprovedMultiModalEnsemble

def get_occupancy_category(occupancy):
    """Convert occupancy rate to category."""
    if occupancy < 40:
        return "Low"
    elif occupancy < 60:
        return "Medium"
    elif occupancy < 80:
        return "High"
    else:
        return "Very High"

def predict_occupancy():
    """Make occupancy prediction with hardcoded listing details."""
    
    # ============================================================
    # EDIT LISTING PROPERTIES HERE
    # ============================================================
    listing_type = 'Entire rental unit'  # Options: 'Entire rental unit', 'Entire home', 'Private room', etc.
    room_type = 'Entire home'           # Options: 'Entire rental unit', 'Entire home', 'Private room', etc.
    max_guests = 6
    price = 150                       # Price per night in dollars
    bedrooms = 2
    beds = 2
    baths = 1
    lat = 33.7                          # Latitude
    lng = 73.05                         # Longitude
    # ============================================================
    
    print("\n" + "="*60)
    print("           AIRBNB OCCUPANCY RATE PREDICTOR")
    print("="*60)
    
    # Load model
    print("\n⏳ Loading model...")
    try:
        model = ImprovedMultiModalEnsemble.load('models/improved_ensemble.pkl')
    except FileNotFoundError:
        print("❌ Error: Model not found. Please train the model first.")
        print("   Run: python train_improved_model.py")
        return
    
    # Prepare data
    listing_data = pd.DataFrame([{
        'listing_type': listing_type,
        'room_type': room_type,
        'max_guests': max_guests,
        'price': price,
        'bedrooms': bedrooms,
        'beds': beds,
        'baths': baths,
        'lat': lat,
        'lng': lng
    }])
    
    # Make prediction
    print("\n⏳ Calculating prediction...")
    prediction, breakdown = model.predict(listing_data)
    predicted_occupancy = prediction[0]
    category = get_occupancy_category(predicted_occupancy)
    
    # Display results
    print("\n" + "="*60)
    print("                    PREDICTION RESULTS")
    print("="*60)
    print(f"\n  📊 Predicted Occupancy Rate: {predicted_occupancy:.1f}%")
    print(f"  📈 Category: {category}")
    print("\n" + "="*60)
    print()

if __name__ == '__main__':
    predict_occupancy()
