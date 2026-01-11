import json

with open('C:/Work/romionsim/tests/test_c/results/R0_base/simulation.jsonl') as f:
    graphs = [json.loads(ln) for ln in f if 'GRAPH' in ln]

if graphs:
    g0 = graphs[0]
    print(f"Tick {g0['tick']}: {len(g0['edges'])} edges")
    
    # Check if nodes field exists
    if 'nodes' in g0:
        print(f"Nodes: {g0['nodes']}")
    else:
        # Infer from edges
        nodes = set()
        for u, v, w in g0['edges']:
            nodes.add(u)
            nodes.add(v)
        print(f"Nodes (inferred): {len(nodes)}")
