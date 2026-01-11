import json

with open('C:/Work/romionsim/tests/sweep_decay_inprocess/results/d0.7_s42/simulation.jsonl') as f:
    graphs = [json.loads(ln) for ln in f if 'GRAPH' in ln]

if graphs:
    last = graphs[-1]
    print(f"Last GRAPH: tick {last['tick']}, edges: {len(last['edges'])}")
    print(f"Total GRAPH dumps: {len(graphs)}")
