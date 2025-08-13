import os
import shutil

# Define source and destination directories
source_dir = os.path.join(os.path.dirname(__file__), '..', 'listings')
dest_dir = os.path.join(os.path.dirname(__file__), '..', 'listings-sanitized')

# Create destination directory if it doesn't exist
os.makedirs(dest_dir, exist_ok=True)

# Copy all files from source to destination
def copy_listings():
    for filename in os.listdir(source_dir):
        src_file = os.path.join(source_dir, filename)
        dst_file = os.path.join(dest_dir, filename)
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dst_file)

if __name__ == "__main__":
    copy_listings()
    print(f"Copied all files from {source_dir} to {dest_dir}")
