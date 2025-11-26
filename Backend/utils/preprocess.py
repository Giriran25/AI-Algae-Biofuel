# backend/utils/preprocess.py
import pandas as pd
import numpy as np
import os

def prepare_dataset(input_path, output_csv=None, verbose=True):
    if verbose:
        print("[preprocess] Reading raw ATP3 file...")

    # Read raw as a single column
    raw = pd.read_csv(input_path, header=None, encoding="latin1", low_memory=False, dtype=str)

    # Split into multiple columns
    df = raw[0].str.split(",", expand=True)
    if verbose:
        print(f"[preprocess] Parsed shape: {df.shape}")

    # ---- Extract header (row 0) ----
    header_raw = df.iloc[0].tolist()

    clean_header = []
    for h in header_raw:
        if h is None:
            clean_header.append("COLUMN")
        else:
            clean_header.append(str(h).strip().replace('"', ''))

    df = df.iloc[1:].reset_index(drop=True)

    # ---- Actual ATP3 header (29 columns) ----
    TRUE_HEADER = [
        'SiteID','ExperimentID','StrainID','SourceID','BatchID','Date','PondID','TreatmentID',
        'Harvest#','time (d)','Harvest Vol (L)','AFDW (g/L)','AFDW (g)','crash','Date_only','pH',
        'Temp (C)','Cond (mS.cm)','DO (mg.L)','DO (%sat)','Sal (g.L)','PAR (umol.m2.s)',
        'AirTemp(C)','RH(%)','GlobalLightEnergy(W.m2)','WindSpeed(km.hr)','WDir(deg)','Depth.cm'
    ]

    # ---- FINAL FIX: Match only min(cols, 29) without throwing errors ----
    cols_to_use = min(len(TRUE_HEADER), df.shape[1])
    df = df.iloc[:, :cols_to_use]
    df.columns = TRUE_HEADER[:cols_to_use]

    # ---- Select required columns ----
    KEEP = [
        'pH','Temp (C)','AFDW (g/L)','DO (mg.L)','Cond (mS.cm)',
        'Sal (g.L)','PAR (umol.m2.s)','AirTemp(C)','Depth.cm'
    ]

    available = [c for c in KEEP if c in df.columns]
    out = df[available].copy()

    # Convert numerically
    for c in available:
        out[c] = pd.to_numeric(out[c], errors="coerce")

    # Drop essential rows
    essential = [c for c in ['pH','Temp (C)','AFDW (g/L)'] if c in out.columns]
    out = out.dropna(subset=essential)

    # ---- Synthetic turbidity (with noise) ----
    if "AFDW (g/L)" in out.columns:
        b = out["AFDW (g/L)"]
        bmin, bmax = b.min(), b.max()
        brange = max(bmax - bmin, 1e-6)
        noise = np.random.normal(0, 5, size=len(out))
        out["turbidity"] = ((b - bmin) / brange * 100) + noise
    else:
        out["turbidity"] = 50  # fallback

    # ---- Rename to ML-friendly names ----
    rename_map = {
        "Temp (C)": "temperature",
        "AFDW (g/L)": "biomass",
        "DO (mg.L)": "dissolved_oxygen",
        "Cond (mS.cm)": "conductivity",
        "Sal (g.L)": "salinity",
        "PAR (umol.m2.s)": "light_energy",
        "AirTemp(C)": "air_temperature",
        "Depth.cm": "depth_cm"
    }
    out = out.rename(columns=rename_map)

    # Fill missing numeric values
    for col in out.columns:
        out[col] = out[col].fillna(out[col].median())

    print("[preprocess] Final cleaned shape:", out.shape)

    if output_csv:
        out.to_csv(output_csv, index=False)
        print(f"[preprocess] Saved cleaned CSV → {output_csv}")

    return out


if __name__ == "__main__":
    src = "backend/storage/atp3_final_csv.csv"
    out_csv = "backend/storage/processed_dataset.csv"
    prepare_dataset(src, output_csv=out_csv, verbose=True)
