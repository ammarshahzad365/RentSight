import os
import json
from utils import get_sanitized_directory

# Directory containing the sanitized listings
listings_dir = get_sanitized_directory()

def calculate_averages():
    """Calculate average values for bedrooms, beds, baths, and max_guests."""
    bedrooms_values = []
    beds_values = []
    baths_values = []
    max_guests_values = []
    
    for filename in os.listdir(listings_dir):
        if not filename.endswith('.json'):
            continue
        
        file_path = os.path.join(listings_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Collect non-null values
            if data.get('bedrooms') is not None:
                bedrooms_values.append(data['bedrooms'])
            if data.get('beds') is not None:
                beds_values.append(data['beds'])
            if data.get('baths') is not None:
                baths_values.append(data['baths'])
            if data.get('max_guests') is not None:
                max_guests_values.append(data['max_guests'])
        
        except Exception as e:
            print(f"Error reading file {filename}: {str(e)}")
    
    # Calculate averages and round to nearest integer
    avg_bedrooms = round(sum(bedrooms_values) / len(bedrooms_values)) if bedrooms_values else 1
    avg_beds = round(sum(beds_values) / len(beds_values)) if beds_values else 1
    avg_baths = round(sum(baths_values) / len(baths_values)) if baths_values else 1
    avg_max_guests = round(sum(max_guests_values) / len(max_guests_values)) if max_guests_values else 2
    
    print(f"Calculated averages:")
    print(f"  Bedrooms: {avg_bedrooms} (from {len(bedrooms_values)} non-null values)")
    print(f"  Beds: {avg_beds} (from {len(beds_values)} non-null values)")
    print(f"  Baths: {avg_baths} (from {len(baths_values)} non-null values)")
    print(f"  Max Guests: {avg_max_guests} (from {len(max_guests_values)} non-null values)")
    
    return avg_bedrooms, avg_beds, avg_baths, avg_max_guests

def fill_missing_values():
    """Fill missing values for bedrooms, beds, baths, and max_guests with averages."""
    # Calculate averages first
    avg_bedrooms, avg_beds, avg_baths, avg_max_guests = calculate_averages()
    
    filled_count = {'bedrooms': 0, 'beds': 0, 'baths': 0, 'max_guests': 0}
    processed_files = 0
    
    for filename in os.listdir(listings_dir):
        if not filename.endswith('.json'):
            continue
        
        file_path = os.path.join(listings_dir, filename)
        modified = False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Fill missing values
            if data.get('bedrooms') is None:
                data['bedrooms'] = float(avg_bedrooms)
                filled_count['bedrooms'] += 1
                modified = True
            
            if data.get('beds') is None:
                data['beds'] = float(avg_beds)
                filled_count['beds'] += 1
                modified = True
            
            if data.get('baths') is None:
                data['baths'] = float(avg_baths)
                filled_count['baths'] += 1
                modified = True
            
            if data.get('max_guests') is None:
                data['max_guests'] = float(avg_max_guests)
                filled_count['max_guests'] += 1
                modified = True
            
            # Write back only if modified
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                processed_files += 1
        
        except Exception as e:
            print(f"Error processing file {filename}: {str(e)}")
    
    print(f"\nFilled missing values:")
    print(f"  Bedrooms: {filled_count['bedrooms']} listings")
    print(f"  Beds: {filled_count['beds']} listings")
    print(f"  Baths: {filled_count['baths']} listings")
    print(f"  Max Guests: {filled_count['max_guests']} listings")
    print(f"\nTotal files modified: {processed_files}")

if __name__ == "__main__":
    fill_missing_values()