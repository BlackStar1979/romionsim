# Analysis Tools

**Post-processing and metrics for ROMION simulations**

---

## 🔧 TOOLS:

### gravity_test (Main Analysis) ⭐
**Location:** `gravity_test/` package (modular) + `gravity_test.py` (wrapper)

**Purpose:** Analyze inter-cluster bridges (gravity-like field)

**Usage:**
```bash
python analysis/gravity_test.py \
  --log simulation.jsonl \
  --tick 400 \
  --wcluster 0.02 \
  --wbridge 0.0 \
  --wdist 0.005 \
  --wdist-mode threshold \
  --min-cluster-size 2
```

**Modules:**
- `io.py` - Load snapshots, parse params (63 lines)
- `clustering.py` - Component detection (138 lines)
- `metrics.py` - Bridge counting, hub analysis (246 lines)
- `distances.py` - All-pairs distances (111 lines)
- `main.py` - CLI and reporting (248 lines)

**Total:** ~815 lines (was 718 monolith)

**Why split:** Better maintainability, testability, reusability

---

### Other Tools:

**squid_spectral.py**
- SQUID topology test
- Spectral analysis
- Status: Spec only (not implemented)

**rolling_alpha.py**
- Time-series analysis
- Rolling window metrics

**verify_spark.py**
- Quantum Spark verification
- Check if derivable from theory

**soc_simple.py**
- Simple SOC analysis

---

## 📊 TYPICAL WORKFLOW:

### 1. Run Simulation:
```bash
python scripts/run_from_config.py cfg/decay_slow.cfg
```

### 2. Analyze Results:
```bash
python analysis/gravity_test.py \
  --log results_decay_slow/simulation.jsonl \
  --tick 400 \
  --wcluster 0.02
```

### 3. Batch Analysis:
```bash
python scripts/batch_test_c.py
```

---

## 🔍 METRICS EXPLAINED:

### Clustering:
- **Clusters:** Connected components @ wcluster threshold
- **Active clusters:** Clusters with inter-cluster bridges
- **Singletons:** Clusters with 1 node

### Bridges:
- **Pairs with bridges:** Number of cluster pairs connected
- **Total bridges:** Sum of all inter-cluster edges
- **Total weight:** Sum of bridge weights

### Hub:
- **Hub cluster:** Cluster with most connections
- **Hub degree:** Number of other clusters connected to hub
- **Hub share:** % of total connections going through hub
- **Coverage:** % of clusters that have bridges

### Range:
- **Max distance:** Longest path with bridges
- **Pattern:** Connectivity-only vs Distance-dependent

---

## 📝 NOTES:

### Version 2.0 Changes:
- Split into modular package
- Improved hub metrics (share of connections)
- Better error handling
- Backward compatible CLI

### Backup:
- Old monolith: `archive/gravity_test_monolith.py`
- Pre-split backup: `gravity_test_before_split.py`
- Pre-bug-fix: `gravity_test_backup_20260107.py`

---

**For details:** See `gravity_test/__init__.py`
