# services/executor/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import subprocess
import requests
import json
import datetime
import shutil

app = FastAPI(title="Executor Agent")


# -----------------------------
# Request schema
# -----------------------------
class ExecuteRequest(BaseModel):
    file_url: str
    script_path: str
    output_dir: str
    run_id: str


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "time": datetime.datetime.utcnow().isoformat() + "Z"
    }


# -----------------------------
# Utilities
# -----------------------------
def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def download_file(url: str, dest: Path):
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    dest.write_bytes(resp.content)


# -----------------------------
# Main execution endpoint
# -----------------------------
@app.post("/execute")
async def execute(req: ExecuteRequest):
    try:
        run_dir = Path(req.output_dir)
        ensure_dir(run_dir)

        # ---- Validate transform script ----
        script_path = Path(req.script_path)
        if not script_path.exists():
            raise HTTPException(
                status_code=400,
                detail=f"transform.py not found at {script_path}"
            )

        # ---- Download user dataset ----
        file_ext = req.file_url.split("?")[0].split(".")[-1].lower()
        if file_ext not in {"csv", "json", "xlsx"}:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}"
            )

        input_path = run_dir / f"input.{file_ext}"
        download_file(req.file_url, input_path)

        # ---- Prepare output path ----
        output_path = run_dir / "output.csv"

        # ---- Execute ETL ----
        cmd = [
            "python3",
            str(script_path),
            "",                     # plan_path ignored
            str(input_path),
            str(output_path)
        ]

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180
        )

        result = {
            "status": "success" if proc.returncode == 0 else "failed",
            "run_id": req.run_id,
            "input_file": str(input_path),
            "output_file": str(output_path),
            "stdout": proc.stdout,
            "stderr": proc.stderr
        }

        # ---- Persist executor logs ----
        log_path = run_dir / "executor_logs.json"
        log_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

        if proc.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"ETL execution failed:\n{proc.stderr}"
            )

        return result

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to download user file: {e}"
        )

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=500,
            detail="ETL execution timed out"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Executor failed: {e}"
        )
