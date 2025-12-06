import re
from utils import get_sanitized_directory, process_json_files

def extract_price(price_str):
    """Extract per night price from strings like '2 nights x $30.50\n$61.00'."""
    match = re.search(r'\$(\d+\.?\d*)', price_str)
    if match:
        return float(match.group(1))
    try:
        return float(price_str)
    except (ValueError, TypeError):
        return None

def process_price(data, filename):
    """Process price field in listing data."""
    if 'price' in data:
        price_val = extract_price(str(data['price']))
        if price_val is not None:
            data['price'] = price_val
    return data

if __name__ == "__main__":
    dir_to_sanitize = get_sanitized_directory()
    process_json_files(dir_to_sanitize, process_price, "Price sanitization")
