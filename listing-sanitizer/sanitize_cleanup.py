import os
import json

# Directory to sanitize
dir_to_sanitize = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')

def sanitize_dates():
    """Remove unnecessary fields from all JSON files."""
    for filename in os.listdir(dir_to_sanitize):
        if not filename.endswith('.json'):
            continue
            
        file_path = os.path.join(dir_to_sanitize, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Remove the date fields
        fields_to_remove = ['checkin_date', 'checkout_date', 'search_date', 'amenities']
        for field in fields_to_remove:
            if field in data:
                del data[field]
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    sanitize_dates()
    print(f"Removed unnecessary fields from all files in {dir_to_sanitize}")
