from pathlib import Path
import subprocess
import json
import csv

# ========= CONFIG =========

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / "experiments" / "exp_mvp_stability_refine"
RUNS_DIR = EXPERIMENT / "runs"
ANALYSIS_DIR = EXPERIMENT / "analysis"

THETA = 0.1

PARAM_GRID = [
    (0.995, 0.018),
    (0.995, 0.019),
    (0.995, 0.020),
    (0.995, 0.021),
    (0.995, 0.022),
    (0.995, 0.023),
    (0.995, 0.024),
    (0.995, 0.025),
    (0.995, 0.026),
    (0.995, 0.027),
    (0.995, 0.028),
    (0.995, 0.029),
    (0.995, 0.030),
]

# ========= HELPERS =========

def run_validate(module_path: str) -> None:
    subprocess.run(
        ["python", "-m", module_path],
        cwd=ROOT,
        check=True,
    )


def compute_t_survival(log_path: Path, theta: float):
    """
    Return last tick t for which visible_ratio >= theta for all ticks up to t.
    If the first TICK already violates, returns None.
    """
    last_ok_tick = None
    with log_path.open("r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            if obj.get("type") != "TICK":
                continue
            vr = obj["fracture"]["visible_ratio"]
            tick = int(obj["tick"])
            if vr >= theta:
                last_ok_tick = tick
            else:
                break
    return last_ok_tick


def newest_log_file(raw_dir: Path) -> Path:
    logs = sorted(
        raw_dir.glob("simulation_*.jsonl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not logs:
        raise RuntimeError(f"No log found in {raw_dir}")
    return logs[0]


def ensure_summary_json(run_dir: Path, log_path: Path) -> Path:
    summary_path = run_dir / "analysis" / "summary.json"
    if summary_path.exists():
        return summary_path

    (run_dir / "analysis").mkdir(exist_ok=True)

    subprocess.run(
        [
            "python",
            str(ROOT / "analysis" / "mvp_read_log.py"),
            "--log",
            str(log_path),
            "--out-json",
            str(summary_path),
        ],
        cwd=ROOT,
        check=True,
    )
    return summary_path


# ========= MAIN =========

def main() -> None:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

    out_csv = ANALYSIS_DIR / "stability_table_auto.csv"

    rows = []

    for p_decay, w_visible in PARAM_GRID:
        tag = f"d{str(p_decay).replace('.', '')}_v{int(w_visible * 1000):03d}"
        run_dir = RUNS_DIR / tag

        module = f"experiments.exp_mvp_stability_refine.runs.{tag}.validate"

        print(f"[RUN] {tag}")
        run_validate(module)

        raw_dir = run_dir / "raw_logs"
        log_path = newest_log_file(raw_dir)

        summary_path = ensure_summary_json(run_dir, log_path)
        summary = json.load(open(summary_path, "r", encoding="utf-8"))

        t_survival = compute_t_survival(log_path, THETA)

        run_id = summary["end"]["run_id"]
        final_vr = summary["end"]["summary"]["final_visible_ratio"]

        rows.append([
            p_decay,
            w_visible,
            THETA,
            t_survival,
            final_vr,
            run_id,
        ])

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "p_decay",
            "w_visible",
            "theta",
            "T_survival",
            "final_visible_ratio",
            "run_id",
        ])
        writer.writerows(rows)

    print(f"[OK] Written {out_csv}")


if __name__ == "__main__":
    main()