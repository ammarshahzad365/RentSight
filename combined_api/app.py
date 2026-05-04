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
from typing import Optional, Literal
from predict import load_all_models, predict_with_price, predict_without_price

# ==============================================================================
# APP SETUP
# ==============================================================================

CityType = Literal['islamabad', 'lahore', 'karachi']

app = FastAPI(
    title="RentSight Combined API",
    description=(
        "Unified API for Airbnb listing analysis across Islamabad, Lahore, and Karachi. "
        "Predicts occupancy when price is known, or finds the optimal price "
        "and then predicts occupancy — returning full revenue analytics in both cases."
    ),
    version="2.0.0",
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
            detail=f"Models for '{city}' are not available. Check that training has been run for this city.",
        )
    return all_city_models[city]


# ==============================================================================
# SHARED SCHEMAS
# ==============================================================================

class Location(BaseModel):
    lat: float = Field(..., description="Latitude",  examples=[33.65])
    lng: float = Field(..., description="Longitude", examples=[73.04])


class NeighborhoodStats(BaseModel):
    comparable_count: int
    min:    float
    q25:    float
    median: float
    q75:    float
    max:    float
    mean:   float


class PriceRange(BaseModel):
    low:  float
    high: float


# ==============================================================================
# ENDPOINT 1 — Price IS provided
# ==============================================================================

class PredictWithPriceRequest(BaseModel):
    """All listing fields INCLUDING price."""
    price: float = Field(..., gt=0, description="Nightly price in USD", examples=[35.0])
    max_guests: int = Field(..., ge=1, description="Maximum number of guests", examples=[4])
    bedrooms: int = Field(..., ge=0, description="Number of bedrooms", examples=[2])
    beds: int = Field(..., ge=1, description="Number of beds", examples=[2])
    baths: float = Field(..., ge=0, description="Number of bathrooms", examples=[1.0])
    listing_type: str = Field(
        default="Entire rental unit",
        description="Type of listing",
        examples=["Entire rental unit", "Private room", "Entire home"],
    )
    room_type: str = Field(
        default="Entire rental unit",
        description="Room type",
        examples=["Entire rental unit", "Private room"],
    )
    location: Location = Field(..., description="Listing coordinates")
    amenities: list[str] = Field(
        default=[],
        description="List of amenity names",
        examples=[["Wifi", "Kitchen", "Air conditioning", "TV", "Free parking on premises"]],
    )


class PredictWithPriceResponse(BaseModel):
    """Response when price is provided — occupancy + derived metrics."""
    price: float = Field(..., description="The price you provided ($/night)")
    market_price: float = Field(..., description="Model-predicted market rate ($/night)")
    occupancy_rate: float = Field(..., description="Predicted occupancy rate (%)")
    positioning: str = Field(..., description="Price positioning vs market")
    booked_nights_per_month: float = Field(..., description="Expected booked nights per month")
    booked_nights_per_year: int = Field(..., description="Expected booked nights per year")
    monthly_revenue: float = Field(..., description="Expected monthly revenue ($)")
    annual_revenue: float = Field(..., description="Expected annual revenue ($)")
    daily_earnings: float = Field(..., description="Average daily earnings ($)")
    recommendation: str = Field(..., description="Human-readable recommendation")


@app.post(
    "/{city}/predict",
    response_model=PredictWithPriceResponse,
    tags=["Prediction"],
    summary="Predict occupancy for a given price",
)
def predict_endpoint(
    req: PredictWithPriceRequest,
    city: CityType = Path(..., description="City (islamabad | lahore | karachi)"),
):
    """
    **Price IS provided** — predict occupancy at the given price and return
    full revenue analytics.

    Use this when the host already has a price in mind and wants to know
    what occupancy rate and revenue to expect.
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
    """All listing fields EXCEPT price."""
    max_guests: int = Field(..., ge=1, description="Maximum number of guests", examples=[4])
    bedrooms: int = Field(..., ge=0, description="Number of bedrooms", examples=[2])
    beds: int = Field(..., ge=1, description="Number of beds", examples=[2])
    baths: float = Field(..., ge=0, description="Number of bathrooms", examples=[1.0])
    listing_type: str = Field(
        default="Entire rental unit",
        description="Type of listing",
        examples=["Entire rental unit", "Private room", "Entire home"],
    )
    room_type: str = Field(
        default="Entire rental unit",
        description="Room type",
        examples=["Entire rental unit", "Private room"],
    )
    location: Location = Field(..., description="Listing coordinates")
    amenities: list[str] = Field(
        default=[],
        description="List of amenity names",
        examples=[["Wifi", "Kitchen", "Air conditioning", "TV", "Free parking on premises"]],
    )


class MarketPriceAnalysis(BaseModel):
    market_price: float = Field(..., description="Model-predicted market rate ($/night)")
    occupancy_at_market_price: float = Field(..., description="Occupancy at market price (%)")
    booked_nights_per_month: float = Field(..., description="Booked nights/month at market price")
    monthly_revenue_at_market: float = Field(..., description="Monthly revenue at market price ($)")


class PredictWithoutPriceResponse(BaseModel):
    """Response when price is NOT provided — optimal price + occupancy + derived metrics."""
    optimal_price: float = Field(..., description="Revenue-maximised price ($/night)")
    market_price: float = Field(..., description="Model-predicted market rate ($/night)")
    price: float = Field(..., description="Recommended price — same as optimal_price ($/night)")
    occupancy_rate: float = Field(..., description="Predicted occupancy at optimal price (%)")
    positioning: str = Field(..., description="Optimal price positioning vs market")
    booked_nights_per_month: float = Field(..., description="Expected booked nights per month")
    booked_nights_per_year: int = Field(..., description="Expected booked nights per year")
    monthly_revenue: float = Field(..., description="Expected monthly revenue ($)")
    annual_revenue: float = Field(..., description="Expected annual revenue ($)")
    daily_earnings: float = Field(..., description="Average daily earnings ($)")
    price_range: PriceRange = Field(..., description="Recommended pricing bracket (±15%)")
    neighborhood: NeighborhoodStats = Field(..., description="Comparable listing price stats")
    recommendation: str = Field(..., description="Human-readable recommendation")
    amenity_count: int = Field(..., description="Number of amenities provided")
    price_sensitivity: float = Field(..., description="Price sensitivity coefficient (0.5=luxury → 1.2=budget)")
    occupancy_at_market_price: float = Field(..., description="Occupancy at market price for comparison (%)")
    market_price_analysis: MarketPriceAnalysis = Field(..., description="Detailed market-price comparison")


@app.post(
    "/{city}/predict-price",
    response_model=PredictWithoutPriceResponse,
    tags=["Prediction"],
    summary="Find optimal price and predict occupancy",
)
def predict_price_endpoint(
    req: PredictWithoutPriceRequest,
    city: CityType = Path(..., description="City (islamabad | lahore | karachi)"),
):
    """
    **Price NOT provided** — find the optimal price, predict occupancy at
    that price, and return full revenue analytics.

    Use this when the host wants a data-driven price recommendation
    and wants to know the expected occupancy and revenue at that price.
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

@app.get("/", tags=["Health"])
def root():
    """Health check — returns service status and which city models are loaded."""
    return {
        "status": "ok",
        "service": "RentSight Combined API",
        "version": "2.0.0",
        "cities_loaded": list(all_city_models.keys()),
    }


@app.get("/cities", tags=["Reference"])
def list_cities():
    """Return which cities have models loaded and are ready to serve predictions."""
    return {
        "available": list(all_city_models.keys()),
        "all": ["islamabad", "lahore", "karachi"],
    }


@app.get("/{city}/amenities", tags=["Reference"])
def list_amenities(
    city: CityType = Path(..., description="City (islamabad | lahore | karachi)"),
):
    """Return the amenities the models for this city recognise as features."""
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
