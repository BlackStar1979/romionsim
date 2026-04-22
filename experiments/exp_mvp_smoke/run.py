import json
from pathlib import Path

from engine.api.engine import EngineParams, RomionEngine


def main() -> int:
    base_dir = Path(__file__).resolve().parent
    params_path = base_dir / "params.json"
    out_dir = base_dir / "raw_logs"

    if not params_path.exists():
        print("ERROR: params.json not found")
        print(str(params_path))
        return 1

    out_dir.mkdir(parents=True, exist_ok=True)

    with open(params_path, "r", encoding="utf-8") as f:
        params_dict = json.load(f)

    # This wrapper is intentionally tolerant at load time so that MVP runs
    # fail inside the engine's explicit validation layer, which also logs
    # the final normalized parameter set used for the run.
    params = EngineParams(
        seed=int(params_dict.get("seed", 0)),
        n_nodes=int(params_dict.get("n_nodes", 0)),
        ticks=int(params_dict.get("ticks", 0)),
        spawn_scale=float(params_dict.get("spawn_scale", 1.0)),
        decay_scale=float(params_dict.get("decay_scale", 1.0)),
        w_max=params_dict.get("w_max", None),
        extra=dict(params_dict.get("extra", {})),
    )

    engine = RomionEngine(params)
    artifacts = engine.run(out_dir=str(out_dir))

    print("OK: run finished")
    print("run_id:", artifacts.run_id)
    print("log_path:", artifacts.log_path)
    if artifacts.summary:
        print("summary:", json.dumps(artifacts.summary, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
