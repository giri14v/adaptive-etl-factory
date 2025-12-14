import subprocess
import json
import sys
import os

def generate_code(plan_path, output_path):
    cmd = [
        "cline", "generate",
        "--spec", plan_path,
        "--lang", "python",
        "--output", output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr

if __name__ == "__main__":
    plan = sys.argv[1]
    out = sys.argv[2]
    print(generate_code(plan, out))
