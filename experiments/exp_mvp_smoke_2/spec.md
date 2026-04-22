# Experiment: exp_mvp_smoke_2

Status: prerelease experiment  
Purpose: parametric control check of FRACTURE decay.

---

## Goal

Test whether the decay of FRACTURE visibility observed in exp_mvp_smoke
is controllable via engine parameters.

This experiment modifies only one parameter:
- p_decay is increased from 0.99 to 0.995

All other parameters are identical.

---

## Method

- Run the MVP engine with identical setup to exp_mvp_smoke
- Compare FRACTURE visibility trends between the two runs

---

## Success Criterion

The experiment is successful if:
- the engine runs without error,
- minimal log validation passes,
- FRACTURE decay slope is less negative than in exp_mvp_smoke.

---

## Notes

This is still not a physical hypothesis test.
It is a control experiment establishing parameter sensitivity.

End of spec