import os
import shutil

def copy_listings():
    """Copy all files from listings to listings-sanitized directory."""
    source_dir = os.path.join(os.path.dirname(__file__), '..', 'listings')
    dest_dir = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')
    
    # Clean destination directory (remove all existing files)
    if os.path.exists(dest_dir):
        for filename in os.listdir(dest_dir):
            file_path = os.path.join(dest_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        os.makedirs(dest_dir, exist_ok=True)
    
    # Copy all files from source to destination
    copied_count = 0
    for filename in os.listdir(source_dir):
        src_file = os.path.join(source_dir, filename)
        dst_file = os.path.join(dest_dir, filename)
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dst_file)
            copied_count += 1
    
    print(f"Copied {copied_count} files from {source_dir} to {dest_dir}")

if __name__ == "__main__":
    copy_listings()
