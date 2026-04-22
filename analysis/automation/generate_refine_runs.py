from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]

SRC_RUN = ROOT / "experiments" / "exp_mvp_stability_sweep" / "runs" / "d0995_v020"
DST_RUNS = ROOT / "experiments" / "exp_mvp_stability_refine" / "runs"

P_DECAY = 0.995
W_VALUES = [
    0.018, 0.019, 0.020, 0.021, 0.022,
    0.023, 0.024, 0.025, 0.026, 0.027,
    0.028, 0.029, 0.030,
]

def main():
    if not SRC_RUN.exists():
        raise RuntimeError("Source run d0995_v020 does not exist")

    DST_RUNS.mkdir(parents=True, exist_ok=True)

    for w in W_VALUES:
        tag = f"d0995_v{int(w*1000):03d}"
        dst = DST_RUNS / tag

        print(f"[GEN] {tag}")

        if dst.exists():
            shutil.rmtree(dst)

        shutil.copytree(SRC_RUN, dst)

        params_path = dst / "params.json"
        params = json.load(open(params_path))

        params["extra"]["p_decay"] = P_DECAY
        params["extra"]["w_visible"] = w

        json.dump(params, open(params_path, "w"), indent=2)

    print("[OK] Refine runs generated")

if __name__ == "__main__":
    main()