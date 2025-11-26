# backend/app.py
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import config
from utils.predictors import predict as model_predict, build_feature_vector
from model.feedback import save_feedback
from utils.serial_reader import start as start_serial_reader
import numpy as np
import os
from fastapi.middleware.cors import CORSMiddleware 
app = FastAPI(title="Algal Biofuel Backend", version="1.0")

# ---------- CORS FIX ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------------------

# ----------------------------------------------------
# Load model + scaler
# ----------------------------------------------------
print("[app] Loading model...")
model = joblib.load(config.MODEL_PATH)
print("[app] Model loaded.")

print("[app] Loading scaler...")
scaler = joblib.load(config.SCALER_PATH)
print("[app] Scaler loaded.")

# ----------------------------------------------------
# SENSOR INPUT SCHEMA
# ----------------------------------------------------
class SensorData(BaseModel):
    pH: float
    temperature: float
    turbidity: float
    dissolved_oxygen: float | None = None
    conductivity: float | None = None
    salinity: float | None = None
    light_energy: float | None = None
    air_temperature: float | None = None
    depth_cm: float | None = None

class FeedbackData(SensorData):
    corrected_biomass: float

# ----------------------------------------------------
# API ROUTES
# ----------------------------------------------------

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Algal Biofuel Optimizer Backend Active",
        "model": "Biomass Prediction + Optimization"
    }

@app.post("/predict")
def predict_route(data: SensorData):
    raw_dict = data.dict()

    # Build features
    X = build_feature_vector(raw_dict, use_advanced=True)

    # Scale + predict
    X_scaled = scaler.transform(X)
    pred = float(model.predict(X_scaled)[0])

    return {
        "predicted_biomass": pred,
        "input_used": raw_dict
    }


@app.post("/wifi-data")
def wifi_input(data: SensorData):
    """Endpoint for ESP32 / Raspberry Pi to POST sensor data."""
    return predict_route(data)


@app.post("/manual-entry")
def manual_entry(data: SensorData):
    """Frontend manual input"""
    return predict_route(data)


@app.post("/feedback")
def feedback_route(fb: FeedbackData):
    """Allow user to send correction of biomass back to model."""
    save_feedback(fb.dict())
    return {"status": "saved", "message": "Feedback stored successfully."}


# ----------------------------------------------------
# START SERIAL THREAD
# ----------------------------------------------------
@app.on_event("startup")
def startup_event():
    print("[app] Starting serial reader...")
    start_serial_reader()
    print("[app] Serial reader running.")


# ----------------------------------------------------
# Start server when executed directly
# ----------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
