#!/usr/bin/env python3
"""
services/adapt/evolve.py

Lightweight adaptive engine (simulated-RL).
- Reads runs/<run_id>/quality_report.json
- Computes score and chooses next strategy (mean/mode/none)
- Updates policies/state.json and policies/history.json
- Optionally writes an updated plan (policies/next_plan.json)
- Safe, reproducible, no heavy ML deps
"""

import json
import argparse
import os
from datetime import datetime
from pathlib import Path
import statistics

parser = argparse.ArgumentParser()
parser.add_argument("--run_id", required=True)
parser.add_argument("--plans_dir", default="runs")   # where plans/output are stored
args = parser.parse_args()

RUNS_DIR = Path("runs")
POLICIES_DIR = Path("policies")
POLICIES_DIR.mkdir(parents=True, exist_ok=True)

run_id = args.run_id
run_path = RUNS_DIR / run_id
quality_path = run_path / "quality_report.json"

if not quality_path.exists():
    print(f"[evolve] quality_report.json not found for run {run_id} at {quality_path}")
    exit(1)

with quality_path.open() as f:
    report = json.load(f)

# score is assumed in report['reward']; if not present, compute a fallback score
score = report.get("reward")
if score is None:
    # fallback: use simple heuristic combining duplicates and null rates
    nulls = report.get("null_counts", {})
    null_rate = 0.0
    row_count = max(1, report.get("rows", 1))
    if isinstance(nulls, dict) and nulls:
        total_nulls = sum(nulls.values())
        null_rate = total_nulls / (row_count * max(1, len(nulls)))
    dup = report.get("duplicate_rows", 0)
    dup_rate = dup / max(1, row_count)
    # lower is better for dup_rate and null_rate -> convert to 0..1 reward
    score = max(0.0, 1.0 - (0.6 * null_rate + 0.4 * dup_rate))

score = float(score)
timestamp = datetime.utcnow().isoformat() + "Z"

# Decide next strategy using simple banding + exploration mutation
if score < 0.45:
    next_strategy = "mean"   # more aggressive numeric imputation
elif score < 0.7:
    next_strategy = "mode"   # categorical mode imputation
else:
    next_strategy = "none"   # no change

# Small exploration: occasionally try alternative strategy (1 in 8 runs)
try:
    # use run_id numeric entropy for light-weight randomness
    entropy = sum(ord(c) for c in run_id) % 8
except Exception:
    entropy = 0
if entropy == 0:
    alternative = {"mean": "mode", "mode": "mean", "none": "mode"}[next_strategy]
    next_strategy = alternative
    exploration = True
else:
    exploration = False

# Load previous state
state_path = POLICIES_DIR / "state.json"
history_path = POLICIES_DIR / "history.json"

state = {"last_run_id": None, "last_score": None, "next_strategy": None, "updated_at": None}
if state_path.exists():
    try:
        with state_path.open() as f:
            state = json.load(f)
    except Exception:
        pass

# Write next plan (mutate last plan if exists, otherwise write a simple plan)
next_plan = {}
last_plan_path = POLICIES_DIR / "last_plan.json"
if last_plan_path.exists():
    try:
        with last_plan_path.open() as f:
            last_plan = json.load(f)
        # mutate impute steps if present
        steps = last_plan.get("steps", [])
        for s in steps:
            if s.get("op") == "impute":
                s.setdefault("params", {})
                # set strategy for both numeric and categorical heuristically
                s["params"]["strategy"] = next_strategy
        next_plan = last_plan
    except Exception:
        next_plan = {}
else:
    # create a simple conservative plan template
    next_plan = {
        "dataset_id": run_id + "-next",
        "steps": [
            {"id": "parse_dates", "op": "parse_date", "columns": [], "params": {"formats": ["%Y-%m-%d", "%d-%m-%Y"]}},
            {"id": "impute", "op": "impute", "columns": [], "params": {"strategy": next_strategy}},
            {"id": "dedupe", "op": "deduplicate", "params": {"keys": []}}
        ],
        "confidence": 0.6
    }

# Save next plan & update policy state and history
state_update = {
    "last_run_id": run_id,
    "last_score": score,
    "next_strategy": next_strategy,
    "exploration": exploration,
    "timestamp": timestamp
}
with state_path.open("w") as f:
    json.dump(state_update, f, indent=2)

# Append history
history = []
if history_path.exists():
    try:
        with history_path.open() as f:
            history = json.load(f)
    except Exception:
        history = []

history_entry = {
    "run_id": run_id,
    "score": score,
    "next_strategy": next_strategy,
    "exploration": exploration,
    "timestamp": timestamp
}
history.append(history_entry)
with history_path.open("w") as f:
    json.dump(history, f, indent=2)

# Save next_plan for consumption by Planner for next run (optional)
next_plan_path = POLICIES_DIR / "next_plan.json"
with next_plan_path.open("w") as f:
    json.dump(next_plan, f, indent=2)

# Also save a copy as last_plan.json for future mutations
with last_plan_path.open("w") as f:
    json.dump(next_plan, f, indent=2)

print(f"[evolve] run={run_id} score={score:.3f} next_strategy={next_strategy} exploration={exploration}")
print(f"[evolve] wrote: {state_path}, {history_path}, {next_plan_path}")
