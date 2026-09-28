import random
from utils import get_sanitized_directory, process_json_files

def parse_search_coords(search_coords_str):
    """Parse search_coords string and return center coordinates with randomization.
    
    Args:
        search_coords_str: String like "ne_lat=33.5700&ne_lng=73.1300&sw_lat=33.5550&sw_lng=73.1150"
    
    Returns:
        Dictionary with lat and lng of the center point (with small random offset), or None if parsing fails
    """
    try:
        params = {}
        for param in search_coords_str.split('&'):
            key, value = param.split('=')
            params[key] = float(value)
        
        # Calculate center point from northeast and southwest corners
        center_lat = (params['ne_lat'] + params['sw_lat']) / 2
        center_lng = (params['ne_lng'] + params['sw_lng']) / 2
        
        # Add random offset of ±0.02 to avoid all listings appearing at the same location
        offset_lat = random.uniform(-0.02, 0.02)
        offset_lng = random.uniform(-0.02, 0.02)
        
        return {
            'lat': center_lat + offset_lat,
            'lng': center_lng + offset_lng
        }
    except (ValueError, KeyError, AttributeError):
        return None

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
    # If map_init_center is not available, try search_coords
    elif 'search_coords' in data and data['search_coords'] is not None:
        if isinstance(data['search_coords'], str):
            data['location'] = parse_search_coords(data['search_coords'])
        else:
            data['location'] = None
    else:
        data['location'] = None
    
    # Remove the original map-related fields
    for field in ['map_init_center', 'map_idle_center', 'map_idle_bounds', 'search_coords']:
        data.pop(field, None)
    
    return data

if __name__ == "__main__":
    dir_to_sanitize = get_sanitized_directory()
    process_json_files(dir_to_sanitize, process_location, "Location sanitization")
