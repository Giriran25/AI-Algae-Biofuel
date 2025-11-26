# backend/model/train_model.py
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

DATASET_FILE = "backend/storage/processed_dataset.csv"
FEEDBACK_FILE = "backend/storage/feedback_buffer.csv"
MODEL_PATH = "backend/storage/biomass_model.joblib"
SCALER_PATH = "backend/storage/scaler.joblib"


def train():
    print(f"[train] Loading dataset: {DATASET_FILE}")
    df_main = pd.read_csv(DATASET_FILE)

    # Load feedback if exists
    if os.path.exists(FEEDBACK_FILE):
        print("[train] Loading feedback entries...")
        df_fb = pd.read_csv(FEEDBACK_FILE)
        df = pd.concat([df_main, df_fb], ignore_index=True)
        print(f"[train] Feedback rows added: {len(df_fb)}")
    else:
        df = df_main

    print(f"[train] Dataset shape: {df.shape}")

    # Features & target
    FEATURES = [
        "pH", "temperature", "turbidity", "dissolved_oxygen",
        "conductivity", "salinity", "light_energy",
        "air_temperature", "depth_cm"
    ]

    TARGET = "biomass"

    # Fill missing values
    df = df.fillna(df.median())

    X = df[FEATURES].values
    y = df[TARGET].values

    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.18, random_state=42
    )

    print("[train] Training HistGradientBoostingRegressor...")
    model = HistGradientBoostingRegressor(
        max_depth=6,
        learning_rate=0.08,
        max_iter=300,
        l2_regularization=0.1,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print("\n===== MODEL PERFORMANCE =====")
    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R²:   {r2:.4f}")

    # Cross-validation
    cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring="r2")
    print("\n===== CROSS-VALIDATION (5-FOLD) =====")
    print("CV R² Scores:", cv_scores)
    print("Mean CV R²:", cv_scores.mean())

    # Save model & scaler
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    print(f"\n[train] Model saved → {MODEL_PATH}")
    print(f"[train] Scaler saved → {SCALER_PATH}")

    print("\nSample predictions:")
    for i in range(5):
        print(f"Input={X_test[i]} → Pred={model.predict([X_test[i]])[0]:.4f}")

if __name__ == "__main__":
    train()
