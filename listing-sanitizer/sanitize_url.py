import re
from utils import get_sanitized_directory, process_json_files

def sanitize_url(url):
    """Sanitize URL to keep only the base Airbnb room URL."""
    if not url:
        return url
    
    # Extract the base URL before any query parameters
    match = re.match(r'(https://www\.airbnb\.com/rooms/\d+)', url)
    return match.group(1) if match else url

def process_url(data, filename):
    """Process URL field in listing data."""
    if 'url' in data:
        data['url'] = sanitize_url(data['url'])
    return data

if __name__ == "__main__":
    dir_to_sanitize = get_sanitized_directory()
    process_json_files(dir_to_sanitize, process_url, "URL sanitization")
