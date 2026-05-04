import os
import json

CITY_ENV_VAR = 'RENTSIGHT_CITY'
DEFAULT_CITY = 'islamabad'
VALID_CITIES = ['islamabad', 'lahore', 'karachi']


def get_city():
    """Get the current city from the RENTSIGHT_CITY environment variable."""
    return os.environ.get(CITY_ENV_VAR, DEFAULT_CITY).lower()


def get_listings_directory(city=None):
    """Get the path to the raw listings directory for a city."""
    if city is None:
        city = get_city()
    return os.path.join(os.path.dirname(__file__), '..', f'listings-{city}')


def get_sanitized_directory(city=None):
    """Get the path to the sanitized listings directory for a city."""
    if city is None:
        city = get_city()
    return os.path.join(os.path.dirname(__file__), '..', f'listings-sanitized-{city}')


def process_json_files(dir_path, process_function, description="Processing"):
    """
    Process all JSON files in a directory with the given function.

    Args:
        dir_path: Directory containing JSON files
        process_function: Function that takes (data, filename) and returns modified data
        description: Description for progress messages
    """
    processed_count = 0

    for filename in os.listdir(dir_path):
        if not filename.endswith('.json'):
            continue

        file_path = os.path.join(dir_path, filename)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            modified_data = process_function(data, filename)

            if modified_data is not None:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(modified_data, f, ensure_ascii=False, indent=2)
                processed_count += 1

        except json.JSONDecodeError:
            print(f"Error reading JSON file: {filename}")
        except Exception as e:
            print(f"Error processing file {filename}: {str(e)}")

    print(f"{description} completed. Processed {processed_count} files.")
    return processed_count
