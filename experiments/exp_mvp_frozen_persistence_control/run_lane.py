from pathlib import Path
import csv
import json
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = Path(__file__).resolve().parent
RUNS_DIR = EXPERIMENT / "runs"
ANALYSIS_DIR = EXPERIMENT / "analysis"
L_PERSIST = 20
RUN_TAGS = ["wb0200", "wb0225", "wb0250"]


def newest_log_file(raw_dir: Path) -> Path:
    logs = sorted(
        raw_dir.glob("simulation_*.jsonl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not logs:
        raise RuntimeError(f"No log file found in {raw_dir}")
    return logs[0]


def classify_log(log_path: Path) -> str:
    validator = ROOT / "validation" / "validate_frozen_persistence.py"
    cmd = [
        sys.executable,
        str(validator),
        "--log",
        str(log_path),
        "--mode",
        "evolving",
        "--l-persist",
        str(L_PERSIST),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stdout.strip() or proc.stderr.strip() or "validator failed")
    text = (proc.stdout or "").strip()
    if not text.startswith("OK:"):
        raise RuntimeError(f"unexpected validator output: {text}")
    return text.split(":", 1)[1].strip()


def read_params(run_dir: Path) -> dict:
    with (run_dir / "params.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def detect_transition(log_path: Path) -> bool:
    saw_active = False
    saw_frozen = False
    with log_path.open("r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            if obj.get("type") != "TICK":
                continue
            fracture = obj.get("fracture", {})
            regime = fracture.get("projection_regime")
            if regime in (None, "legacy_visible_only"):
                continue
            freeze_state = fracture.get("freeze_state")
            if freeze_state is False:
                saw_active = True
            elif freeze_state is True and saw_active:
                saw_frozen = True
                break
    return saw_active and saw_frozen


def main() -> None:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    out_csv = ANALYSIS_DIR / "control_lane_results.csv"
    rows = []

    for tag in RUN_TAGS:
        run_dir = RUNS_DIR / tag
        module = f"experiments.exp_mvp_frozen_persistence_control.runs.{tag}.validate"
        print(f"[RUN] {tag}")
        subprocess.run([sys.executable, "-m", module], cwd=ROOT, check=True)

        log_path = newest_log_file(run_dir / "raw_logs")
        classification = classify_log(log_path)
        params = read_params(run_dir)
        w_bridge = params["extra"]["w_bridge"]
        rows.append(
            [
                tag,
                w_bridge,
                L_PERSIST,
                classification,
                str(detect_transition(log_path)).lower(),
                str(log_path),
            ]
        )

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "tag",
                "w_bridge",
                "L_persist",
                "classification",
                "has_active_to_frozen_transition",
                "log_path",
            ]
        )
        writer.writerows(rows)

    print(f"[OK] Written {out_csv}")


if __name__ == "__main__":
    main()
