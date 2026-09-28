"""
RentSight Combined API — FastAPI Application
==============================================
Unified REST API for all three cities (Islamabad, Lahore, Karachi).

Endpoints:
    GET   /                              — Health check
    GET   /cities                        — List available cities with loaded models
    POST  /{city}/predict                — Price IS provided → occupancy + derived metrics
    POST  /{city}/predict-price          — Price NOT provided → best price + occupancy + derived metrics
    GET   /{city}/amenities              — List of recognised amenities for that city
"""

from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
from predict import load_all_models, predict_with_price, predict_without_price

# ==============================================================================
# APP SETUP
# ==============================================================================

CityType = Literal['islamabad', 'lahore', 'karachi']

_DESCRIPTION = """
## Overview

RentSight is a machine-learning API for short-term rental (Airbnb) analytics across **Islamabad**, **Lahore**, and **Karachi**.

It exposes two core prediction workflows per city:

| Workflow | Endpoint | When to use |
|----------|----------|-------------|
| Price known | `POST /{city}/predict` | Host has a price in mind — get expected occupancy & revenue |
| Price unknown | `POST /{city}/predict-price` | Host wants a data-driven price recommendation + revenue forecast |

---

## How the models work

Each city has **two independently trained XGBoost models**:

- **Price model** — predicts the market-rate nightly price from listing features (room type, capacity, location, amenities). Trained on log-price to handle price skew.
- **Occupancy model** — predicts the occupancy rate (%) using price, listing features, neighborhood context, and amenity signals.

Both models are trained on sanitized, city-specific Airbnb listing data.

---

## Cities

| City | Path prefix |
|------|-------------|
| Islamabad | `/islamabad/...` |
| Lahore | `/lahore/...` |
| Karachi | `/karachi/...` |

---

## Common fields

**`listing_type`** accepted values (case-sensitive):
`Entire rental unit`, `Entire home`, `Entire condo`, `Entire serviced apartment`,
`Private room`, `Private room in home`, `Shared room`, `Room in hotel`

**`room_type`** accepted values:
`Entire home/apt`, `Entire rental unit`, `Private room`, `Shared room`, `Hotel room`

**`amenities`** — use the exact names returned by `GET /{city}/amenities`.
Unrecognised names are silently ignored.
"""

_TAGS = [
    {
        "name": "Prediction",
        "description": "Core prediction endpoints. One for when price is known, one for when it is not.",
    },
    {
        "name": "Reference",
        "description": "Lookup endpoints — cities available, recognised amenity names.",
    },
    {
        "name": "Health",
        "description": "Service health check.",
    },
]

app = FastAPI(
    title="RentSight Combined API",
    description=_DESCRIPTION,
    version="2.0.0",
    openapi_tags=_TAGS,
    contact={
        "name": "RentSight",
        "email": "munim@iclosed.io",
    },
    license_info={
        "name": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Populated at startup: { 'islamabad': {...}, 'lahore': {...}, 'karachi': {...} }
all_city_models: dict = {}


@app.on_event("startup")
def startup():
    global all_city_models
    print("Loading prediction models for all cities...")
    all_city_models = load_all_models()
    loaded = list(all_city_models.keys())
    print(f"Models loaded for: {', '.join(loaded) if loaded else 'none'}")


def _get_city_models(city: str) -> dict:
    """Return models for a city or raise 503 if not loaded."""
    if city not in all_city_models:
        raise HTTPException(
            status_code=503,
            detail=f"Models for '{city}' are not available. Ensure training has been run for this city.",
        )
    return all_city_models[city]


# ==============================================================================
# SHARED SCHEMAS
# ==============================================================================

class Location(BaseModel):
    lat: float = Field(..., description="Latitude (decimal degrees)", examples=[33.65])
    lng: float = Field(..., description="Longitude (decimal degrees)", examples=[73.04])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"lat": 33.65, "lng": 73.06},
            ]
        }
    }


class NeighborhoodStats(BaseModel):
    """Price statistics for comparable listings within ~1 km of the given location."""
    comparable_count: int   = Field(..., description="Number of comparable listings found nearby")
    min:    float           = Field(..., description="Lowest price among comparable listings ($/night)")
    q25:    float           = Field(..., description="25th percentile price ($/night)")
    median: float           = Field(..., description="Median price ($/night)")
    q75:    float           = Field(..., description="75th percentile price ($/night)")
    max:    float           = Field(..., description="Highest price among comparable listings ($/night)")
    mean:   float           = Field(..., description="Average price among comparable listings ($/night)")


class PriceRange(BaseModel):
    """Recommended pricing bracket around the optimal price."""
    low:  float = Field(..., description="Lower bound — 15% below optimal price ($/night)")
    high: float = Field(..., description="Upper bound — 15% above optimal price ($/night)")


# ==============================================================================
# ENDPOINT 1 — Price IS provided
# ==============================================================================

class PredictWithPriceRequest(BaseModel):
    """Request body for `/{city}/predict` — all listing fields **including** price."""

    price: float = Field(
        ..., gt=0,
        description="Nightly price in USD that the host intends to charge.",
        examples=[35.0],
    )
    max_guests: int = Field(
        ..., ge=1,
        description="Maximum number of guests the listing can accommodate.",
        examples=[4],
    )
    bedrooms: int = Field(
        ..., ge=0,
        description="Number of bedrooms (0 for studio).",
        examples=[2],
    )
    beds: int = Field(
        ..., ge=1,
        description="Total number of beds.",
        examples=[2],
    )
    baths: float = Field(
        ..., ge=0,
        description="Number of bathrooms (0.5 = shared half-bath).",
        examples=[1.0],
    )
    listing_type: str = Field(
        default="Entire rental unit",
        description="Airbnb listing type.",
        examples=["Entire rental unit", "Private room", "Entire home"],
    )
    room_type: str = Field(
        default="Entire rental unit",
        description="Airbnb room type category.",
        examples=["Entire home/apt", "Private room"],
    )
    location: Location = Field(..., description="GPS coordinates of the listing.")
    amenities: list[str] = Field(
        default=[],
        description=(
            "List of amenity names exactly as returned by `GET /{city}/amenities`. "
            "Unrecognised names are silently ignored."
        ),
        examples=[["Wifi", "Kitchen", "Air conditioning", "TV", "Free parking on premises"]],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "price": 35.0,
                    "max_guests": 4,
                    "bedrooms": 2,
                    "beds": 2,
                    "baths": 1.0,
                    "listing_type": "Entire rental unit",
                    "room_type": "Entire home/apt",
                    "location": {"lat": 33.65, "lng": 73.06},
                    "amenities": [
                        "Wifi", "Kitchen", "Air conditioning",
                        "TV", "Free parking on premises", "Hot water",
                    ],
                }
            ]
        }
    }


class PredictWithPriceResponse(BaseModel):
    """Revenue analytics for a listing at a host-specified price."""

    price: float           = Field(..., description="The price you provided ($/night).")
    market_price: float    = Field(..., description="Model-predicted market rate for this listing type and location ($/night).")
    occupancy_rate: float  = Field(..., description="Predicted occupancy rate at the given price (%).")
    positioning: str       = Field(..., description=(
        "Where your price sits relative to the market. "
        "One of: `at market rate`, `above market rate (premium positioning)`, "
        "`below market rate (competitive positioning)`."
    ))
    booked_nights_per_month: float = Field(..., description="Expected number of booked nights per month.")
    booked_nights_per_year: int    = Field(..., description="Expected number of booked nights per year.")
    monthly_revenue: float         = Field(..., description="Expected gross monthly revenue ($/month).")
    annual_revenue: float          = Field(..., description="Expected gross annual revenue ($/year).")
    daily_earnings: float          = Field(..., description="Average daily earnings accounting for vacancy ($/day).")
    recommendation: str            = Field(..., description="Human-readable summary with occupancy, revenue, and neighbourhood context.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "price": 35.0,
                    "market_price": 36.23,
                    "occupancy_rate": 23.5,
                    "positioning": "at market rate",
                    "booked_nights_per_month": 7.1,
                    "booked_nights_per_year": 86,
                    "monthly_revenue": 248.5,
                    "annual_revenue": 3010.0,
                    "daily_earnings": 8.28,
                    "recommendation": (
                        "At $35.00/night (at market rate), expect ~24% occupancy "
                        "(~7 nights/month). Estimated monthly revenue: $249. "
                        "Comparable listings in your area charge $28–$45/night."
                    ),
                }
            ]
        }
    }


@app.post(
    "/{city}/predict",
    response_model=PredictWithPriceResponse,
    tags=["Prediction"],
    summary="Predict occupancy at a given price",
    response_description="Occupancy rate and full revenue analytics at the provided price.",
    responses={
        200: {"description": "Prediction successful."},
        422: {"description": "Validation error — check request body fields."},
        500: {"description": "Internal prediction error."},
        503: {"description": "Models for the requested city are not yet loaded."},
    },
)
def predict_endpoint(
    req: PredictWithPriceRequest,
    city: CityType = Path(..., description="City whose model to use.", examples=["islamabad"]),
):
    """
    **Use this endpoint when the host already has a price in mind.**

    Given a complete listing description including the intended nightly price,
    the API predicts:

    - **Occupancy rate** — what percentage of nights will be booked at that price
    - **Revenue metrics** — expected monthly and annual revenue
    - **Market positioning** — how the price compares to comparable listings nearby
    - **Recommendation** — plain-English summary

    The occupancy model is trained on city-specific data, so Islamabad, Lahore,
    and Karachi each produce different predictions reflecting their local markets.
    """
    models = _get_city_models(city)
    try:
        listing = {
            "price":        req.price,
            "max_guests":   req.max_guests,
            "bedrooms":     req.bedrooms,
            "beds":         req.beds,
            "baths":        req.baths,
            "listing_type": req.listing_type,
            "room_type":    req.room_type,
            "location":     {"lat": req.location.lat, "lng": req.location.lng},
            "amenities":    req.amenities,
        }
        result = predict_with_price(listing, models)
        return PredictWithPriceResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================================================
# ENDPOINT 2 — Price NOT provided
# ==============================================================================

class PredictWithoutPriceRequest(BaseModel):
    """Request body for `/{city}/predict-price` — all listing fields **except** price."""

    max_guests: int = Field(
        ..., ge=1,
        description="Maximum number of guests the listing can accommodate.",
        examples=[4],
    )
    bedrooms: int = Field(
        ..., ge=0,
        description="Number of bedrooms (0 for studio).",
        examples=[2],
    )
    beds: int = Field(
        ..., ge=1,
        description="Total number of beds.",
        examples=[2],
    )
    baths: float = Field(
        ..., ge=0,
        description="Number of bathrooms (0.5 = shared half-bath).",
        examples=[1.0],
    )
    listing_type: str = Field(
        default="Entire rental unit",
        description="Airbnb listing type.",
        examples=["Entire rental unit", "Private room", "Entire home"],
    )
    room_type: str = Field(
        default="Entire rental unit",
        description="Airbnb room type category.",
        examples=["Entire home/apt", "Private room"],
    )
    location: Location = Field(..., description="GPS coordinates of the listing.")
    amenities: list[str] = Field(
        default=[],
        description=(
            "List of amenity names exactly as returned by `GET /{city}/amenities`. "
            "Unrecognised names are silently ignored."
        ),
        examples=[["Wifi", "Kitchen", "Air conditioning", "TV", "Free parking on premises"]],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "max_guests": 4,
                    "bedrooms": 2,
                    "beds": 2,
                    "baths": 1.0,
                    "listing_type": "Entire rental unit",
                    "room_type": "Entire home/apt",
                    "location": {"lat": 33.65, "lng": 73.06},
                    "amenities": [
                        "Wifi", "Kitchen", "Air conditioning",
                        "TV", "Free parking on premises", "Hot water",
                    ],
                }
            ]
        }
    }


class MarketPriceAnalysis(BaseModel):
    """Revenue comparison at the raw market price vs the revenue-optimal price."""
    market_price: float              = Field(..., description="Model-predicted market rate ($/night).")
    occupancy_at_market_price: float = Field(..., description="Predicted occupancy if priced at market rate (%).")
    booked_nights_per_month: float   = Field(..., description="Booked nights/month at market rate.")
    monthly_revenue_at_market: float = Field(..., description="Monthly revenue at market rate ($).")


class PredictWithoutPriceResponse(BaseModel):
    """
    Optimal pricing recommendation plus full revenue analytics.

    The `optimal_price` is found by sweeping price points around the market rate
    and selecting the one that maximises `price × occupancy_rate × 30`
    (estimated monthly revenue). It accounts for price sensitivity — premium
    listings are penalised less for pricing above market.
    """

    optimal_price: float    = Field(..., description="Revenue-maximising price found by the model ($/night).")
    market_price: float     = Field(..., description="Raw market-rate prediction for this listing type and location ($/night).")
    price: float            = Field(..., description="Alias for `optimal_price` — the recommended price to set ($/night).")
    occupancy_rate: float   = Field(..., description="Predicted occupancy rate at the optimal price (%).")
    positioning: str        = Field(..., description=(
        "Where the optimal price sits relative to market. "
        "One of: `at market rate`, `above market rate (premium positioning)`, "
        "`below market rate (competitive positioning)`."
    ))
    booked_nights_per_month: float  = Field(..., description="Expected booked nights per month at the optimal price.")
    booked_nights_per_year: int     = Field(..., description="Expected booked nights per year at the optimal price.")
    monthly_revenue: float          = Field(..., description="Expected gross monthly revenue at the optimal price ($).")
    annual_revenue: float           = Field(..., description="Expected gross annual revenue at the optimal price ($).")
    daily_earnings: float           = Field(..., description="Average daily earnings accounting for vacancy ($/day).")
    price_range: PriceRange         = Field(..., description="Suggested pricing window — ±15% around the optimal price.")
    neighborhood: NeighborhoodStats = Field(..., description="Price distribution of comparable listings within ~1 km.")
    recommendation: str             = Field(..., description="Human-readable summary with price, occupancy, revenue, and neighbourhood context.")
    amenity_count: int              = Field(..., description="Number of amenities from the request that the model recognised.")
    price_sensitivity: float        = Field(..., description=(
        "How elastic demand is for this listing. "
        "Range 0.5 (luxury — less sensitive to price) → 1.2 (budget — more sensitive). "
        "Influences how aggressively the model penalises above-market pricing."
    ))
    occupancy_at_market_price: float    = Field(..., description="Predicted occupancy if the listing were priced at the raw market rate — for comparison (%).")
    market_price_analysis: MarketPriceAnalysis = Field(..., description="Revenue metrics at the raw market price for side-by-side comparison with the optimal price.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "optimal_price": 36.35,
                    "market_price": 36.23,
                    "price": 36.35,
                    "occupancy_rate": 23.5,
                    "positioning": "at market rate",
                    "booked_nights_per_month": 7.1,
                    "booked_nights_per_year": 86,
                    "monthly_revenue": 257.89,
                    "annual_revenue": 3127.1,
                    "daily_earnings": 8.6,
                    "price_range": {"low": 30.9, "high": 41.8},
                    "neighborhood": {
                        "comparable_count": 12,
                        "min": 18.0, "q25": 26.5, "median": 34.0,
                        "q75": 44.0, "max": 72.0, "mean": 35.1,
                    },
                    "recommendation": (
                        "At $36.35/night (at market rate), expect ~24% occupancy "
                        "(~7 nights/month). Estimated monthly revenue: $258. "
                        "Comparable listings in your area charge $27–$44/night."
                    ),
                    "amenity_count": 6,
                    "price_sensitivity": 0.87,
                    "occupancy_at_market_price": 23.4,
                    "market_price_analysis": {
                        "market_price": 36.23,
                        "occupancy_at_market_price": 23.4,
                        "booked_nights_per_month": 7.0,
                        "monthly_revenue_at_market": 253.61,
                    },
                }
            ]
        }
    }


@app.post(
    "/{city}/predict-price",
    response_model=PredictWithoutPriceResponse,
    tags=["Prediction"],
    summary="Find the optimal price and predict occupancy",
    response_description="Optimal price recommendation, occupancy forecast, and full revenue analytics.",
    responses={
        200: {"description": "Prediction successful."},
        422: {"description": "Validation error — check request body fields."},
        500: {"description": "Internal prediction error."},
        503: {"description": "Models for the requested city are not yet loaded."},
    },
)
def predict_price_endpoint(
    req: PredictWithoutPriceRequest,
    city: CityType = Path(..., description="City whose model to use.", examples=["islamabad"]),
):
    """
    **Use this endpoint when the host does not yet have a price in mind.**

    Given a listing description (without price), the API:

    1. **Predicts the market rate** — what similar listings in the area charge
    2. **Finds the optimal price** — sweeps price points to maximise estimated monthly revenue
       (`price × occupancy × 30`), accounting for how price-sensitive this type of listing is
    3. **Predicts occupancy** at the optimal price using the occupancy model
    4. **Computes full revenue metrics** — monthly/annual revenue, booked nights, daily earnings
    5. **Returns a market comparison** — how the optimal price compares to the raw market rate

    The `price_sensitivity` coefficient reflects how aggressively demand drops as price
    rises above market: `0.5` = luxury (less penalised), `1.2` = budget (more penalised).
    """
    models = _get_city_models(city)
    try:
        listing = {
            "max_guests":   req.max_guests,
            "bedrooms":     req.bedrooms,
            "beds":         req.beds,
            "baths":        req.baths,
            "listing_type": req.listing_type,
            "room_type":    req.room_type,
            "location":     {"lat": req.location.lat, "lng": req.location.lng},
            "amenities":    req.amenities,
        }
        result = predict_without_price(listing, models)
        return PredictWithoutPriceResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================================================
# REFERENCE ENDPOINTS
# ==============================================================================

@app.get(
    "/",
    tags=["Health"],
    summary="Health check",
    response_description="Service status and list of cities with models currently loaded.",
)
def root():
    """Returns `ok` plus which city models are currently loaded and serving requests."""
    return {
        "status": "ok",
        "service": "RentSight Combined API",
        "version": "2.0.0",
        "cities_loaded": list(all_city_models.keys()),
    }


@app.get(
    "/cities",
    tags=["Reference"],
    summary="List available cities",
    response_description="Cities with models loaded vs all supported cities.",
)
def list_cities():
    """
    Returns two lists:

    - **`available`** — cities that have models loaded and are ready to serve predictions right now
    - **`all`** — every city the API supports (models may not be loaded for all of them)
    """
    return {
        "available": list(all_city_models.keys()),
        "all": ["islamabad", "lahore", "karachi"],
    }


@app.get(
    "/{city}/amenities",
    tags=["Reference"],
    summary="List recognised amenities for a city",
    response_description="Top individual amenities and grouped amenity categories used as model features.",
    responses={
        503: {"description": "Models for the requested city are not yet loaded."},
    },
)
def list_amenities(
    city: CityType = Path(..., description="City whose amenity list to return.", examples=["islamabad"]),
):
    """
    Returns the amenity names that the **city's model** was trained on.

    Use these exact strings in the `amenities` array when calling the prediction
    endpoints — unrecognised names are silently ignored by the model.

    Response structure:

    - **`top_amenities`** — individual amenities used as binary features (present / not present)
    - **`categories`** — grouped amenity categories used as count features
      (e.g. `kitchen`, `comfort`, `safety`, `entertainment`, `convenience`, `outdoor`, `family`)
    """
    models = _get_city_models(city)
    meta = models['price_meta']
    return {
        "city": city,
        "top_amenities": meta.get("top_amenities", []),
        "categories": dict(meta.get("amenity_categories", {}).items()),
    }


# ==============================================================================
# RUN
# ==============================================================================

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8002))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
