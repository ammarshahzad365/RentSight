import os
import json
from utils import get_sanitized_directory

# Required fields for the project
REQUIRED_FIELDS = [
    'id', 'title', 'listing_type', 'room_type', 'price', 'max_guests',
    'bedrooms', 'beds', 'baths', 'rating_overall', 'rating_cleanliness',
    'rating_accuracy', 'rating_checkin', 'rating_communication',
    'rating_location', 'rating_value', 'reviews', 'url', 'location'
]

def check_field_value(data, field, listing_id, filename):
    """Check if a specific field has a valid value."""
    if field not in data or data[field] is None:
        return f"{listing_id} - {filename}"
    
    if field == 'location' and isinstance(data[field], dict):
        # Special check for location - ensure it has lat and lng
        if 'lat' not in data[field] or 'lng' not in data[field] or \
           data[field]['lat'] is None or data[field]['lng'] is None:
            return f"{listing_id} - {filename}"
    elif field == 'reviews' and isinstance(data[field], list):
        # Check if reviews array is empty
        if len(data[field]) == 0:
            return f"{listing_id} - {filename}"
    
    return None

def process_json_file(file_path, filename, required_fields, null_field_entries):
    """Process a single JSON file and check for missing fields."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get the ID for identification
        listing_id = data.get('id', 'Unknown')
        
        # Check each required field
        for field in required_fields:
            missing_entry = check_field_value(data, field, listing_id, filename)
            if missing_entry:
                null_field_entries[field].append(missing_entry)
    
    except json.JSONDecodeError:
        print(f"Error reading JSON file: {filename}")
    except Exception as e:
        print(f"Error processing file {filename}: {str(e)}")

def generate_report(null_field_entries, required_fields):
    """Generate the validation report file."""
    report_file = os.path.join(os.path.dirname(__file__), 'missing_fields_report.txt')
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("MISSING FIELDS VALIDATION REPORT\n")
        f.write("=" * 50 + "\n\n")
        
        total_missing = 0
        
        for field in required_fields:
            missing_count = len(null_field_entries[field])
            total_missing += missing_count
            
            f.write(f"Field: {field}\n")
            f.write(f"Missing in {missing_count} listings\n")
            
            if missing_count > 0:
                f.write("Affected listings (ID - Filename):\n")
                for entry in null_field_entries[field]:
                    f.write(f"  - {entry}\n")
            else:
                f.write("No missing values found.\n")
            
            f.write("\n" + "-" * 30 + "\n\n")
        
        f.write("SUMMARY:\n")
        f.write(f"Total missing field instances: {total_missing}\n")
        f.write(f"Fields with missing values: {sum(1 for field in required_fields if len(null_field_entries[field]) > 0)}\n")
    
    return total_missing

def validate_required_fields():
    """Check for null values in required fields and generate a report."""
    
    # Dictionary to store null field entries
    null_field_entries = {field: [] for field in REQUIRED_FIELDS}
    
    # Process each JSON file
    dir_to_validate = get_sanitized_directory()
    for filename in os.listdir(dir_to_validate):
        if not filename.endswith('.json'):
            continue
            
        file_path = os.path.join(dir_to_validate, filename)
        process_json_file(file_path, filename, REQUIRED_FIELDS, null_field_entries)
    
    # Generate the validation report
    total_missing = generate_report(null_field_entries, REQUIRED_FIELDS)
    
    print("Validation report generated: missing_fields_report.txt")
    print(f"Total missing field instances found: {total_missing}")
    
    # Print summary to console
    for field in REQUIRED_FIELDS:
        missing_count = len(null_field_entries[field])
        if missing_count > 0:
            print(f"  - {field}: {missing_count} missing")

if __name__ == "__main__":
    validate_required_fields()
