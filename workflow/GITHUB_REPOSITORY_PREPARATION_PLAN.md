# GITHUB REPOSITORY PREPARATION PLAN

Purpose:
Prepare the rebuilt local project
to become the clean source of truth
before replacing the old remote state on GitHub.

Current local state:
- local `.git` directory now exists
- local `.gitignore` now exists
- the rebuilt project already has restart notes,
  workflow memory, validation scripts, and staged conclusions
  that should be preserved in version history

Target remote:
- `BlackStar1979/romionsim`

This plan does NOT push anything yet.
This plan does NOT modify the remote repository yet.

Execution status update — 2026-04-22:
- local `.gitignore` now exists
- local Git has been initialized in `C:\Work\romionsim`
- old remote state has been preserved:
  - locally as mirror and readable checkout archives under `C:\Work\github_remote_archives\`
  - remotely on branch `archive/pre-rebuild-2026-04-22`
- remote `main` has been cleared to a placeholder README
  so the rebuilt local repository can later replace it intentionally
- first clean local snapshot commit now exists:
  - `f4584f9` — `Initial rebuilt repository snapshot`
- controlled import has now been executed successfully:
  - remote `main` -> `ee9d8e3`
  - archive branch preserved -> `a94ad051`
- the next Git-related blocker is no longer remote cleanup,
  local capture, or first import,
  but short post-import audit and upstream hygiene

---

## 1. PREP GOAL

The goal is not only to "upload files".

The goal is to prepare:
- a clean local repository history,
- a safe first snapshot,
- and a controlled replacement path for the old remote state.

That means:
- local Git first,
- remote replacement second.

---

## 2. REQUIRED LOCAL PREPARATION

Before any push:

1. initialize local Git in `C:\Work\romionsim`
2. add a minimal `.gitignore`
3. review whether any generated or local-only artifacts should stay untracked
4. make the first clean snapshot commit
5. verify that the local tree matches the intended source-of-truth scope

Minimal `.gitignore` should likely cover:
- `__pycache__/`
- `*.pyc`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- temporary lock or local environment files if introduced later

It should NOT blindly exclude:
- workflow notes
- conclusions
- validation scripts
- canonical experiment metadata

Those are part of the rebuilt project state.

---

## 3. REQUIRED REMOTE PREPARATION

Before replacing the old GitHub state:

1. confirm that `BlackStar1979/romionsim` is the intended target
2. preserve old remote state as archive reference
3. choose the replacement strategy:
   - archive old repository and push into a clean new default branch
   - or replace `main` only after a local snapshot is confirmed

Preferred safe direction:
- keep old remote history reachable,
- but treat the rebuilt local repository
  as the only future source of truth.

---

## 4. MINIMAL SAFE SEQUENCE

Recommended operational order:

1. create local `.gitignore`
2. initialize local Git
3. create first local commit:
   `rebuild snapshot before GitHub replacement`
4. inspect what would be pushed
5. only then connect to the remote
6. archive or freeze the old remote state
7. push the rebuilt repository intentionally

This avoids mixing:
- old remote chaos
- with new local recovery work

---

## 5. WHAT MUST NOT HAPPEN

Do NOT:
- connect the local tree to the old remote before the first clean local snapshot
- inherit old remote structure as if it were still authoritative
- delete the old remote state before confirming the rebuilt snapshot exists locally
- push generated clutter because `.gitignore` was skipped

---

## 6. RECOMMENDED NEXT GIT-RELATED ACTION

The next honest move is now:
- confirm that local workflow memory
  and remote-published state are aligned
- close one short post-import audit
- then decide the next upstream hygiene step

This should still happen as a dedicated small step,
not mixed into engine semantics work.

---

End of plan
