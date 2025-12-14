from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI(title="Evaluator Agent")

class EvalPayload(BaseModel):
    run_id: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/evaluate")
async def evaluate(payload: EvalPayload):
    run_folder = f"/workspace/runs/{payload.run_id}"
    os.makedirs(run_folder, exist_ok=True)
    report = {
        "run_id": payload.run_id,
        "score": 0.8,
        "metrics": {"missing_before": 10, "missing_after": 0}
    }
    with open(os.path.join(run_folder, "quality_report.json"), 'w') as f:
        json.dump(report, f)
    return report