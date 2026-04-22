from pathlib import Path
import subprocess
import json
import csv

# ========= CONFIG =========

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / "experiments" / "exp_mvp_stability_sweep"
RUNS_DIR = EXPERIMENT / "runs"
ANALYSIS_DIR = EXPERIMENT / "analysis"

THETA = 0.1

PARAM_GRID = [
    (0.99,  0.015),
    (0.99,  0.02),
    (0.99,  0.03),
    (0.995, 0.015),
    (0.995, 0.02),
    (0.995, 0.03),
    (0.999, 0.015),
    (0.999, 0.02),
    (0.999, 0.03),
]

# ========= HELPERS =========

def run_validate(module_path: str):
    subprocess.run(
        ["python", "-m", module_path],
        cwd=ROOT,
        check=True
    )

def compute_t_survival(log_path: Path, theta: float):
    last_ok_tick = None
    with log_path.open() as f:
        for line in f:
            obj = json.loads(line)
            if obj.get("type") != "TICK":
                continue
            vr = obj["fracture"]["visible_ratio"]
            tick = obj["tick"]
            if vr >= theta:
                last_ok_tick = tick
            else:
                break
    return last_ok_tick

# ========= MAIN =========

def main():
    ANALYSIS_DIR.mkdir(exist_ok=True)

    out_csv = ANALYSIS_DIR / "stability_table_auto.csv"

    rows = []

    for p_decay, w_visible in PARAM_GRID:
        tag = f"d{str(p_decay).replace('.', '')}_v{int(w_visible*1000):03d}"
        run_dir = RUNS_DIR / tag

        module = f"experiments.exp_mvp_stability_sweep.runs.{tag}.validate"

        print(f"[RUN] {tag}")
        run_validate(module)
        
        # --- generate summary.json if missing ---
        summary_path = run_dir / "analysis" / "summary.json"
        if not summary_path.exists():
            (run_dir / "analysis").mkdir(exist_ok=True)

            logs = list((run_dir / "raw_logs").glob("simulation_*.jsonl"))
            if not logs:
                raise RuntimeError(f"No log file for {tag}")

            subprocess.run(
                [
                    "python",
                    str(ROOT / "analysis" / "mvp_read_log.py"),
                    "--log",
                    str(logs[0]),
                    "--out-json",
                    str(summary_path),
                ],
                check=True,
                cwd=ROOT,
            )

        logs = list((run_dir / "raw_logs").glob("simulation_*.jsonl"))
        if not logs:
            raise RuntimeError(f"No log found for {tag}")
        log_path = logs[0]

        t_survival = compute_t_survival(log_path, THETA)

        summary = json.load(open(run_dir / "analysis" / "summary.json"))
        run_id = summary["end"]["run_id"]
        final_vr = summary["end"]["summary"]["final_visible_ratio"]

        rows.append([
            p_decay,
            w_visible,
            THETA,
            t_survival,
            final_vr,
            run_id
        ])

    with out_csv.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "p_decay",
            "w_visible",
            "theta",
            "T_survival",
            "final_visible_ratio",
            "run_id"
        ])
        writer.writerows(rows)

    print(f"[OK] Written {out_csv}")

if __name__ == "__main__":
    main()