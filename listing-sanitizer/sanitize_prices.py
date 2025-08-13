import os
import json
import re


# Directory to sanitize
dir_to_sanitize = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')
os.makedirs(dir_to_sanitize, exist_ok=True)

def extract_price(price_str):
    """
    Extracts the per night price as a float from a string like '2 nights x $30.50\n$61.00'.
    Returns None if not found.
    """
    match = re.search(r'\$([0-9]+\.?[0-9]*)', price_str)
    if match:
        return float(match.group(1))
    try:
        return float(price_str)
    except Exception:
        return None

def sanitize_listings():
    for filename in os.listdir(dir_to_sanitize):
        file_path = os.path.join(dir_to_sanitize, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Sanitize price
            if 'price' in data:
                price_val = extract_price(str(data['price']))
                if price_val is not None:
                    data['price'] = price_val
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    sanitize_listings()
    print(f"Sanitized all prices in files in {dir_to_sanitize}")
