import os
import json
import pandas as pd
import numpy as np

def load_listings_from_json(listings_dir):
    """Load all JSON listings and convert to pandas DataFrame."""
    listings_data = []
    
    for filename in os.listdir(listings_dir):
        if not filename.endswith('.json'):
            continue
        
        file_path = os.path.join(listings_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract flat features
            listing = {
                'id': data.get('id'),
                'listing_type': data.get('listing_type'),
                'room_type': data.get('room_type'),
                'price': data.get('price'),
                'max_guests': data.get('max_guests'),
                'bedrooms': data.get('bedrooms'),
                'beds': data.get('beds'),
                'baths': data.get('baths'),
                'occ_rate': data.get('occ_rate'),
            }
            
            # Extract location
            location = data.get('location', {})
            if location:
                listing['lat'] = location.get('lat')
                listing['lng'] = location.get('lng')
            else:
                listing['lat'] = None
                listing['lng'] = None
            
            listings_data.append(listing)
        
        except Exception as e:
            print(f"Error loading {filename}: {str(e)}")
    
    df = pd.DataFrame(listings_data)
    return df

def save_to_csv(df, output_path):
    """Save DataFrame to CSV file."""
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} listings to {output_path}")

if __name__ == "__main__":
    # Load listings
    listings_dir = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')
    df = load_listings_from_json(listings_dir)
    
    # Save to CSV
    output_path = os.path.join(os.path.dirname(__file__), 'listings_data.csv')
    save_to_csv(df, output_path)
    
    # Display basic info
    print(f"\nDataset shape: {df.shape}")
    print(f"\nColumn types:\n{df.dtypes}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nBasic statistics:\n{df.describe()}")
