import os
import json

# Common utilities for all sanitization scripts

def get_sanitized_directory():
    """Get the path to the listings-sanitized directory."""
    return os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')

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
            
            # Process the data
            modified_data = process_function(data, filename)
            
            # Write back to file if data was modified
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
