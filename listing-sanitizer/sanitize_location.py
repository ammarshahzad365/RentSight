from utils import get_sanitized_directory, process_json_files

def process_location(data, filename):
    """Process location data in listing."""
    # Extract location from map_init_center
    if 'map_init_center' in data and data['map_init_center'] is not None:
        map_center = data['map_init_center']
        if isinstance(map_center, dict) and 'lat' in map_center and 'lng' in map_center:
            data['location'] = {
                'lat': map_center['lat'],
                'lng': map_center['lng']
            }
        else:
            data['location'] = None
    else:
        data['location'] = None
    
    # Remove the original map-related fields
    for field in ['map_init_center', 'map_idle_center', 'map_idle_bounds']:
        data.pop(field, None)
    
    return data

if __name__ == "__main__":
    dir_to_sanitize = get_sanitized_directory()
    process_json_files(dir_to_sanitize, process_location, "Location sanitization")
