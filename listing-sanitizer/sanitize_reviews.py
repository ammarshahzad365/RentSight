import os
import json
import re
from datetime import datetime, timedelta

# Directory to sanitize
dir_to_sanitize = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')

def extract_rating(metadata):
    """Extract rating from metadata string."""
    match = re.search(r'Rating, (\d+) stars?', metadata)
    if match:
        return int(match.group(1))
    return None

def extract_review_time(metadata):
    """Extract and convert review time to MM/YYYY format."""
    current_date = datetime(2025, 8, 13)  # Based on current date from context
    
    # Check for relative time patterns
    weeks_match = re.search(r'(\d+) weeks? ago', metadata)
    if weeks_match:
        weeks_ago = int(weeks_match.group(1))
        review_date = current_date - timedelta(weeks=weeks_ago)
        return review_date.strftime("%m/%Y")
    
    # Check for "month year" pattern
    month_year_match = re.search(r'([A-Za-z]+) (\d{4})', metadata)
    if month_year_match:
        month_name = month_year_match.group(1)
        year = month_year_match.group(2)
        
        # Convert month name to number
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
    # Look for stay duration patterns at the end
    stay_patterns = [
        r'Stayed (one night|a few nights|about a week|over a week|with kids)',
        r'Stayed (one night|a few nights|about a week|over a week)'
    ]
    
    for pattern in stay_patterns:
        match = re.search(pattern, metadata)
        if match:
            return match.group(1)
    
    return None

def sanitize_reviews():
    """Sanitize reviews in all JSON files."""
    for filename in os.listdir(dir_to_sanitize):
        if not filename.endswith('.json'):
            continue
            
        file_path = os.path.join(dir_to_sanitize, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Sanitize reviews if they exist
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
                elif isinstance(review, dict) and 'text' in review and 'review_id' not in review:
                    # Handle reviews that only have text (no metadata)
                    continue
            
            data['reviews'] = sanitized_reviews
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    sanitize_reviews()
    print(f"Sanitized reviews in all files in {dir_to_sanitize}")
