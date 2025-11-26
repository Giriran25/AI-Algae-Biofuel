# backend/model/test.py
import joblib, os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.predictors import predict, build_feature_vector
import config

def quick_test():
    model = joblib.load(config.MODEL_PATH)
    sample = {
        "pH": 8.0, "temperature": 26.0, "turbidity": 40.0, "dissolved_oxygen": 8.0,
        "conductivity": 5.0, "salinity": 30.0, "light_energy": 300.0, "air_temperature": 25.0, "depth_cm": 20.0
    }
    val = predict(model, sample, use_advanced=True)
    print("Prediction:", val)

if __name__ == "__main__":
    quick_test()
