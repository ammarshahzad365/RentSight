FROM python:3.12-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the combined API code
COPY . .

# Copy model artefacts from sibling directories
COPY ../price_predictor/xgb_price_model.pkl    /models/price_predictor/xgb_price_model.pkl
COPY ../price_predictor/price_model_meta.pkl    /models/price_predictor/price_model_meta.pkl
COPY ../occupancy_predictor/xgb_occupancy_model.pkl /models/occupancy_predictor/xgb_occupancy_model.pkl
COPY ../occupancy_predictor/label_encoders.pkl  /models/occupancy_predictor/label_encoders.pkl

CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8002}
