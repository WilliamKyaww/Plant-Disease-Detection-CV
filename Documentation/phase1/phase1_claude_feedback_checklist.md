# Phase 1 Closure Checklist (Based on Claude Opus Review)

Date created: 2026-03-01  
Source review: `Markdown Files/reviews/comprehensive_project_review.md`

## Purpose
Close the remaining Phase 1 risks identified in the external review before entering Phase 2 training runs.

---

## Must Fix Before Phase 2

- [x] 1. Record near-duplicate decision formally.
  - Action: Add a short written decision in `Markdown Files/docs/documentation.md` and `Markdown Files/docs/lab_log.md` explaining why integrity reported `Passed: False` (14 dHash near-duplicate pairs) and whether they are accepted false positives or require remediation.
  - Exit criterion: clear acceptance/remediation statement exists with date.
  - Status: completed on 2026-03-01 (policy recorded in both files).

- [x] 2. Fix scheduler compatibility in `src/training.py`.
  - Action: update scheduler stepping so `ReduceLROnPlateau` uses `scheduler.step(val_loss)` while other schedulers use `scheduler.step()`.
  - Exit criterion: no runtime failure when using `ReduceLROnPlateau`.
  - Status: completed on 2026-03-01 (code updated + direct smoke validation script passed).

- [x] 3. Run a real Colab smoke check once.
  - Action: run `src.colab_smoke` in actual Colab runtime and store resulting `latest_colab_smoke.json/.txt`.
  - Exit criterion: artifact indicates real Colab execution (`Executed in Colab: True`).
  - Status: completed on 2026-03-02 (artifact shows `executed_in_colab=true` and `passed=true`).

- [x] 4. Add class-imbalance mitigation option.
  - Action: add class-weighted loss support for training runs (for example inverse-frequency weights passed to `CrossEntropyLoss`), with toggle/config.
  - Exit criterion: documented and testable training path with weighted loss.
  - Status: completed on 2026-03-01 (`run_baseline_smoke --class-weighting inverse_frequency` implemented and executed).

- [x] 5. Convert artifact paths to repo-relative.
  - Action: replace absolute machine paths in manifests/metrics with project-relative paths where feasible.
  - Exit criterion: key artifacts are portable across machines without hardcoded local absolute paths.
  - Status: completed on 2026-03-01 for split manifest, integrity report, metrics snapshot, and experiment artifacts.

---

## Can Defer (Post-Phase 2 Start)

- [ ] Add `pytest` migration (`conftest.py`, `pytest.ini`) once test surface grows.
- [ ] Optimize near-duplicate scan complexity (current O(n^2) is acceptable for PlantVillage scale).
- [ ] Add split idempotency guard to skip regeneration if hashes already match manifest.
- [ ] Add `tqdm` progress wrapping in long training loops.
- [ ] Improve confusion matrix PNG labels for dissertation-quality figures.
- [ ] Remove `os.chdir(...)` side effect in `src.colab_smoke.py` (low risk currently).

---

## Already Verified as Complete (from current Phase 1 work)

- [x] Reproducible split manifest pipeline with hashes/seed/commit.
- [x] Integrity reporting artifacts (JSON + TXT) and near-duplicate detection implemented.
- [x] Script-based baseline smoke run with experiment logging artifacts.
- [x] Path portability hardening between Windows and Colab/Linux in dataset loading.
- [x] 01-03 notebooks aligned to `src`-based orchestration and schema.

---

## Cross-Review Assessment (Codex vs Claude)

This section documents where the external review is fully accepted, partially accepted, or accepted with scope caveats.

### Fully Agree (High Confidence)

1. Conditional Phase 1 pass is the correct verdict.
   - Reason: the engineering foundation is complete, but there are still formal closure and method-hardening tasks that should be done before claiming a clean Phase 2 launch.

2. Near-duplicate closure requires an explicit written decision.
   - Reason: `latest_integrity_report.json` currently records `passed=false` due to dHash near-pairs. Without a documented policy statement, the go/no-go decision appears inconsistent to an examiner.

3. Scheduler handling needed a defensive fix.
   - Reason: generic `scheduler.step()` can break for `ReduceLROnPlateau`, which requires a monitored metric (`val_loss`).

4. Class imbalance is a substantive Phase 2 risk.
   - Reason: class distribution is materially skewed, and this can reduce macro-F1 even if overall accuracy appears acceptable. Mitigation options must exist in training.

5. Absolute paths in artifacts reduce reproducibility portability.
   - Reason: machine-specific paths in manifests/logs are weak evidence for external replication and should be repo-relative where possible.

### Partially Agree (Context-Dependent / Priority-Dependent)

1. O(n^2) near-duplicate scan is technical debt, but not a current blocker.
   - Agreement: complexity is high in theory.
   - Partiality reason: PlantVillage scale remains manageable for current checks; optimization is lower priority than experiment rigor fixes.

2. Pytest migration is useful, but not required before Phase 2 starts.
   - Agreement: pytest improves ergonomics and scaling.
   - Partiality reason: existing `unittest` coverage already guards critical regression points for this phase.

3. `tqdm` usage and confusion matrix presentation are quality improvements, not gate criteria.
   - Agreement: both improve usability/reporting quality.
   - Partiality reason: they do not materially affect correctness, reproducibility, or validity of results.

4. Colab live run evidence is important, but execution is environment-constrained.
   - Agreement: a real Colab artifact strengthens portability claims.
   - Partiality reason: this item may require manual execution in external runtime; code-side preparation can be complete before that final artifact is produced.

### Net Position

1. Overall agreement with Claude review: approximately 85-90%.
2. Disagreement is mostly about execution order and what counts as a pre-Phase-2 blocker vs a deferred enhancement.
3. The review is directionally correct and materially useful for raising dissertation rigor.

---

## Validation Recap (2026-03-01)

1. Local validation commands passed:
   - `py -3.13 -m unittest discover -s tests`
   - `py -3.13 -m src.prepare_splits`
   - `py -3.13 -m src.integrity_report`
   - `py -3.13 -m src.run_baseline_smoke --epochs 1 --class-weighting inverse_frequency`
   - Direct `ReduceLROnPlateau` scheduler smoke check.
2. Remaining blocker from this checklist: none (all five must-fix items now complete).
