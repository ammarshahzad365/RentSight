from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from predict import load_model, predict_occupancy

# ==============================================================================
# APP SETUP
# ==============================================================================

app = FastAPI(
    title="RentSight Occupancy Predictor API",
    description="Predict Airbnb listing occupancy rates based on listing features and amenities.",
    version="1.0.0",
)

# Allow all origins for development — restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once at startup
model, encoders = None, None


@app.on_event("startup")
def startup():
    global model, encoders
    print("Loading occupancy prediction model...")
    model, encoders = load_model()
    print("Model loaded and ready!")


# ==============================================================================
# SCHEMAS
# ==============================================================================

class Location(BaseModel):
    lat: float = Field(..., description="Latitude", examples=[33.65])
    lng: float = Field(..., description="Longitude", examples=[73.04])


class PredictionRequest(BaseModel):
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


class PredictionResponse(BaseModel):
    occupancy_rate: float = Field(..., description="Predicted occupancy rate (%)", examples=[42.5])
    amenity_count: int = Field(..., description="Number of amenities provided")
    model_version: str = Field(default="2.0-amenities", description="Model version used")


# ==============================================================================
# ENDPOINTS
# ==============================================================================

@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "RentSight Occupancy Predictor"}


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(req: PredictionRequest):
    """
    Predict the occupancy rate for an Airbnb listing.

    Accepts listing details including price, capacity, location, and amenities.
    Returns a predicted occupancy rate between 10% and 95%.
    """
    try:
        listing = {
            "price": req.price,
            "max_guests": req.max_guests,
            "bedrooms": req.bedrooms,
            "beds": req.beds,
            "baths": req.baths,
            "listing_type": req.listing_type,
            "room_type": req.room_type,
            "location": {"lat": req.location.lat, "lng": req.location.lng},
            "amenities": req.amenities,
        }

        occ = predict_occupancy(listing, model=model, encoders=encoders)

        return PredictionResponse(
            occupancy_rate=occ,
            amenity_count=len(req.amenities),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/amenities", tags=["Reference"])
def list_amenities():
    """Return the list of amenities the model recognizes as features."""
    top = encoders.get("top_amenities", []) if encoders else []
    categories = encoders.get("amenity_categories", {}) if encoders else {}
    return {
        "top_amenities": top,
        "categories": {k: v for k, v in categories.items()},
    }


# ==============================================================================
# RUN
# ==============================================================================

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
