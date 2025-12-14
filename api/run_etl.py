from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from requests.auth import HTTPBasicAuth
from api.results import router as results_router

app = FastAPI(title="ETL Trigger API")

app.include_router(results_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

KESTRA_URL = "http://localhost:8080/api/v1/main/executions/giri.etl/adaptive_etl_flow"

KESTRA_USERNAME = "srisankargiriv14@gmail.com"
KESTRA_PASSWORD = "Giri@2003"

class RunRequest(BaseModel):
    file_url: str

@app.post("/run-etl")
def run_etl(req: RunRequest):
    response = requests.post(
        KESTRA_URL,
        auth=HTTPBasicAuth(KESTRA_USERNAME, KESTRA_PASSWORD),
        files={
            "file_url": (None, req.file_url)
        },
        timeout=30,
    )

    response.raise_for_status()
    data = response.json()

    return {
        "execution_id": data["id"],
        "kestra_url": data.get("url"),
    }


from fastapi import HTTPException
import json
import os

@app.get("/runs/{run_id}/result")
def get_run_result(run_id: str):
    eval_path = f"runs/{run_id}/evaluation.json"

    if not os.path.exists(eval_path):
        raise HTTPException(status_code=404, detail="Evaluation not found")

    with open(eval_path, "r") as f:
        evaluation = json.load(f)

    return {
        "run_id": evaluation["run_id"],
        "quality_score": evaluation["quality_score"],
        "rows": evaluation["rows"],
        "columns": evaluation["columns"],
        "null_density": evaluation["null_density"],
        "status": evaluation["status"],
        "download_url": f"/runs/{run_id}/download"
    }

from fastapi.responses import FileResponse

@app.get("/runs/{run_id}/download")
def download_cleaned_csv(run_id: str):
    output_path = f"runs/{run_id}/output.csv"

    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="Output file not found")

    return FileResponse(
        output_path,
        media_type="text/csv",
        filename="cleaned_data.csv"
    )


@app.get("/health")
def health():
    return {"status": "ok"}
