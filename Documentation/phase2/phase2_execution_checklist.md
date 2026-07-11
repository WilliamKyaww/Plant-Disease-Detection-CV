# Phase 2 Execution Checklist (Core Modeling Benchmark)

Date created: 2026-03-02  
Status: Approved for implementation kickoff

## Objective
Build and run a rigorous 4-architecture, 3-seed benchmark on frozen 15-class splits with reproducible logging and Colab-first execution.

## Scope Lock (Phase 2 Only)
- [x] Primary task remains 15-class classification (no scope drift).
- [x] Architectures fixed for Phase 2:
  - ResNet18
  - ResNet50
  - EfficientNet-B0
  - ViT-Small (`vit_small_patch16_224`)
- [x] Seed protocol fixed at 3 seeds (`41,42,43`).
- [x] Default class imbalance handling fixed to `--class-weighting inverse_frequency`.
- [x] Frozen split policy enforced (no ad-hoc split regeneration for benchmark runs).

Reasoning:
1. Locks comparability and prevents silent protocol drift between models.
2. Keeps scope aligned with dissertation-grade empirical evaluation.

---

## Implementation Plan (Code Structure)

### A) Orchestrator Script
- [x] Create `src/run_phase2_benchmark.py` to orchestrate model x seed runs.
- [x] Add CLI arguments:
  - `--models`
  - `--seeds`
  - `--epochs`
  - `--batch-size`
  - `--lr-cnn`
  - `--lr-vit`
  - `--weight-decay`
  - `--class-weighting` (default: `inverse_frequency`)
  - `--scheduler` (`cosine`/`plateau`)
  - `--patience`
  - `--pretrained`
  - `--amp`
  - `--num-workers`
  - `--out-dir`
  - `--resume`

Reasoning:
1. Single script ensures one source of truth for protocol and reproducibility.
2. CLI keeps runs explicit and auditable.

### B) Model Registry
- [x] Create `src/model_registry.py`.
- [x] Implement `build_model(model_name, num_classes, pretrained=True)`.
- [x] Support all 4 target architectures with consistent classifier head replacement.

Reasoning:
1. Decouples model definitions from experiment logic.
2. Reduces copy-paste and model-specific branching in the benchmark script.

### C) Frozen Split Guard
- [x] Create `src/split_guard.py`.
- [x] Verify CSV hashes against `results/split_manifests/latest_split_manifest.json`.
- [x] Hard-fail benchmark if mismatch is detected.

Reasoning:
1. Prevents invalid comparisons caused by unintended split changes.

### D) Reporting Aggregator
- [x] Create `src/phase2_reporting.py`.
- [x] Write per-run table: `results/phase2/model_seed_metrics.csv`.
- [x] Write per-model summary: `results/phase2/model_summary_mean_std.csv`.
- [x] Write leaderboard: `results/phase2/leaderboard.csv`.

Reasoning:
1. Produces dissertation-ready analysis tables directly from artifacts.

---

## Training Protocol Enforcement
- [x] Use identical split files for all runs.
- [x] Use same transform family and image size for all models (document exceptions if any).
- [x] Keep early stopping and evaluation protocol consistent.
- [x] Log accuracy + macro F1 + per-class metrics + confusion matrix per run.
- [x] Record latency, parameter count, and model size per run.

Reasoning:
1. Fairness across architecture comparisons is mandatory for valid conclusions.

---

## Artifact and Logging Requirements
- [x] Save checkpoints per model/seed under `models/phase2/...`.
- [x] Save run metrics JSON under `results/phase2/runs/...`.
- [x] Save confusion matrix JSON/PNG per run.
- [x] Save experiment logs with:
  - git commit hash
  - split manifest hash
  - seed
  - environment metadata
  - key artifact hashes
- [x] Ensure paths remain repo-relative in all generated JSON artifacts.

Reasoning:
1. Keeps evidence reproducible and externally inspectable.

---

## Colab Execution (Primary)
- [x] Add `Google Colab/phase2_benchmark_runner.ipynb` as thin runner.
- [x] Notebook should only:
  - set repo root
  - install requirements
  - call script commands
  - avoid embedding training logic
- [x] Run at least one short dry-run in Colab before full sweep.

Reasoning:
1. Minimizes notebook drift and keeps code in `src`.
2. Reduces environment surprises before long runs.

---

## Validation and Gate to Continue Phase 2
- [x] Dry-run passes for all 4 models at 1 epoch x 1 seed.
- [x] Full 3-seed sweep starts without protocol errors.
- [x] Aggregation outputs are generated correctly.
- [x] No split-manifest mismatch or schema drift warnings.

## Phase 2 Completion Gate
- [x] All 4 models completed across 3 seeds (or fallback invocation documented).
- [x] Mean+std results table finalized.
- [ ] Statistical comparison run for top CNN vs top ViT.
- [ ] Phase 2 methodology + results draft written.

---

## Fallback Rules
- [ ] If ViT cost/time is prohibitive, document fallback and continue with stronger CNN depth analysis.
- [ ] If Colab runtime constraints block full sweep, prioritize completion of at least 3 models with full 3-seed rigor.

Reasoning:
1. Preserves dissertation quality under runtime constraints instead of stalling.

---

## Notes
1. This checklist is implementation-focused and complements `Markdown Files/plans/implementation_plan2_chatgpt_edited.md`.
2. Keep deviations explicit in `Markdown Files/docs/lab_log.md` and `Markdown Files/docs/documentation.md`.
3. Current implementation status:
   - `run_phase2_benchmark.py` is now modularized via:
     - `src/split_guard.py`
     - `src/phase2_reporting.py`
4. Update (2026-03-02):
   - Refactor completed: `run_phase2_benchmark.py` now imports and uses `src/split_guard.py` and `src/phase2_reporting.py`.
   - Local validations completed:
     - all-model dry-run (`--dry-run`)
     - 1-model smoke benchmark with sampled splits:
       - `--models resnet18 --seeds 41 --epochs 1 --max-train 256 --max-val 96 --max-test 96`
5. Update (2026-03-02, continued):
   - Added AMP-capable training path in `src/training.py` (`use_amp` flag, CUDA-only activation).
   - Enforced per-seed split reuse across all models in `src/run_phase2_benchmark.py` to guarantee split identity.
   - Added split hashes + model size logging in run metrics and experiment logs.
   - Completed local all-architecture non-dry smoke:
     - `--models resnet18,resnet50,efficientnet_b0,vit_small_patch16_224 --seeds 41 --epochs 1 --max-train 192 --max-val 96 --max-test 96`
6. Update (2026-03-06):
   - Live Colab dry-run executed successfully from `Google Colab/phase2_benchmark_runner.ipynb`.
   - Confirmed strict frozen-split behavior: notebook reported existing `latest_split_manifest.json` and skipped regeneration.
7. Update (2026-03-14):
   - Imported canonical `phase2_artifacts_export.zip` from Colab into local `results/phase2/`.
   - Full benchmark artifact set is now present locally for all 12 runs (`4 models x 3 seeds`).
   - Current leaderboard from `results/phase2/leaderboard.csv`:
     - `resnet18` first
     - `efficientnet_b0` second
     - `vit_small_patch16_224` third
     - `resnet50` fourth
   - Statistical comparison and dissertation write-up are still pending.
