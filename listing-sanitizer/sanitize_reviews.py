import re
from datetime import datetime, timedelta
from utils import get_sanitized_directory, process_json_files

def extract_rating(metadata):
    """Extract rating from metadata string."""
    match = re.search(r'Rating, (\d+) stars?', metadata)
    return int(match.group(1)) if match else None

def extract_review_time(metadata):
    """Extract and convert review time to MM/YYYY format."""
    current_date = datetime(2025, 8, 13)
    
    # Check for relative time patterns
    weeks_match = re.search(r'(\d+) weeks? ago', metadata)
    if weeks_match:
        weeks_ago = int(weeks_match.group(1))
        review_date = current_date - timedelta(weeks=weeks_ago)
        return review_date.strftime("%m/%Y")
    
    # Check for "month year" pattern
    month_year_match = re.search(r'([A-Za-z]+) (\d{4})', metadata)
    if month_year_match:
        month_name, year = month_year_match.groups()
        month_map = {
            'January': '01', 'February': '02', 'March': '03', 'April': '04',
            'May': '05', 'June': '06', 'July': '07', 'August': '08',
            'September': '09', 'October': '10', 'November': '11', 'December': '12'
        }
        month_num = month_map.get(month_name, '01')
        return f"{month_num}/{year}"
    
    return None

def extract_stay_duration(metadata):
    """Extract stay duration from metadata."""
    stay_patterns = [
        r'Stayed (one night|a few nights|about a week|over a week|with kids)',
        r'Stayed (one night|a few nights|about a week|over a week)'
    ]
    
    for pattern in stay_patterns:
        match = re.search(pattern, metadata)
        if match:
            return match.group(1)
    
    return None

def process_reviews(data, filename):
    """Process reviews in listing data."""
    if 'reviews' in data and isinstance(data['reviews'], list):
        sanitized_reviews = []
        
        for review in data['reviews']:
            if isinstance(review, dict) and 'review_id' in review and 'metadata' in review:
                sanitized_review = {
                    'review_id': review['review_id'],
                    'rating': extract_rating(review['metadata']),
                    'review_time': extract_review_time(review['metadata']),
                    'stay_duration': extract_stay_duration(review['metadata'])
                }
                sanitized_reviews.append(sanitized_review)
        
        data['reviews'] = sanitized_reviews
    
    return data

if __name__ == "__main__":
    dir_to_sanitize = get_sanitized_directory()
    process_json_files(dir_to_sanitize, process_reviews, "Review sanitization")
