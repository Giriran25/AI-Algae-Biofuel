# backend/utils/wifi_client.py
# Example payload sender for ESP32/RPi POST requests (not executed on device here).
import requests, json

def push_data(server_url, payload):
    """
    server_url: e.g. "http://<host>:8000/api/wifi-data"
    payload: dict with pH, temperature, turbidity (optional), dissolved_oxygen (optional)
    """
    r = requests.post(server_url, json=payload, timeout=5)
    r.raise_for_status()
    return r.json()

# Example:
# push_data("http://192.168.1.20:8000/api/wifi-data", {"pH":7.8,"temperature":26.1,"turbidity":45.3,"dissolved_oxygen":8.2})
