# Phase 1 Execution Checklist (Weeks 1-4)

## Objective
Lock a reproducible, leakage-safe 15-class pipeline before full model benchmarking.

## 1) Environment and Repo Setup
- [x] Confirm Python version and virtual environment are active.
- [x] Install dependencies from pinned requirements.
- [x] Verify `src` imports work locally.
- [x] Verify dataset root resolution (`DATASETS_DIR`) on local machine.

## 2) Dataset Integrity Audit
- [x] Verify all expected PlantVillage class folders exist.
- [x] Count images per folder and flag empty folders.
- [x] Detect unreadable/corrupt images.
- [x] Detect exact duplicates (file hash).
- [x] Detect near-duplicates (dHash-based), especially across splits/classes.
- [x] Save integrity report artifact to `results`.

## 3) Frozen Split Generation
- [x] Run split generation script from repo root:
  - `py -3.13 -m src.prepare_splits`
- [x] Confirm train/val/test CSV files are produced in `CSV`.
- [x] Confirm leakage check passes.
- [x] Confirm class distributions are stratified and reasonable.
- [x] Confirm split manifest is written to:
  - `results/split_manifests/latest_split_manifest.json`

## 4) Artifact Logging Baseline
- [x] Ensure each run logs:
  - run name + timestamp
  - hyperparameters + seed
  - metrics
  - environment metadata
  - git commit hash
  - split manifest (CSV hashes + class counts)
- [x] Run one smoke training run and verify log JSON output in:
  - `results/experiment_logs`

## 5) Baseline Model Sanity Run
- [x] Train one lightweight baseline (for example ResNet18) for a short run.
- [x] Save model checkpoint and evaluation outputs.
- [x] Confirm confusion matrix and per-class metrics generation works.
- [x] Confirm rerun with same seed is stable (within expected variance).

## 6) Documentation During Execution
- [x] Keep a short lab log per session (date, change, result, next action).
- [x] Record anomalies and how they were resolved.
- [x] Draft 1-2 pages of methodology notes while executing.

## Go/No-Go Criteria to Enter Phase 2
- [x] Integrity audit complete and archived.
- [x] Frozen split manifest complete with hashes and seed.
- [x] Baseline training/evaluation end-to-end works.
- [x] Experiment logging fields complete and validated.
- [x] Phase 1 summary note written (what is stable, what is pending).

Verification note (2026-03-01):
1. Re-checked after external review; all six sections remain complete.

Verification note (2026-03-02):
1. Phase 1 sign-off formally completed (see `Markdown Files/phase1/phase1_signoff_claude.md`).
