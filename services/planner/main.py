# services/planner/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Optional
from pathlib import Path
import pandas as pd
import json
import uuid
import datetime
from fastapi.responses import PlainTextResponse
app = FastAPI(title="Planner Agent")


# -----------------------------
# Request schema
# -----------------------------
class RowsPayload(BaseModel):
    rows: Optional[List[Dict]] = None


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "time": datetime.datetime.utcnow().isoformat() + "Z"
    }


@app.post("/plan")
async def plan(payload: RowsPayload):
    """
    Planner Agent
    - Always produces a plan.json on disk
    - Returns only plan_path (Kestra-safe)
    """

    run_id = str(uuid.uuid4())
    plan_path = Path(f"runs/{run_id}/plan.json")
    plan_path.parent.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------------------
    # Fallback mode: No rows provided
    # -----------------------------------------------------
    if not payload.rows:
        plan = {
            "dataset_id": "auto",
            "confidence": 0.75,
            "steps": [
                {
                    "id": "auto_parse_dates",
                    "op": "parse_date",
                    "columns": ["order_date"],
                    "params": {
                        "formats": ["%Y-%m-%d", "%d-%m-%Y"]
                    },
                }
            ],
        }

    # -----------------------------------------------------
    # Normal mode: Profile rows
    # -----------------------------------------------------
    else:
        df = pd.DataFrame(payload.rows)

        date_cols = [c for c in df.columns if "date" in c.lower()]
        impute_cols = df.columns[df.isnull().any()].tolist()

        steps = []

        if date_cols:
            steps.append(
                {
                    "id": "parse_dates",
                    "op": "parse_date",
                    "columns": date_cols,
                    "params": {
                        "formats": ["%Y-%m-%d", "%d-%m-%Y"]
                    },
                }
            )

        if impute_cols:
            steps.append(
                {
                    "id": "impute",
                    "op": "impute",
                    "columns": impute_cols,
                    "params": {
                        "strategy": "median"
                    },
                }
            )

        # Always deduplicate
        steps.append(
            {
                "id": "dedupe",
                "op": "deduplicate",
                "params": {
                    "keys": ["id"]
                },
            }
        )

        plan = {
            "dataset_id": "profiled",
            "confidence": 0.87,
            "steps": steps,
        }

    # -----------------------------------------------------
    # Persist plan to disk (CRITICAL)
    # -----------------------------------------------------
    plan_path.write_text(
        json.dumps(plan, indent=2),
        encoding="utf-8"
    )

    # -----------------------------------------------------
    # Return ONLY plan_path
    # -----------------------------------------------------
    return PlainTextResponse(
        content=str(plan_path),
        media_type="text/plain"
    )

