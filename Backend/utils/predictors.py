# backend/utils/predictors.py
import numpy as np
import joblib
import os
import config as C  # if used as package; else import config directly

# fallback model loader
def load_model(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found: {path}")
    return joblib.load(path)
    
#build_feature_vector
def build_feature_vector(input_dict, use_advanced=True):
    # always safe conversions
    def safe_float(x, default=np.nan):
        if x in (None, "", "null"):
            return default
        try:
            return float(x)
        except:
            return default

    pH = safe_float(input_dict.get("pH"), 7.5)
    temperature = safe_float(input_dict.get("temperature"), 25.0)
    turbidity = safe_float(input_dict.get("turbidity"), 0.0)
    do = safe_float(input_dict.get("dissolved_oxygen"), np.nan)

    if use_advanced:
        conductivity = safe_float(input_dict.get("conductivity"), np.nan)
        salinity = safe_float(input_dict.get("salinity"), np.nan)
        light_energy = safe_float(input_dict.get("light_energy"), np.nan)
        air_temperature = safe_float(input_dict.get("air_temperature"), temperature)
        depth_cm = safe_float(input_dict.get("depth_cm"), np.nan)

        return np.array([[pH, temperature, turbidity, do,
                          conductivity, salinity, light_energy,
                          air_temperature, depth_cm]])

    else:
        return np.array([[pH, temperature, turbidity, do]])

def predict(model, input_dict, use_advanced=True):
    X = build_feature_vector(input_dict, use_advanced=use_advanced)
    pred = model.predict(X)[0]
    return float(pred)
