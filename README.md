# Airbnb Scraper Setup and Usage Guide

## Prerequisites

1. **Python 3.12+** installed on your system
2. **Chrome browser** installed (the script uses ChromeDriver)
3. **ChromeDriver** - The script will automatically download and manage ChromeDriver through Selenium 4.x

## Setup Instructions

### 1. Create and Activate Virtual Environment

```powershell
# Navigate to the project directory
cd "c:\Users\CN0007\Downloads\airbnb_scrape"

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run this first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Install Dependencies

```powershell
# Install required packages
pip install -r requirements.txt

# Or install just the main dependency
pip install selenium==4.34.2
```

### 3. Verify Installation

```powershell
python -c "import selenium; print('Selenium version:', selenium.__version__)"
```

## Running the Project

### Basic Usage

```powershell
# Make sure your virtual environment is activated
.\venv\Scripts\Activate.ps1

# Run the scraper with default settings (2025-10-01 to 2025-10-03, 2 pages)
python scrape_airbnb_islamabad.py
```

### Custom Usage

You can modify the dates and number of pages in the script's main section:

```python
if __name__ == "__main__":
    # Customize these parameters
    listings = scrape_islamabad_listings("2025-08-01", "2025-08-03", max_pages=3)
    print(f"Collected {len(listings)} listings")
    
    # Results are saved to islamabad_listings_output.json
    with open("islamabad_listings_output.json", "w", encoding="utf-8") as f:
        json.dump([asdict(l) for l in listings], f, ensure_ascii=False, indent=2)
```

## Output

- The script will create `islamabad_listings_output.json` with all scraped listing data
- Each listing includes: title, price, ratings, amenities, capacity, and more
- The script will print the number of listings collected

## Important Notes

1. **Legal Compliance**: Review Airbnb's Terms of Service before scraping
2. **Rate Limiting**: The script includes delays to be respectful to the server
3. **Dynamic Content**: Airbnb's interface may change; selectors might need updates
4. **Browser Automation**: A Chrome browser window will open during scraping

## Troubleshooting

### ChromeDriver Issues
- Selenium 4.x automatically manages ChromeDriver
- Ensure Chrome browser is installed and up to date

### Execution Policy (Windows)
If you get an execution policy error when activating the virtual environment:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Element Not Found Errors
- Airbnb's interface changes frequently
- You may need to update CSS selectors in the script
- Check if the page structure has changed

## File Structure

```
airbnb_scrape/
├── venv/                           # Virtual environment
├── scrape_airbnb_islamabad.py      # Main scraper script
├── requirements.txt                # All dependencies with versions
├── requirements-simple.txt         # Just selenium dependency
├── islamabad_airbnb_listings.json  # Sample data (if exists)
├── islamabad_listings_output.json  # Script output (generated)
└── README.md                      # This guide
```
