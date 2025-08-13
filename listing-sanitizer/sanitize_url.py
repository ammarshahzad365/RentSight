import os
import json
import re

# Directory to sanitize
dir_to_sanitize = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')

def sanitize_url(url):
    """
    Sanitize URL to keep only the base Airbnb room URL.
    Converts: https://www.airbnb.com/rooms/47114668?adults=1&check_in=2025-10-01...
    To: https://www.airbnb.com/rooms/47114668
    """
    if not url:
        return url
    
    # Extract the base URL before any query parameters
    match = re.match(r'(https://www\.airbnb\.com/rooms/\d+)', url)
    if match:
        return match.group(1)
    
    return url

def sanitize_urls():
    """Sanitize URLs in all JSON files."""
    for filename in os.listdir(dir_to_sanitize):
        if not filename.endswith('.json'):
            continue
            
        file_path = os.path.join(dir_to_sanitize, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Sanitize URL if it exists
        if 'url' in data:
            data['url'] = sanitize_url(data['url'])
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    sanitize_urls()
    print(f"Sanitized URLs in all files in {dir_to_sanitize}")
