import pandas as pd
import json
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--run_id")
args = parser.parse_args()

run_path = f"runs/{args.run_id}"

df = pd.read_csv(f"{run_path}/output_sample.csv")

quality_report = {
    "rows": len(df),
    "null_counts": df.isnull().sum().to_dict(),
    "duplicate_rows": int(df.duplicated().sum()),
    "schema_types": {col: str(df[col].dtype) for col in df.columns},
    "reward": None
}

# Simple reward
quality_report["reward"] = max(0, 1 - (quality_report["duplicate_rows"] / max(1, len(df))))

with open(f"{run_path}/quality_report.json", "w") as f:
    json.dump(quality_report, f, indent=2)

print("Evaluation complete.")
