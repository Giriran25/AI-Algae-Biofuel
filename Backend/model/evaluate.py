# backend/model/evaluate.py
import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import numpy as np

DATASET_FILE = "backend/storage/processed_dataset.csv"
MODEL_PATH = "backend/storage/biomass_model.joblib"
SCALER_PATH = "backend/storage/scaler.joblib"


def evaluate():
    print("[evaluate] Loading model & scaler...")
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    df = pd.read_csv(DATASET_FILE)
    FEATURES = [
        "pH","temperature","turbidity","dissolved_oxygen",
        "conductivity","salinity","light_energy",
        "air_temperature","depth_cm"
    ]
    TARGET = "biomass"

    df = df.fillna(df.median())
    X = scaler.transform(df[FEATURES].values)
    y = df[TARGET].values

    preds = model.predict(X)

    mae = mean_absolute_error(y, preds)
    rmse = np.sqrt(mean_squared_error(y, preds))
    r2 = r2_score(y, preds)

    print("\n===== FULL DATASET EVALUATION =====")
    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R²:   {r2:.4f}")

if __name__ == "__main__":
    evaluate()
