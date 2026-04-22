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


def fail(msg: str) -> Tuple[bool, str]:
    return False, msg


def ok(msg: str) -> Tuple[bool, str]:
    return True, msg


def validate_minimal_log(rows: List[Dict[str, Any]]) -> Tuple[bool, str]:
    if not rows:
        return fail("empty log")

    first = rows[0]
    if first.get("type") != "METADATA":
        return fail("first event must be METADATA")
    if "schema_version" not in first:
        return fail("METADATA must contain schema_version")
    if str(first.get("schema_version")) != "2.0":
        return fail("schema_version must be 2.0 for MVP logs")

    if len(rows) < 2:
        return fail("log must contain at least METADATA and PARAMS")

    second = rows[1]
    if second.get("type") != "PARAMS":
        return fail("second event must be PARAMS")
    if "params" not in second:
        return fail("PARAMS event must contain params dict")
    if not isinstance(second.get("params"), dict):
        return fail("PARAMS.params must be a dict")

    last = rows[-1]
    if last.get("type") != "END":
        return fail("last event must be END")
    if "ok" not in last:
        return fail("END event must contain ok field")
    if last.get("ok") is not True:
        reason = last.get("reason", "no reason provided")
        return fail("END.ok is false; reason: " + str(reason))

    # Validate tick sequence and required fields
    expected_tick = 0
    tick_events = 0
    for i, ev in enumerate(rows[2:], start=2):
        t = ev.get("type")
        if t == "END":
            # END must be last; if END occurs earlier, fail
            if i != len(rows) - 1:
                return fail("END event must be the final line")
            break

        if t != "TICK":
            return fail("unexpected event type at line " + str(i + 1) + ": " + str(t))

        if "tick" not in ev:
            return fail("TICK event missing tick field at line " + str(i + 1))
        try:
            tick_val = int(ev["tick"])
        except Exception:
            return fail("TICK.tick must be int at line " + str(i + 1))

        if tick_val != expected_tick:
            return fail("tick sequence broken at line " + str(i + 1) + ", expected " + str(expected_tick) + ", got " + str(tick_val))

        if "core" not in ev:
            return fail("TICK event missing core field at tick " + str(tick_val))
        if "fracture" not in ev:
            return fail("TICK event missing fracture field at tick " + str(tick_val))

        if not isinstance(ev.get("core"), dict):
            return fail("TICK.core must be dict at tick " + str(tick_val))
        if not isinstance(ev.get("fracture"), dict):
            return fail("TICK.fracture must be dict at tick " + str(tick_val))

        # Minimal fracture expectations
        fr = ev["fracture"]
        for k in ["visible_edges", "visible_weight", "visible_ratio"]:
            if k not in fr:
                return fail("fracture missing field " + k + " at tick " + str(tick_val))

        expected_tick += 1
        tick_events += 1

    if tick_events == 0:
        return fail("no TICK events found")

    return ok("ok: minimal log contract satisfied")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate minimal ROMION JSONL log (MVP contract)")
    ap.add_argument("--log", required=True, help="Path to simulation_*.jsonl")
    args = ap.parse_args()

    path = Path(args.log)
    if not path.exists():
        print("FAIL: log file not found")
        print(str(path))
        return 2

    try:
        rows = read_jsonl(path)
        valid, msg = validate_minimal_log(rows)
    except Exception as e:
        print("FAIL: exception while reading or validating log")
        print(str(e))
        return 3

    if valid:
        print("OK:", msg)
        return 0

    print("FAIL:", msg)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())