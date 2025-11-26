# backend/utils/serial_reader.py
import serial, threading, time, traceback, os, pandas as pd
from datetime import datetime
import config

latest = {
    "pH": None, "temperature": None, "turbidity": None, "dissolved_oxygen": None,
    "source": None, "timestamp": None
}

def append_log(row: dict):
    log_file = config.LOG_CSV
    df = pd.DataFrame([row])
    if not os.path.exists(log_file):
        df.to_csv(log_file, index=False)
    else:
        df.to_csv(log_file, mode="a", header=False, index=False)

def serial_thread():
    try:
        ser = serial.Serial(config.SERIAL_PORT, config.SERIAL_BAUDRATE, timeout=config.SERIAL_TIMEOUT)
        print("[serial] opened", config.SERIAL_PORT)
    except Exception as e:
        print("[serial] could not open port:", e)
        return

    while True:
        try:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                time.sleep(0.1)
                continue
            # Expect csv: pH,temperature,turbidity,do  (do optional)
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 3:
                try:
                    pH = float(parts[0]); temp = float(parts[1]); turb = float(parts[2])
                    do = float(parts[3]) if len(parts) > 3 else None
                    ts = datetime.utcnow().isoformat()
                    latest.update({"pH":pH, "temperature":temp, "turbidity":turb, "dissolved_oxygen":do, "source":"serial", "timestamp":ts})
                    append_log({"timestamp":ts, "source":"serial", "pH":pH, "temperature":temp, "turbidity":turb, "dissolved_oxygen":do})
                    print("[serial] logged", pH, temp, turb, do)
                except ValueError:
                    print("[serial] parse error for line:", line)
            else:
                print("[serial] unexpected format:", line)
        except Exception:
            traceback.print_exc()
            time.sleep(1)

def start():
    t = threading.Thread(target=serial_thread, daemon=True)
    t.start()
    return t
