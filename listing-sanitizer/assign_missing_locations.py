import os
import json
import random

# Directory containing the original listings
listings_dir = os.path.join(os.path.dirname(__file__), '..', 'listings')

def get_location_bounds():
    """Get the min/max latitude and longitude from existing map bounds."""
    latitudes = []
    longitudes = []
    
    for filename in os.listdir(listings_dir):
        if not filename.endswith('.json'):
            continue
        
        file_path = os.path.join(listings_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check map_idle_bounds
            map_bounds = data.get('map_idle_bounds')
            if map_bounds and isinstance(map_bounds, dict):
                ne = map_bounds.get('ne', {})
                sw = map_bounds.get('sw', {})
                
                if ne.get('lat') and ne.get('lng') and sw.get('lat') and sw.get('lng'):
                    latitudes.extend([ne['lat'], sw['lat']])
                    longitudes.extend([ne['lng'], sw['lng']])
        except Exception:
            pass
    
    if not latitudes or not longitudes:
        # Default to Islamabad area if no locations found
        return 33.53, 33.57, 73.07, 73.18
    
    return min(latitudes), max(latitudes), min(longitudes), max(longitudes)


def generate_random_location_data(min_lat, max_lat, min_lng, max_lng):
    """Generate random location data in the proper format with bounds."""
    # Generate random center point within bounds
    center_lat = random.uniform(min_lat, max_lat)
    center_lng = random.uniform(min_lng, max_lng)
    
    # Create bounds around the center point
    # Typical bounds span about 0.035 degrees (roughly 4km)
    lat_offset = random.uniform(0.015, 0.020)
    lng_offset = random.uniform(0.020, 0.025)
    
    ne_lat = center_lat + lat_offset
    ne_lng = center_lng + lng_offset
    sw_lat = center_lat - lat_offset
    sw_lng = center_lng - lng_offset
    
    # Ensure bounds stay within overall limits
    ne_lat = min(ne_lat, max_lat)
    ne_lng = min(ne_lng, max_lng)
    sw_lat = max(sw_lat, min_lat)
    sw_lng = max(sw_lng, min_lng)
    
    return {
        "map_init_center": {
            "lat": round(center_lat, 5),
            "lng": round(center_lng, 5)
        },
        "map_idle_center": {
            "lat": round(center_lat, 5),
            "lng": round(center_lng, 5)
        },
        "map_idle_bounds": {
            "ne": {
                "lat": round(ne_lat, 5),
                "lng": round(ne_lng, 5)
            },
            "sw": {
                "lat": round(sw_lat, 5),
                "lng": round(sw_lng, 5)
            }
        }
    }

def assign_missing_locations():
    """Assign locations to listings with missing location data."""
    # Get bounds from existing locations
    min_lat, max_lat, min_lng, max_lng = get_location_bounds()
    print(f"Location bounds:")
    print(f"  Latitude: {min_lat:.5f} to {max_lat:.5f}")
    print(f"  Longitude: {min_lng:.5f} to {max_lng:.5f}\n")
    
    # Load all listings and find missing ones
    missing_location_listings = []
    
    for filename in os.listdir(listings_dir):
        if not filename.endswith('.json'):
            continue
        
        file_path = os.path.join(listings_dir, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if any map location fields are missing
            has_map_init = data.get('map_init_center') is not None
            has_map_idle = data.get('map_idle_center') is not None
            has_map_bounds = data.get('map_idle_bounds') is not None
            
            if not (has_map_init and has_map_idle and has_map_bounds):
                missing_location_listings.append({
                    'filename': filename,
                    'filepath': file_path,
                    'data': data
                })
        except Exception as e:
            print(f"Error reading {filename}: {str(e)}")
    
    print(f"Found {len(missing_location_listings)} listings with missing location data\n")
    
    # Assign random locations within bounds
    assigned_count = 0
    
    for item in missing_location_listings:
        data = item['data']
        
        # Generate random location data
        location_data = generate_random_location_data(min_lat, max_lat, min_lng, max_lng)
        
        # Update the listing with all three map fields
        data['map_init_center'] = location_data['map_init_center']
        data['map_idle_center'] = location_data['map_idle_center']
        data['map_idle_bounds'] = location_data['map_idle_bounds']
        
        # Write back to file
        with open(item['filepath'], 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        assigned_count += 1
        center = location_data['map_init_center']
        print(f"Assigned location to {item['filename']}: ({center['lat']}, {center['lng']})")
    
    print(f"\n✓ Successfully assigned locations to {assigned_count} listings")


if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    assign_missing_locations()