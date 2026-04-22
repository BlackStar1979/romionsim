import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def extract_ticks(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [r for r in rows if r.get("type") == "TICK"]


def summarize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    meta = rows[0] if rows else {}
    params_ev = rows[1] if len(rows) > 1 else {}
    ticks = extract_ticks(rows)
    end = rows[-1] if rows else {}

    n_ticks = len(ticks)

    def series(field_path: Tuple[str, ...]) -> List[float]:
        out: List[float] = []
        for t in ticks:
            cur: Any = t
            ok = True
            for k in field_path:
                if not isinstance(cur, dict) or k not in cur:
                    ok = False
                    break
                cur = cur[k]
            if ok:
                try:
                    out.append(float(cur))
                except Exception:
                    pass
        return out

    visible_ratio = series(("fracture", "visible_ratio"))
    visible_edges = series(("fracture", "visible_edges"))
    total_weight = series(("core", "total_weight"))
    mean_pressure = series(("core", "mean_pressure"))

    def first_last(xs: List[float]) -> Tuple[Optional[float], Optional[float]]:
        if not xs:
            return None, None
        return xs[0], xs[-1]

    def slope(xs: List[float]) -> Optional[float]:
        if len(xs) < 2:
            return None
        return (xs[-1] - xs[0]) / float(len(xs) - 1)

    vr0, vrN = first_last(visible_ratio)
    ve0, veN = first_last(visible_edges)
    tw0, twN = first_last(total_weight)
    mp0, mpN = first_last(mean_pressure)

    out: Dict[str, Any] = {
        "schema_version": meta.get("schema_version"),
        "run_ok": bool(end.get("ok", False)),
        "n_ticks": n_ticks,
        "params": params_ev.get("params", {}),
        "fracture": {
            "visible_ratio_start": vr0,
            "visible_ratio_end": vrN,
            "visible_ratio_slope": slope(visible_ratio),
            "visible_edges_start": ve0,
            "visible_edges_end": veN,
            "visible_edges_slope": slope(visible_edges),
        },
        "core": {
            "total_weight_start": tw0,
            "total_weight_end": twN,
            "total_weight_slope": slope(total_weight),
            "mean_pressure_start": mp0,
            "mean_pressure_end": mpN,
            "mean_pressure_slope": slope(mean_pressure),
        },
        "end": end,
    }

    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="MVP log reader and summarizer")
    ap.add_argument("--log", required=True, help="Path to simulation_*.jsonl")
    ap.add_argument("--out-json", default=None, help="Optional path to save summary JSON")
    args = ap.parse_args()

    log_path = Path(args.log)
    if not log_path.exists():
        print("FAIL: log file not found")
        print(str(log_path))
        return 2

    rows = read_jsonl(log_path)
    s = summarize(rows)

    print("OK: log summary")
    print("schema_version:", s.get("schema_version"))
    print("run_ok:", s.get("run_ok"))
    print("n_ticks:", s.get("n_ticks"))

    fr = s["fracture"]
    cr = s["core"]

    print("fracture.visible_ratio_start:", fr["visible_ratio_start"])
    print("fracture.visible_ratio_end:", fr["visible_ratio_end"])
    print("fracture.visible_ratio_slope:", fr["visible_ratio_slope"])

    print("fracture.visible_edges_start:", fr["visible_edges_start"])
    print("fracture.visible_edges_end:", fr["visible_edges_end"])
    print("fracture.visible_edges_slope:", fr["visible_edges_slope"])

    print("core.total_weight_start:", cr["total_weight_start"])
    print("core.total_weight_end:", cr["total_weight_end"])
    print("core.total_weight_slope:", cr["total_weight_slope"])

    print("core.mean_pressure_start:", cr["mean_pressure_start"])
    print("core.mean_pressure_end:", cr["mean_pressure_end"])
    print("core.mean_pressure_slope:", cr["mean_pressure_slope"])

    if args.out_json:
        out_path = Path(args.out_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(s, f, indent=2, ensure_ascii=False)
        print("saved:", str(out_path))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())