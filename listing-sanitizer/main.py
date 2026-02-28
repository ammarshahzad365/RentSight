import subprocess
import sys
import os

def run_script(script_name, description):
    """Run a script and handle errors."""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    print(f"{description}...")
    
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    print(result.stdout)
    
    if result.returncode != 0:
        print(f"Error during {description.lower()}: {result.stderr}")
        sys.exit(1)

def main():
    """Run the complete sanitization pipeline."""
    pipeline_steps = [
        ('copy_listings.py', 'Copying listings'),
        ('sanitize_prices.py', 'Sanitizing prices'),
        ('sanitize_ratings.py', 'Sanitizing ratings'),
        ('sanitize_reviews.py', 'Sanitizing reviews'),
        ('sanitize_url.py', 'Sanitizing URLs'),
        ('sanitize_location.py', 'Sanitizing location data'),
        ('sanitize_amenities.py', 'Sanitizing amenities'),
        ('sanitize_cleanup.py', 'Final cleanup'),
        ('validate_fields.py', 'Validating required fields')
    ]
    
    for script_name, description in pipeline_steps:
        run_script(script_name, description)
    
    print("✓ Sanitization pipeline completed successfully!")

if __name__ == "__main__":
    main()
