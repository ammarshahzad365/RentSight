import subprocess
import sys
import os

# Get the directory of this script
base_dir = os.path.dirname(__file__)

# Paths to the scripts
copy_script = os.path.join(base_dir, 'copy_listings.py')
sanitize_script = os.path.join(base_dir, 'sanitize_prices.py')
sanitize_reviews_script = os.path.join(base_dir, 'sanitize_reviews.py')
sanitize_url_script = os.path.join(base_dir, 'sanitize_url.py')
sanitize_location_script = os.path.join(base_dir, 'sanitize_location.py')
sanitize_cleanup_script = os.path.join(base_dir, 'sanitize_cleanup.py')
validate_fields_script = os.path.join(base_dir, 'validate_fields.py')

if __name__ == "__main__":
    # Run copy_listings.py
    print("Copying listings...")
    result1 = subprocess.run([sys.executable, copy_script], capture_output=True, text=True)
    print(result1.stdout)
    if result1.returncode != 0:
        print("Error copying listings:", result1.stderr)
        sys.exit(1)

    # Run sanitize_prices.py
    print("Sanitizing prices...")
    result2 = subprocess.run([sys.executable, sanitize_script], capture_output=True, text=True)
    print(result2.stdout)
    if result2.returncode != 0:
        print("Error sanitizing prices:", result2.stderr)
        sys.exit(1)

    # Run sanitize_reviews.py
    print("Sanitizing reviews...")
    result3 = subprocess.run([sys.executable, sanitize_reviews_script], capture_output=True, text=True)
    print(result3.stdout)
    if result3.returncode != 0:
        print("Error sanitizing reviews:", result3.stderr)
        sys.exit(1)

    # Run sanitize_url.py
    print("Sanitizing URLs...")
    result4 = subprocess.run([sys.executable, sanitize_url_script], capture_output=True, text=True)
    print(result4.stdout)
    if result4.returncode != 0:
        print("Error sanitizing URLs:", result4.stderr)
        sys.exit(1)

    # Run sanitize_location.py
    print("Sanitizing location data...")
    result5 = subprocess.run([sys.executable, sanitize_location_script], capture_output=True, text=True)
    print(result5.stdout)
    if result5.returncode != 0:
        print("Error sanitizing location data:", result5.stderr)
        sys.exit(1)

    # Run sanitize_cleanup.py
    print("Final cleanup...")
    result6 = subprocess.run([sys.executable, sanitize_cleanup_script], capture_output=True, text=True)
    print(result6.stdout)
    if result6.returncode != 0:
        print("Error during final cleanup:", result6.stderr)
        sys.exit(1)

    # Run validate_fields.py
    print("Validating required fields...")
    result7 = subprocess.run([sys.executable, validate_fields_script], capture_output=True, text=True)
    print(result7.stdout)
    if result7.returncode != 0:
        print("Error during field validation:", result7.stderr)
        sys.exit(1)

    print("Done.")
