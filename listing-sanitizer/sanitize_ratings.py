from utils import get_sanitized_directory, process_json_files

def process_ratings(data, filename):
    """Remove all rating fields and reviews from sanitized listings."""
    # List of all rating fields to remove
    rating_fields = [
        'rating_overall',
        'rating_cleanliness',
        'rating_accuracy',
        'rating_checkin',
        'rating_communication',
        'rating_location',
        'rating_value'
    ]
    
    # Remove all rating fields
    for field in rating_fields:
        if field in data:
            del data[field]
    
    # Remove reviews field
    if 'reviews' in data:
        del data['reviews']
    
    return data

if __name__ == "__main__":
    dir_to_sanitize = get_sanitized_directory()
    process_json_files(dir_to_sanitize, process_ratings, "Rating and review removal")
