# INITIAL GIT SNAPSHOT PLAN

Status:
Planning result for KROK 81.

Purpose:
Define the first clean local snapshot scope
before any push to the cleaned GitHub remote.

---

## 1. INPUT OBSERVED FROM REAL GIT STATUS

Current top-level untracked scope:
- `.gitignore`
- `.hermesignore`
- `analysis/`
- `conclusions/`
- `docs/`
- `engine/`
- `experiments/`
- `hypotheses/`
- `rebuild_project_map.py`
- `validation/`
- `workflow/`

This is structurally consistent
with the rebuilt repository as current source of truth.

---

## 2. CRITICAL SIZE FINDING

`workflow/oldies/` is archive-only
and currently occupies roughly `46.5 GB`.

That means:
- it must NOT enter the first local snapshot
- it must remain local reference material only
- it should stay excluded from both active reading
  and Git tracking

Operational decision:
- exclude `workflow/oldies/` in `.gitignore`
- preserve local availability only

---

## 3. FIRST SNAPSHOT SCOPE

Include in the first snapshot:
- `.gitignore`
- `.hermesignore`
- `analysis/`
- `conclusions/`
- `docs/`
- `engine/`
- `experiments/`
- `hypotheses/`
- `validation/`
- `workflow/` except `workflow/oldies/`
- `rebuild_project_map.py`

Reason:
- these files define the rebuilt theory-engine-workflow state
- they are the current source of truth
- they are already organized enough
  to support an intentional first repository history point

---

## 4. FIRST SNAPSHOT MUST NOT INCLUDE

Do NOT include:
- `workflow/oldies/`
- ignored caches and bytecode
- future local environment clutter if created later

Do NOT try to optimize history yet.
The first goal is clean capture,
not retroactive beautification.

---

## 5. RECOMMENDED FIRST COMMIT SHAPE

Recommended commit message:
- `Initial rebuilt repository snapshot`

This commit should mean:
- local rebuilt source of truth captured
- remote cleanup already completed separately
- import push still intentionally deferred

---

## 6. NEXT HONEST MOVE

Execute the first local snapshot commit
with the scope above,
then inspect repository state again
before any remote import action.

That should be the next dedicated Git step.

---

End of plan
