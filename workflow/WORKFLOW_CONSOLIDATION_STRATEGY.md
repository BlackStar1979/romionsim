# WORKFLOW CONSOLIDATION STRATEGY

Purpose:
Reduce workflow fragmentation
without losing restart safety,
auditability,
or staged reasoning history.

Reason:
The current `workflow/` layer has remained functional,
but Stage 5 has created a chain of micro-plans and micro-notes
that is now costly to keep mentally active.

This strategy is intentionally small.
It does NOT redesign the whole process.

---

## 1. WHAT MUST STAY CENTRAL

These files remain the core operational surface:

1. `workflow/PROJECT_WORKING_MEMORY.md`
2. `workflow/NEXT_SESSION_START.md`
3. `workflow/ENGINE_TEST_GRID.md`
4. `workflow/EXPERIMENT_WORKFLOW.md`

Rule:
Daily work should be restartable from these files alone.

---

## 2. WHAT IS NOW TOO FRAGMENTED

The main fragmentation problem is not all of `workflow/`.
It is the recent micro-chain inside Stage 5 contract-promotion work:

- `EXCLUSION_NARROW_CONTRACT_PROPOSAL_PLAN.md`
- `EXCLUSION_CONTRACT_PATCH_CANDIDATE_PLAN.md`
- `EXCLUSION_CANONICAL_PATCH_GATE_PLAN.md`
- `EXCLUSION_HUMAN_REVIEW_PACKET_PLAN.md`
- `EXCLUSION_REVIEW_HANDOFF_PLAN.md`

and the matching interim notes in `conclusions/`.

Each file made local sense,
but together they now create:
- too many adjacent micro-decisions,
- too many things that "should still be read",
- and too much risk that a file becomes historically true
  but operationally forgotten.

---

## 3. CONSOLIDATION TARGET

After the current micro-passage is finished,
consolidate the Stage 5 contract-promotion chain into:

1. one workflow tracker file
   `workflow/EXCLUSION_CONTRACT_PROMOTION_TRACK.md`
2. one conclusions synthesis file
   `conclusions/EXCLUSION_CONTRACT_PROMOTION_SYNTHESIS.md`

The old micro-files should remain preserved,
but they should stop being part of the active reading path.

---

## 4. NEW ACTIVE-READING RULE

At any given time,
the active reading path should contain only:

- the four central workflow files,
- one current plan file,
- one current conclusion/interim file,
- optional most-recent audit file if needed.

Everything else becomes:
- historical support material,
not
- mandatory active context.

---

## 5. WHEN TO CONSOLIDATE

Do NOT consolidate in the middle of a still-moving micro-step.

Do consolidate when:
- the current review-handoff micro-passage is complete,
- or when the next step would otherwise create yet another near-duplicate plan file.

That means:
- finish the present handoff lane first,
- then consolidate before opening a new family of micro-files.

---

## 6. WHAT TO AVOID

Do NOT:
- collapse all workflow history into one huge file
- delete useful step history
- remove restart notes or audits
- turn consolidation into a second project

The goal is:
- smaller active surface,
- preserved history,
- cleaner restart behavior.

---

## 7. RECOMMENDED NEXT PROCESS STEP

Recommended process move after the current handoff lane:
- `KROK 78 — Workflow Consolidation Plan`

That step should:
- define the exact consolidation boundary
- list which Stage 5 micro-files leave the active reading path
- keep all historical files preserved

---

End of strategy
