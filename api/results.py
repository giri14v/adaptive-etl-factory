from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import json

router = APIRouter(prefix="/results", tags=["Results"])

BASE_RUNS_DIR = Path("runs")


@router.get("/{run_id}/metrics")
def get_metrics(run_id: str):
    run_dir = BASE_RUNS_DIR / run_id
    evaluation_file = run_dir / "evaluation.json"

    if not evaluation_file.exists():
        raise HTTPException(status_code=404, detail="Evaluation not found")

    with evaluation_file.open() as f:
        data = json.load(f)

    return data


@router.get("/{run_id}/output")
def download_output(run_id: str):
    run_dir = BASE_RUNS_DIR / run_id
    output_file = run_dir / "output.csv"

    if not output_file.exists():
        raise HTTPException(status_code=404, detail="Output CSV not found")

    return FileResponse(
        path=output_file,
        media_type="text/csv",
        filename=f"{run_id}_cleaned.csv"
    )
