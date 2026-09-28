from utils import get_sanitized_directory, process_json_files

def process_cleanup(data, filename):
    """Remove unnecessary fields from listing data."""
    fields_to_remove = ['checkin_date', 'checkout_date', 'search_date']
    for field in fields_to_remove:
        data.pop(field, None)
    return data

if __name__ == "__main__":
    dir_to_sanitize = get_sanitized_directory()
    process_json_files(dir_to_sanitize, process_cleanup, "Field cleanup")
