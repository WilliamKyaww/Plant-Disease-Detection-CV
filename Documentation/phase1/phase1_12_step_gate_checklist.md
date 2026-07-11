# Phase 1: 12-Step Execution and Gate Checklist

Status legend:
1. Checked `[x]`: completed.
2. Unchecked `[ ]`: not fully completed yet (notes explain partial progress where relevant).

---

- [x] 1. Lock scope and terminology.
  Notes: 15-class primary + 4-disease side analysis + optional gated severity are locked in plan.

- [x] 2. Fix local runtime first.
  Notes: Completed with deviation. Standardized on Python 3.13 (`py -3.13`) instead of 3.11, with pinned requirements and a runner script.

- [x] 3. Run dataset integrity audit and save artifact.
  Notes: Dedicated artifact writer added (`src.integrity_report`) that saves JSON/TXT reports in `results/integrity_reports`.

- [x] 4. Upgrade duplicate check from exact-only to near-duplicate.
  Notes: Implemented dHash near-duplicate detection (Hamming distance threshold). Plan wording aligned to dHash.

- [x] 5. Generate/freeze splits from script, not notebook.
  Notes: `src.prepare_splits` is canonical and used by runner.

- [x] 6. Create split manifest artifact.
  Notes: Includes timestamp, seed, SHA256 hashes, class counts, and git commit.

- [x] 7. Harden path portability.
  Notes: Split CSV paths normalized; loader handles slash normalization and `Datasets/` prefix mapping.

- [x] 8. Deprecate stale notebook logic and use `src` only.
  Notes: 01-03 switched to thin `src` orchestrators; 04-06 explicitly deprecated until optional Phase 4.

- [x] 9. Create one minimal script-based baseline training run (1-2 epochs) with saved outputs.
  Notes: Implemented `src.run_baseline_smoke`; generated checkpoint, metrics snapshot, and experiment log artifacts.

- [x] 10. Integrate experiment logging fully in that baseline run.
  Notes: Baseline smoke run logs seed, git commit hash, split artifacts, and split manifest file hash via `ExperimentLog`.

- [x] 11. Colab path sanity pass + one Colab end-to-end smoke run evidence.
  Notes: Implemented `src.colab_smoke` + Colab notebook integration and generated smoke evidence artifacts (`results/colab_smoke/latest_*`).

- [x] 12. Phase 1 gate decision (hard stop before Phase 2).
  Notes: Formal gate sign-off completed on 2026-03-02 (see `Markdown Files/phase1/phase1_signoff_claude.md`).

---

## Current Completion Snapshot
1. Completed: 12/12
2. Pending: 0/12
3. Estimated Phase 1 completion: 100%
