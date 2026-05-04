# RentSight – Short-Term Rental Analytics & Pricing Intelligence

RentSight is a data-driven platform for analyzing Airbnb short-term rental (STR) listings across Pakistani cities.
It sanitizes raw scraped listing data, estimates occupancy rates, trains city-specific ML models, and serves predictions through a unified REST API.

---

## Cities Supported

| City | Raw Listings | Sanitized Listings |
|------|-------------|-------------------|
| Islamabad | `listings-islamabad/` | `listings-sanitized-islamabad/` |
| Lahore | `listings-lahore/` | `listings-sanitized-lahore/` |
| Karachi | `listings-karachi/` | `listings-sanitized-karachi/` |

---

## Project Structure

```
RentSight/
├── listings-islamabad/          # Raw scraped listings — Islamabad
├── listings-lahore/             # Raw scraped listings — Lahore
├── listings-karachi/            # Raw scraped listings — Karachi
├── listings-sanitized-islamabad/# Cleaned listings with occ_rate — Islamabad
├── listings-sanitized-lahore/   # Cleaned listings with occ_rate — Lahore
├── listings-sanitized-karachi/  # Cleaned listings with occ_rate — Karachi
│
├── listing-sanitizer/           # Data cleaning pipeline
│   ├── main.py                  # Entry point — run full pipeline for a city
│   ├── add_occupancy_rate.py    # Compute & write occ_rate (manual step)
│   ├── copy_listings.py
│   ├── sanitize_prices.py
│   ├── sanitize_ratings.py
│   ├── sanitize_reviews.py
│   ├── sanitize_url.py
│   ├── sanitize_location.py
│   ├── sanitize_amenities.py
│   ├── sanitize_cleanup.py
│   ├── validate_fields.py
│   └── utils.py                 # City-aware path helpers (RENTSIGHT_CITY env var)
│
├── price_predictor/             # XGBoost market-price model (per city)
│   ├── train_model.py           # --city islamabad|lahore|karachi
│   └── ...
│
├── occupancy_predictor/         # XGBoost occupancy-rate model (per city)
│   ├── train_model.py           # --city islamabad|lahore|karachi
│   └── ...
│
└── combined_api/                # FastAPI service — all cities, all endpoints
    ├── app.py
    ├── predict.py
    ├── islamabad/               # Trained models for Islamabad
    │   ├── xgb_price_model.pkl
    │   ├── price_model_meta.pkl
    │   ├── xgb_occupancy_model.pkl
    │   └── label_encoders.pkl
    ├── lahore/                  # Trained models for Lahore
    └── karachi/                 # Trained models for Karachi
```

---

## Workflow

### 1. Sanitize listings for a city

```bash
python listing-sanitizer/main.py --city islamabad
python listing-sanitizer/main.py --city lahore
python listing-sanitizer/main.py --city karachi
```

This runs the full pipeline:
copy → sanitize prices → sanitize ratings → sanitize reviews → sanitize URLs → sanitize location → sanitize amenities → cleanup → validate

### 2. Add occupancy rates (manual step)

Must be run after sanitization. Reads original listings for review signals (volume, recency, frequency), ratings, and amenities to estimate occupancy.

```bash
python listing-sanitizer/add_occupancy_rate.py --city islamabad
python listing-sanitizer/add_occupancy_rate.py --city lahore
python listing-sanitizer/add_occupancy_rate.py --city karachi
```

### 3. Train models for a city

Train both the price predictor and occupancy predictor. Models are saved to `combined_api/{city}/`.

```bash
python price_predictor/train_model.py --city islamabad
python occupancy_predictor/train_model.py --city islamabad

python price_predictor/train_model.py --city lahore
python occupancy_predictor/train_model.py --city lahore

python price_predictor/train_model.py --city karachi
python occupancy_predictor/train_model.py --city karachi
```

### 4. Run the API

```bash
cd combined_api
uvicorn app:app --host 0.0.0.0 --port 8002
```

Or via Docker:

```bash
cd combined_api
docker build -t rentsight-api .
docker run -p 8002:8002 rentsight-api
```

---

## API Endpoints

Base URL: `http://localhost:8002`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check — lists loaded cities |
| GET | `/cities` | Which cities have models loaded |
| POST | `/{city}/predict` | Price IS provided → occupancy + revenue analytics |
| POST | `/{city}/predict-price` | Price NOT provided → optimal price + occupancy + revenue |
| GET | `/{city}/amenities` | Amenities recognised by that city's model |

`{city}` is one of: `islamabad`, `lahore`, `karachi`

### POST `/{city}/predict` — price known

Request:
```json
{
  "price": 35.0,
  "max_guests": 4,
  "bedrooms": 2,
  "beds": 2,
  "baths": 1.0,
  "listing_type": "Entire rental unit",
  "room_type": "Entire rental unit",
  "location": { "lat": 33.65, "lng": 73.06 },
  "amenities": ["Wifi", "Kitchen", "Air conditioning", "TV"]
}
```

Response includes: `occupancy_rate`, `market_price`, `positioning`, `booked_nights_per_month`, `monthly_revenue`, `annual_revenue`, `recommendation`.

### POST `/{city}/predict-price` — price unknown

Same request body but without `price`.

Response includes everything above plus: `optimal_price`, `price_range`, `neighborhood` stats, `price_sensitivity`, `market_price_analysis`.

---

## Models

Each city has two independently trained XGBoost models:

- **Price model** — predicts the market-rate nightly price from listing features (capacity, location, amenities). Trained on log-price to handle skew.
- **Occupancy model** — predicts the occupancy rate (%) using price, listing features, neighborhood context, and amenity signals.

Training uses 5-fold cross-validation with early stopping. Models are stored per city in `combined_api/{city}/`.

---

## Occupancy Rate Estimation

The `add_occupancy_rate.py` script uses a weighted multi-factor model applied to the **original** (pre-sanitization) listings:

| Factor | Weight | Signal |
|--------|--------|--------|
| Review volume | 30% | More reviews → more bookings (log curve) |
| Review recency | 15% | Recent activity = current demand |
| Review frequency | 10% | Reviews/month across listing lifespan |
| Ratings | 10% | Higher ratings attract more guests |
| Price competitiveness | 15% | Price vs. city median |
| Capacity | 5% | Sweet spot: 2–3 bed, 4–6 guests |
| Listing type | 5% | Entire home > private room > shared |
| Amenities | 10% | More amenity categories = higher attractiveness |

Final score is mapped to a 10–95% range through a sigmoid curve.
