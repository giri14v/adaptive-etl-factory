# services/evaluator/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import pandas as pd
import json
import datetime

app = FastAPI(title="Evaluator Agent")


# -----------------------------
# Request schema
# -----------------------------
class EvaluateRequest(BaseModel):
    run_id: str
    output_dir: str


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "time": datetime.datetime.utcnow().isoformat() + "Z"
    }


# -----------------------------
# Main evaluation endpoint
# -----------------------------
@app.post("/evaluate")
async def evaluate(req: EvaluateRequest):
    try:
        run_dir = Path(req.output_dir)

        output_csv = run_dir / "output.csv"
        metrics_json = run_dir / "metrics.json"

        if not output_csv.exists():
            raise HTTPException(
                status_code=400,
                detail=f"output.csv not found in {run_dir}"
            )

        if not metrics_json.exists():
            raise HTTPException(
                status_code=400,
                detail=f"metrics.json not found in {run_dir}"
            )

        # Load data
        df = pd.read_csv(output_csv)
        base_metrics = json.loads(metrics_json.read_text())

        rows = int(len(df))
        cols = int(len(df.columns))
        nulls = int(df.isna().sum().sum())

        total_cells = max(rows * cols, 1)
        null_density = round(nulls / total_cells, 4)

        # Simple heuristic quality score
        quality_score = round(
            max(0.0, 1.0 - null_density),
            3
        )

        status = "success"
        if quality_score < 0.7:
            status = "warning"

        evaluation = {
            "run_id": req.run_id,
            "rows": rows,
            "columns": cols,
            "null_count": nulls,
            "null_density": null_density,
            "quality_score": quality_score,
            "status": status,
            "evaluated_at": datetime.datetime.utcnow().isoformat() + "Z"
        }

        # Persist evaluation
        eval_path = run_dir / "evaluation.json"
        eval_path.write_text(
            json.dumps(evaluation, indent=2),
            encoding="utf-8"
        )

        return evaluation

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation failed: {e}"
        )
