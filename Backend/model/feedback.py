# backend/model/feedback.py
import os
import pandas as pd

FEEDBACK_FILE = "backend/storage/feedback_buffer.csv"

def save_feedback(feedback_entry: dict):
    """
    feedback_entry = {
        "pH": 7.9,
        "temperature": 24.1,
        "turbidity": 45.2,
        "dissolved_oxygen": 8.22,
        "conductivity": 42000,
        "salinity": 33.9,
        "light_energy": 650.5,
        "air_temperature": 26.1,
        "depth_cm": 24,
        "corrected_biomass": 0.412
    }
    """

    df_new = pd.DataFrame([feedback_entry])

    if os.path.exists(FEEDBACK_FILE):
        df_old = pd.read_csv(FEEDBACK_FILE)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(FEEDBACK_FILE, index=False)
    print(f"[feedback] Saved entry. Total feedback rows = {len(df)}")
