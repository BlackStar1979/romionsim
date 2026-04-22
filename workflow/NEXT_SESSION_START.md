# NEXT SESSION START — 2026-04-22

Purpose:
Give the smallest clean restart point for the next session.

---

## Current stopping point

- KROK 80 is complete
- result type: execution
- next active step: `KROK 81 — Initial Git Snapshot Plan`

---

## Files to open first

1. `workflow/PROJECT_WORKING_MEMORY.md`
2. `workflow/ENGINE_TEST_GRID.md`
3. `workflow/NEXT_SESSION_START.md`
4. `workflow/EXCLUSION_CONTRACT_PROMOTION_TRACK.md`
5. `conclusions/EXCLUSION_CONTRACT_PROMOTION_SYNTHESIS.md`
6. `workflow/GITHUB_REPOSITORY_PREPARATION_PLAN.md`
7. `workflow/LOCAL_GIT_BOOTSTRAP_INTERIM.md`
8. `workflow/WORKFLOW_CONSOLIDATION_AUDIT_2026-04-22_1759.md`

---

## What KROK 81 must do

- define the first local snapshot scope
- use the real current Git status as input
- treat the cleaned GitHub remote as prepared but still untouched by rebuilt local history
- stop before any import push
- close with a narrow repo-hygiene plan

---

## What KROK 81 must NOT do

- no remote replacement yet
- no push to GitHub yet
- no rewriting of canonical docs
- no destructive history cleanup

---

## Practical reminder

- broad searches should keep excluding `workflow/oldies/`
- after meaningful structural changes, run:

```powershell
python .\rebuild_project_map.py
```

---

End of restart note
