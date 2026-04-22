from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
N_TAIL = 20

TARGET_CSVS = [
    ROOT / "experiments" / "exp_mvp_stability_sweep" / "analysis" / "stability_table_auto.csv",
    ROOT / "experiments" / "exp_mvp_stability_refine" / "analysis" / "stability_table_auto.csv",
]


def read_visible_ratio_series(log_path: Path) -> List[float]:
    values: List[float] = []
    with log_path.open("r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            if obj.get("type") != "TICK":
                continue
            values.append(float(obj["fracture"]["visible_ratio"]))
    return values


def tail_mean_visible_ratio(log_path: Path, n_tail: int) -> float:
    values = read_visible_ratio_series(log_path)
    if not values:
        raise RuntimeError(f"No TICK events in {log_path}")
    tail = values[-n_tail:] if len(values) >= n_tail else values
    return sum(tail) / float(len(tail))


def newest_log_in_run(run_dir: Path) -> Path:
    raw_dir = run_dir / "raw_logs"
    logs = sorted(
        raw_dir.glob("simulation_*.jsonl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not logs:
        raise RuntimeError(f"No simulation log found in {raw_dir}")
    return logs[0]


def make_run_tag(row: Dict[str, str]) -> str:
    p_decay = row["p_decay"]
    w_visible = float(row["w_visible"])
    return f"d{str(p_decay).replace('.', '')}_v{int(w_visible * 1000):03d}"


def update_csv(csv_path: Path) -> None:
    if not csv_path.exists():
        print(f"[SKIP] Missing CSV: {csv_path}")
        return

    rows: List[Dict[str, str]] = []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        for row in reader:
            rows.append(dict(row))

    column = f"tail_mean_visible_ratio_N{N_TAIL}"
    if column not in fieldnames:
        fieldnames.append(column)

    experiment_dir = csv_path.parents[1]
    runs_dir = experiment_dir / "runs"

    for row in rows:
        run_tag = make_run_tag(row)
        run_dir = runs_dir / run_tag
        if not run_dir.exists():
            raise RuntimeError(f"Missing run directory for tag {run_tag}: {run_dir}")
        log_path = newest_log_in_run(run_dir)
        row[column] = str(tail_mean_visible_ratio(log_path, N_TAIL))

    tmp_path = csv_path.with_suffix(".tmp")
    with tmp_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    tmp_path.replace(csv_path)
    print(f"[OK] Updated {csv_path}")


def main() -> None:
    for csv_path in TARGET_CSVS:
        update_csv(csv_path)


if __name__ == "__main__":
    main()
