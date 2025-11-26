# backend/config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dataset path (ATP3 uploaded file)
CLEANED_DATA_PATH = os.path.normpath("/mnt/data/atp3_final_csv.csv")

# Where processed CSV and saved models go
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

PROCESSED_CSV = os.path.join(STORAGE_DIR, "processed_dataset.csv")
MODEL_PATH = os.path.join(STORAGE_DIR, "biomass_model.joblib")
SCALER_PATH = os.path.join(STORAGE_DIR, "scaler.joblib")
LOG_CSV = os.path.join(STORAGE_DIR, "sensor_log.csv")

# Serial config (adjust per your machine)
SERIAL_PORT = "COM3"     # Windows example. Change to '/dev/ttyUSB0' on Linux
SERIAL_BAUDRATE = 9600
SERIAL_TIMEOUT = 1.0

# Server settings
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True
