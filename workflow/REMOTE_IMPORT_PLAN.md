# REMOTE IMPORT PLAN

Status:
Planning result for KROK 83.

Purpose:
Define the safest way
to import the rebuilt local repository
into the already cleaned GitHub remote.

---

## 1. CURRENT VERIFIED STATE

Local:
- local Git repository exists
- current snapshot commit:
  - `f4584f9` — `Initial rebuilt repository snapshot`
- current local branch:
  - `master`
- no remote is configured yet

Remote:
- target repository:
  - `BlackStar1979/romionsim`
- old remote state is preserved on:
  - `archive/pre-rebuild-2026-04-22`
- remote `main` is intentionally only a placeholder branch

This means:
- remote `main` is not authoritative
- local rebuilt history is authoritative

---

## 2. SAFEST IMPORT SHAPE

Recommended path:

1. add `origin` pointing to `BlackStar1979/romionsim`
2. rename local `master` to `main`
3. fetch remote refs for visibility only
4. verify that remote archive branch still exists
5. intentionally replace remote `main`
   with local `main`
6. verify resulting remote HEAD and repository contents

Important:
- this is a deliberate history replacement of placeholder `main`
- it is NOT a merge with the placeholder history

---

## 3. REQUIRED PUSH MODE

Because local rebuilt history
and remote placeholder history are unrelated,
the import push should be:
- intentional
- explicit
- replacement-style

Recommended push mode:
- `git push --force-with-lease origin main`

Reason:
- `main` was already cleared on purpose
- old state is preserved elsewhere
- `--force-with-lease` is safer than raw `--force`

---

## 4. WHAT MUST NOT HAPPEN

Do NOT:
- merge local rebuilt history into placeholder `main`
- delete the archive branch
- push from local `master` without first making branch naming explicit
- improvise the push from memory without first checking remote refs

---

## 5. NEXT HONEST MOVE

Execute the remote import in one controlled pass:
- add remote
- rename branch
- fetch and verify
- push rebuilt `main` intentionally
- verify the remote result

That should be the next dedicated Git step.

---

End of plan
