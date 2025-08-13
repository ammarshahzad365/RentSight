import os
import json

# Directory to sanitize
dir_to_sanitize = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')

def sanitize_location():
    """Sanitize location data in all JSON files."""
    
    for filename in os.listdir(dir_to_sanitize):
        if not filename.endswith('.json'):
            continue
            
        file_path = os.path.join(dir_to_sanitize, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract location from map_init_center and create new location field
        if 'map_init_center' in data and data['map_init_center'] is not None:
            map_center = data['map_init_center']
            if isinstance(map_center, dict) and 'lat' in map_center and 'lng' in map_center:
                data['location'] = {
                    'lat': map_center['lat'],
                    'lng': map_center['lng']
                }
            else:
                # If map_init_center exists but doesn't have lat/lng, set location to null
                data['location'] = None
        else:
            # If map_init_center doesn't exist or is null, set location to null
            data['location'] = None
        
        # Remove the original map-related fields
        fields_to_remove = ['map_init_center', 'map_idle_center', 'map_idle_bounds']
        for field in fields_to_remove:
            if field in data:
                del data[field]
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    sanitize_location()
    print(f"Sanitized location data in all files in {dir_to_sanitize}")
