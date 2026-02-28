"""
RentSight Price Predictor — FastAPI Application
=================================================
REST API for optimal price prediction of new Airbnb listings.

Endpoints:
    GET  /              — Health check
    POST /predict       — Full price recommendation
    POST /market-price  — Market price only (fast)
    GET  /amenities     — List of recognised amenities
"""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from predict import load_models, predict_optimal_price, predict_market_price, get_neighborhood_prices

logger = logging.getLogger("uvicorn.error")

# ==============================================================================
# APP SETUP
# ==============================================================================

# ---------------------------------------------------------------------------
# Lifespan — load models once at startup, release on shutdown
# ---------------------------------------------------------------------------
models = None


@asynccontextmanager
async def lifespan(application: FastAPI):
    global models
    logger.info("Loading price prediction models...")
    models = load_models()
    has_occ = models['occ_model'] is not None
    logger.info(f"Models loaded! (occupancy model: {'yes' if has_occ else 'no'})")
    yield  # app is running
    logger.info("Shutting down price predictor.")


app = FastAPI(
    title="RentSight Price Predictor API",
    description=(
        "Predict the optimal nightly price for a new Airbnb listing. "
        "Combines market-rate modelling with revenue optimisation."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================================================
# SCHEMAS
# ==============================================================================

class Location(BaseModel):
    lat: float = Field(..., description="Latitude", examples=[33.65])
    lng: float = Field(..., description="Longitude", examples=[73.04])


class PricePredictionRequest(BaseModel):
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


class NeighborhoodStats(BaseModel):
    comparable_count: int
    min: float
    q25: float
    median: float
    q75: float
    max: float
    mean: float


class PriceRange(BaseModel):
    low: float
    high: float


class PricePredictionResponse(BaseModel):
    market_price: float = Field(..., description="Model-predicted market rate ($/night)")
    optimal_price: float = Field(..., description="Revenue-maximised price ($/night)")
    expected_occupancy: Optional[float] = Field(None, description="Expected occupancy rate at optimal price (%)")
    expected_monthly_revenue: Optional[float] = Field(None, description="Expected monthly revenue ($)")
    base_occupancy: Optional[float] = Field(None, description="Base occupancy at market price (%)")
    price_sensitivity: Optional[float] = Field(None, description="Price sensitivity coefficient (lower = less sensitive)")
    price_range: PriceRange = Field(..., description="Recommended pricing bracket")
    neighborhood: NeighborhoodStats = Field(..., description="Comparable listing price stats")
    recommendation: str = Field(..., description="Human-readable pricing recommendation")
    amenity_count: int = Field(..., description="Number of amenities provided")
    model_version: str = Field(default="1.0", description="Model version")


# ==============================================================================
# ENDPOINTS
# ==============================================================================

@app.get("/", tags=["Health"])
def root():
    """Health check."""
    return {"status": "ok", "service": "RentSight Price Predictor"}


@app.post("/predict", response_model=PricePredictionResponse, tags=["Prediction"])
def predict(req: PricePredictionRequest):
    """
    Full price recommendation for a new listing.

    Returns market price, revenue-optimised price, expected occupancy,
    expected monthly revenue, price range, neighbourhood comparables,
    and a human-readable recommendation.
    """
    try:
        listing = {
            "max_guests": req.max_guests,
            "bedrooms": req.bedrooms,
            "beds": req.beds,
            "baths": req.baths,
            "listing_type": req.listing_type,
            "room_type": req.room_type,
            "location": {"lat": req.location.lat, "lng": req.location.lng},
            "amenities": req.amenities,
        }

        result = predict_optimal_price(listing, models)

        return PricePredictionResponse(
            market_price=result['market_price'],
            optimal_price=result['optimal_price'],
            expected_occupancy=result.get('expected_occupancy'),
            expected_monthly_revenue=result.get('expected_monthly_revenue'),
            base_occupancy=result.get('base_occupancy'),
            price_sensitivity=result.get('price_sensitivity'),
            price_range=result['price_range'],
            neighborhood=result['neighborhood'],
            recommendation=result['recommendation'],
            amenity_count=len(req.amenities),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/market-price", tags=["Prediction"])
def market_price(req: PricePredictionRequest):
    """Quick market price estimate (no revenue optimisation)."""
    try:
        listing = {
            "max_guests": req.max_guests,
            "bedrooms": req.bedrooms,
            "beds": req.beds,
            "baths": req.baths,
            "listing_type": req.listing_type,
            "room_type": req.room_type,
            "location": {"lat": req.location.lat, "lng": req.location.lng},
            "amenities": req.amenities,
        }
        price = predict_market_price(listing, models)
        neighborhood = get_neighborhood_prices(listing, models)
        return {
            "market_price": price,
            "neighborhood": neighborhood,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/amenities", tags=["Reference"])
def list_amenities():
    """Return the amenities the model recognises as features."""
    meta = models['price_meta'] if models else {}
    top = meta.get("top_amenities", [])
    categories = meta.get("amenity_categories", {})
    return {
        "top_amenities": top,
        "categories": dict(categories.items()),
    }


# ==============================================================================
# RUN
# ==============================================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("app:app", host="0.0.0.0", port=port, log_level="info")
