import subprocess
import sys
import os
import argparse

VALID_CITIES = ['islamabad', 'lahore', 'karachi']


def run_script(script_name, description, city):
    """Run a script with the city env var set, and halt on error."""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    print(f"{description}...")

    env = os.environ.copy()
    env['RENTSIGHT_CITY'] = city

    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, env=env)
    print(result.stdout)

    if result.returncode != 0:
        print(f"Error during {description.lower()}: {result.stderr}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Run the complete listing sanitization pipeline for a city.'
    )
    parser.add_argument(
        '--city',
        choices=VALID_CITIES,
        default='islamabad',
        help='City to sanitize listings for (default: islamabad)',
    )
    args = parser.parse_args()
    city = args.city

    print('=' * 55)
    print(f'  Sanitization pipeline — {city.upper()}')
    print('=' * 55)

    pipeline_steps = [
        ('copy_listings.py',    'Copying listings'),
        ('sanitize_prices.py',  'Sanitizing prices'),
        ('sanitize_ratings.py', 'Sanitizing ratings'),
        ('sanitize_reviews.py', 'Sanitizing reviews'),
        ('sanitize_url.py',     'Sanitizing URLs'),
        ('sanitize_location.py','Sanitizing location data'),
        ('sanitize_amenities.py','Sanitizing amenities'),
        ('sanitize_cleanup.py', 'Final cleanup'),
        ('validate_fields.py',  'Validating required fields'),
    ]

    for script_name, description in pipeline_steps:
        run_script(script_name, description, city)

    print(f'\n✓ Sanitization pipeline for {city} completed successfully!')
    print(f'  Next step: python add_occupancy_rate.py --city {city}')


if __name__ == '__main__':
    main()
