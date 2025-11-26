import pandas as pd

# Load the ATP3 CSV
df = pd.read_csv(
    r"backend/storage/atp3_final_csv.csv",
    encoding="latin1",
    low_memory=False,
    dtype=str
)

print("\n=== COLUMN NAMES ===")
print(df.columns.tolist())

print("\n=== FIRST 10 ROWS ===")
print(df.head(10))

print("\n=== SAMPLE UNIQUE VALUES PER COLUMN ===")
for col in df.columns:
    print(f"\n[ {col} ]")
    vals = df[col].dropna().unique()
    print(vals[:5])
