import json

# Check d0.5_s42
print("d0.5_s42:")
with open('C:/Work/romionsim/tests/sweep_decay_inprocess/results/d0.5_s42/simulation.jsonl') as f:
    lines = f.readlines()
    graphs = [json.loads(ln) for ln in lines if 'GRAPH' in ln]
    print(f"  Total lines: {len(lines)}")
    print(f"  GRAPH dumps: {len(graphs)}")
    if graphs:
        for g in graphs:
            print(f"    tick {g['tick']}: {len(g['edges'])} edges")

print("\nd0.5_s123:")
try:
    with open('C:/Work/romionsim/tests/sweep_decay_inprocess/results/d0.5_s123/simulation.jsonl') as f:
        lines = f.readlines()
        print(f"  Total lines: {len(lines)}")
except Exception as e:
    print(f"  ERROR: {e}")

# Compare with working run
print("\nd0.6_s42 (working):")
with open('C:/Work/romionsim/tests/sweep_decay_inprocess/results/d0.6_s42/simulation.jsonl') as f:
    lines = f.readlines()
    graphs = [json.loads(ln) for ln in lines if 'GRAPH' in ln]
    print(f"  Total lines: {len(lines)}")
    print(f"  GRAPH dumps: {len(graphs)}")
