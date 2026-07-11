# Project Documentation and Change History

## Purpose
This document records the technical evolution of the repository from the first reviewed state to the current state, including key decisions, rationale, and delivered features.  
It serves two audiences:
1. Human project owner/supervisor: transparent progress history and reasoning.
2. Agentic LLM workflows: stable context so future edits remain aligned with established decisions.

## Repository State at First Review (Non-Blank Baseline)
When first reviewed, the repository already contained:
1. Core source modules in `Main/src` (`datasets.py`, `prepare_splits.py`, `training.py`, `integrity.py`, `utils.py`, `experiment_log.py`).
2. Notebook-driven pipeline files `Main/notebooks/01_dataset_preparation.ipynb` through `Main/notebooks/06_severity_*.ipynb`.
3. Existing CSV artifacts under `Main/CSV`.
4. A Colab context notebook under `Main/Google Colab/Plant_Disease.ipynb`.
5. Existing plan files under `Markdown Files/`.

### Key Issues Found in that State
1. Schema drift between notebooks and `src` pipeline (`label` vs `binary_label`/`class_label`).
2. `notebooks/01_dataset_preparation.ipynb` used stale metadata key `meta["label"]`.
3. Cross-platform path fragility (Windows paths vs Linux/Colab execution).
4. Colab import/root path assumptions were brittle.
5. README workflow did not match executable reality.
6. Environment reproducibility/runtime mismatch (default shell was Python 3.14).
7. Integrity checks used exact hashing only (no near-duplicate scan).
8. Dependencies were range-based, not pinned.
9. Repository governance was hiding useful reproducibility artifacts.

## Strategic Decisions Taken

### 1) Scope Lock and Phaseing
Adopted the revised plan in `implementation_plan2_chatgpt_edited.md`:
1. Primary task: 15-class crop+disease classification.
2. Side analysis: 4-disease subset.
3. Severity (0-3): optional, gated Phase 4 only.

Rationale:
1. Prevent scope creep over 15 months.
2. Prioritize dissertation-grade rigor and reproducibility first.
3. Keep optional severity as value-add, not core dependency.

### 2) Single Source of Truth
Shifted pipeline authority to `Main/src` modules; notebooks became thin orchestration layers.

Rationale:
1. Reduces duplicate logic and hidden drift.
2. Enables both local and Colab execution using identical code paths.

### 3) Near-Duplicate Method Choice: dHash
Used dHash-based near-duplicate screening in integrity checks rather than pHash.

Rationale:
1. dHash is simpler and fast for standardized leaf imagery.
2. Sufficient for Phase 1 screening; pHash can be added later if needed.
3. Plan wording was aligned to dHash to remove method ambiguity.

### 4) Environment Deviation (Accepted)
Original recommendation suggested Python 3.10/3.11.  
Implemented Python 3.13 standardization instead (`Main/.python-version`) because this machine already had a working 3.13 stack with PyTorch and related dependencies.

Rationale:
1. Faster stabilization with current machine constraints.
2. Lower friction than forcing a full interpreter migration mid-refactor.
3. Explicit `py -3.13` runner prevents drift with default `python` (3.14).

## Delivered Changes (Chronological Summary)

### A. Planning and Governance
1. Added/updated plan file: `Markdown Files/plans/implementation_plan2_chatgpt_edited.md`.
2. Added Phase 1 checklist: `Markdown Files/phase1/phase1_execution_checklist.md`.
3. Added this persistent history file: `Markdown Files/docs/documentation.md`.
4. Added 12-step gate tracker: `Markdown Files/phase1/phase1_12_step_gate_checklist.md`.

### B. Reproducibility and Artifacts
1. Extended split manifest generation in `Main/src/prepare_splits.py`:
   - timestamp, seed, CSV SHA256, class counts, git commit.
2. Extended experiment logging in `Main/src/experiment_log.py`:
   - `set_git_commit(...)`
   - `set_split_artifacts(...)`
3. Added dedicated integrity artifact writer `Main/src/integrity_report.py`:
   - timestamped + latest JSON report
   - timestamped + latest TXT summary
   - output path: `results/integrity_reports/`.

### C. Data/Path Robustness
1. CSV image paths normalized to forward slashes in `prepare_splits.py`.
2. Loader path normalization in `datasets.py` for Windows/Colab portability.
3. Default label column moved to `class_label` in `datasets.py` and loader schema checks added.

### D. Integrity Improvements
1. Exact duplicate detection updated to SHA256.
2. Added near-duplicate cross-class scan using dHash Hamming distance.
3. Integrity output now suitable for reproducible artifact tracking.

### E. Notebook Refactor
1. `notebooks/01_dataset_preparation.ipynb` now calls `src.integrity`/`src.prepare_splits`.
2. `notebooks/02_data_pipeline.ipynb` now validates dataloaders via `src` and `class_label`.
3. `notebooks/03_finetuning_resnet.ipynb` now uses `src` modules and `ExperimentLog`.
4. `04`, `05`, `06` severity notebooks are explicitly deprecated/parked.

### F. Runtime and Dependency Stabilization
1. Added `.python-version` with `3.13`.
2. Pinned dependencies in `Main/requirements.txt`.
3. Added one-command Phase 1 runner `Main/run_phase1.bat` enforcing `py -3.13`.

### G. Tests Added
Added minimal regression tests:
1. `Main/tests/test_split_leakage.py`
2. `Main/tests/test_dataset_schema.py`
3. `Main/tests/test_integrity.py`

### H. Phase 1 Gate Completion Work (Steps 9-11)
1. Added script-based baseline runner:
   - `Main/src/run_baseline_smoke.py`
   - Produces checkpoint, metrics snapshot, confusion matrix (JSON/PNG), and experiment log artifacts.
2. Integrated full logging in baseline run:
   - seed, git commit hash, split artifacts, split manifest file hash.
   - metrics snapshot hash, confusion matrix artifact hashes, model checkpoint hash.
3. Added Colab path sanity + smoke evidence runner:
   - `Main/src/colab_smoke.py`
   - Colab notebook now calls this smoke reporter.
   - Current stored smoke artifact was generated from local simulation mode (`Executed in Colab: False`) using the same `Main/` root checks and import path logic.
4. Extended one-command runner:
   - `Main/run_phase1.bat` now executes integrity -> splits -> tests -> baseline smoke -> colab smoke -> repeat-run stability check.
5. Added repeat-run stability report:
   - `Main/src/stability_check.py`
   - Produces mean/std summaries for accuracy and macro F1 across multiple seeds.

### I. Post-Review Hardening (Claude Feedback Closure, 2026-03-01)
1. Added scheduler compatibility handling in `Main/src/training.py`.
   - `ReduceLROnPlateau` now steps with validation loss (`scheduler.step(val_loss)`).
   - Other schedulers keep the standard `scheduler.step()` path.
   - Why: avoids Phase 2 runtime errors when monitor-based schedulers are enabled.

2. Added class-imbalance mitigation option in `Main/src/run_baseline_smoke.py`.
   - New `--class-weighting` argument with `none` or `inverse_frequency`.
   - `inverse_frequency` computes balanced class weights from training split counts and passes them to `CrossEntropyLoss`.
   - Why: Phase 2 class distribution is highly imbalanced; weighted loss support is now available by configuration.

3. Standardized artifact paths to repo-relative values for portability.
   - `Main/src/prepare_splits.py` manifest paths are now relative (for example `CSV/plantvillage_train.csv`).
   - `Main/src/run_baseline_smoke.py` metrics snapshot and experiment artifacts store relative paths.
   - `Main/src/integrity_report.py` now writes project-relative paths for dataset and near-duplicate preview items.
   - Why: removes machine-specific absolute paths from canonical reproducibility artifacts.

4. Added explicit smoke-run note to baseline metrics/log artifacts.
   - Notes now explain low metrics are expected for random init + very short smoke settings.
   - Why: prevents misinterpretation of smoke-run metrics by external reviewers.

5. Validation evidence collected after hardening:
   - `py -3.13 -m unittest discover -s tests` passed.
   - `py -3.13 -m src.prepare_splits` regenerated latest split manifest with relative paths.
   - `py -3.13 -m src.integrity_report` regenerated latest integrity artifacts with relative paths.
   - `py -3.13 -m src.run_baseline_smoke --epochs 1 --class-weighting inverse_frequency` executed successfully.
   - Additional direct scheduler smoke script verified `ReduceLROnPlateau` path does not fail.

6. Near-duplicate decision record (formal):
   - Decision: treat dHash cross-class near-duplicate findings (`14` pairs at threshold `<=5`) as **warning-level review flags**, not automatic hard failures for split validity.
   - Basis: exact cross-class duplicates remain `0`, and dHash at this threshold is known to over-flag visually similar but non-identical leaf imagery.
   - Control policy: keep reporting these pairs in every integrity run, and perform targeted manual review if count rises materially or if specific pairs recur in suspicious patterns during Phase 2 experiments.
   - Why: preserves conservative monitoring while avoiding destructive/unsupported auto-removal rules.

### J. Validation Snapshot and Final Residual Blocker (2026-03-01)
1. Validation commands executed locally after hardening:
   - `py -3.13 -m unittest discover -s tests`
   - `py -3.13 -m src.prepare_splits`
   - `py -3.13 -m src.integrity_report`
   - `py -3.13 -m src.run_baseline_smoke --epochs 1 --class-weighting inverse_frequency`
   - Direct scheduler smoke script using `torch.optim.lr_scheduler.ReduceLROnPlateau` with `src.training.train_model`.

2. Validation outcome:
   - All above commands completed successfully.
   - Canonical latest artifacts were regenerated and now use repo-relative paths in split/integrity/baseline artifacts.

3. Residual blocker status update (resolved on 2026-03-02):
   - Live Colab execution artifact captured and stored under:
     - `results/colab_smoke/latest_colab_smoke.json`
     - `results/colab_smoke/latest_colab_smoke.txt`
   - Acceptance signal achieved: `executed_in_colab = true` and `passed = true`.

## Current Execution Workflow (Phase 1)
From repo root:
1. `run_phase1.bat`

What it does:
1. Runs integrity checks and writes JSON/TXT artifacts.
2. Generates frozen splits + split manifest.
3. Executes minimal test suite.
4. Runs script-based baseline smoke training and saves metrics/log artifacts.
5. Runs Colab smoke checks and saves evidence artifacts.

## Artifact Locations
1. Split manifests:
   - `results/split_manifests/latest_split_manifest.json`
2. Integrity reports:
   - `results/integrity_reports/latest_integrity_report.json`
   - `results/integrity_reports/latest_integrity_report.txt`
3. Tests:
   - `tests/`
4. Baseline smoke:
   - `results/baseline_smoke/latest_metrics_snapshot.json`
   - `results/baseline_smoke/latest_confusion_matrix.json`
   - `results/baseline_smoke/latest_confusion_matrix.png`
   - `results/baseline_smoke/latest_experiment_log.json`
5. Colab smoke:
   - `results/colab_smoke/latest_colab_smoke.json`
   - `results/colab_smoke/latest_colab_smoke.txt`
6. Stability checks:
   - `results/stability_checks/latest_stability_check.json`
   - `results/stability_checks/latest_stability_check.txt`
7. Lab log:
   - `Markdown Files/docs/lab_log.md`

## What Is Still Not Completed (Phase 1)
1. None. Phase 1 gate sign-off completed on 2026-03-02 (see `Markdown Files/phase1/phase1_signoff_claude.md`).

## Phase 1 Summary Note (Stable vs Pending)
Date: 2026-02-28

Stable:
1. Scope and terminology are locked (15-class primary, 4-disease side analysis, gated severity).
2. Environment is reproducible under Python 3.13 with pinned dependencies.
3. Integrity, split generation, baseline smoke training, colab smoke checks, and stability checks are executable via scripts.
4. Core artifacts (integrity, split manifest, baseline metrics/log/confusion matrix, colab smoke, stability report) are generated and persisted.
5. Notebook/schema drift is resolved for 01-03; severity notebooks are explicitly parked.

Pending:
1. None (Phase 1 sign-off complete as of 2026-03-02).

## Why This Approach Is Appropriate
1. It prioritizes reproducibility and evaluator trust over rapid feature expansion.
2. It reduces technical debt early (schema drift, path drift, env drift).
3. It establishes a clean baseline for rigorous Phase 2 architecture comparisons.

## Phase 2 Kickoff Record (Approved 2026-03-02)

### Trigger
1. External follow-up review (`Markdown Files/phase1/phase1_signoff_claude.md`) signed off Phase 1 as PASS.
2. Owner approved immediate Phase 2 start with multi-architecture benchmark as first priority.

### Approved Phase 2 Script Structure
1. `src/run_phase2_benchmark.py`:
   - benchmark orchestrator over model x seed
   - default class weighting: `inverse_frequency`
   - Colab-friendly CLI execution
2. `src/model_registry.py`:
   - canonical model builder for:
     - ResNet18
     - ResNet50
     - EfficientNet-B0
     - ViT-Small (`vit_small_patch16_224`)
3. `src/split_guard.py`:
   - verifies current split CSV hashes against `results/split_manifests/latest_split_manifest.json`
   - hard-fails benchmark on mismatch
4. `src/phase2_reporting.py`:
   - outputs:
     - `results/phase2/model_seed_metrics.csv`
     - `results/phase2/model_summary_mean_std.csv`
     - `results/phase2/leaderboard.csv`

### Protocol Decisions Locked for Phase 2
1. Task: 15-class frozen-split benchmark.
2. Seeds: 3 (`41,42,43`) for every architecture.
3. Class-weighting default: `inverse_frequency`.
4. Execution target: Colab for heavy training, same `src` codepath as local.

### New Operational Checklist
1. Created `Markdown Files/phase2/phase2_execution_checklist.md` to track:
   - implementation tasks
   - protocol enforcement
   - artifact requirements
   - go/no-go gates
   - fallback rules

### Rationale
1. Keeps benchmark fairness auditable and reproducible.
2. Avoids notebook logic drift by centering all training in `src`.
3. Produces dissertation-ready summary artifacts directly from run outputs.

## Documentation Reorganization (2026-03-02)

### Change
1. Reorganized `Markdown Files/` into functional and phase-based subfolders:
   - `Markdown Files/plans/`
   - `Markdown Files/docs/`
   - `Markdown Files/reviews/`
   - `Markdown Files/phase1/`
   - `Markdown Files/phase2/`
   - `Markdown Files/phase3/`
   - `Markdown Files/archive/`
2. Added index file: `Markdown Files/README.md`.
3. Updated internal references in checklists/documentation to new paths.

### Why
1. Reduces navigation friction as documentation volume grows.
2. Keeps phase state, plans, and historical reviews separated for faster retrieval by both human and LLM workflows.

## Phase 2 Implementation Start (2026-03-02)

### Implemented first code units
1. Added `src/model_registry.py`:
   - canonical model names + aliases
   - architecture builder for ResNet18/ResNet50/EfficientNet-B0/ViT-Small
   - trainable parameter counter
2. Added `src/run_phase2_benchmark.py`:
   - CLI-based orchestrator for model x seed benchmark runs
   - default class weighting option (`inverse_frequency`)
   - split-manifest hash validation guard (inline)
   - dry-run mode for architecture/load-path sanity checks
   - run artifact writing + aggregate CSV outputs

### Validation performed
1. `py -3.13 -m py_compile src/model_registry.py src/run_phase2_benchmark.py`
2. `py -3.13 -m src.run_phase2_benchmark --dry-run --no-pretrained --batch-size 4 --num-workers 0 --models resnet18,resnet50,efficientnet_b0,vit_small_patch16_224`
3. Dry-run artifact generated: `results/phase2/phase2_dry_run_report.json`

### Remaining near-term work for Phase 2
1. Extract inline split guard into dedicated `src/split_guard.py`.
2. Extract inline aggregation logic into dedicated `src/phase2_reporting.py`.
3. Add `Google Colab/phase2_benchmark_runner.ipynb` thin runner.
4. Execute first non-dry benchmark pass (1 epoch x all models x 1 seed) before full sweep.

## Phase 2 Refactor and Smoke Validation (2026-03-02, continued)

### Additional implementation completed
1. Added `src/split_guard.py` and integrated it into `src/run_phase2_benchmark.py`.
2. Added `src/phase2_reporting.py` and integrated summary/leaderboard generation through it.
3. Added Colab thin runner notebook:
   - `Google Colab/phase2_benchmark_runner.ipynb`
4. Extended benchmark runner with fast local smoke controls:
   - `--max-train`
   - `--max-val`
   - `--max-test`
   These are optional overrides for fast validation; default behavior remains full frozen-split runs.

### Validation evidence
1. Compile check:
   - `py -3.13 -m py_compile src/model_registry.py src/split_guard.py src/phase2_reporting.py src/run_phase2_benchmark.py`
2. All-model dry-run:
   - `py -3.13 -m src.run_phase2_benchmark --dry-run --no-pretrained --batch-size 4 --num-workers 0 --models resnet18,resnet50,efficientnet_b0,vit_small_patch16_224`
3. Non-dry smoke benchmark (sampled splits):
   - `py -3.13 -m src.run_phase2_benchmark --models resnet18 --seeds 41 --epochs 1 --batch-size 16 --num-workers 0 --no-pretrained --scheduler cosine --class-weighting inverse_frequency --max-train 256 --max-val 96 --max-test 96`
4. Generated outputs:
   - `results/phase2/phase2_dry_run_report.json`
   - `results/phase2/model_seed_metrics.csv`
   - `results/phase2/model_summary_mean_std.csv`
   - `results/phase2/leaderboard.csv`
   - `results/phase2/runs/resnet18/seed_41/metrics.json`

## Phase 2 Protocol Hardening and Multi-Architecture Smoke (2026-03-02, later)

### Code changes
1. Upgraded `src/training.py`:
   - Added `use_amp` support to `train_model(...)`.
   - AMP is enabled only when `--amp` is requested and CUDA is available.
2. Hardened `src/run_phase2_benchmark.py`:
   - Added explicit `--pretrained` / `--no-pretrained` mutually exclusive CLI flags.
   - Reworked split handling so sampled/frozen split files are prepared once per seed and then reused across all architectures.
   - Added per-run split SHA-256 hashes into metrics payload.
   - Added `model_size_bytes` logging from saved checkpoints.
   - Forwarded `use_amp=args.amp` into the training loop.
3. Updated `src/phase2_reporting.py`:
   - Summary table now includes `model_size_bytes`.
4. Updated AMP scaler path in `src/training.py`:
   - Uses `torch.amp.GradScaler("cuda", ...)` when available, with legacy fallback for compatibility.

### Why these changes were made
1. AMP path was required for efficient Colab GPU execution in Phase 2.
2. Per-seed split reuse removes any risk of model-to-model split drift during sampled smoke runs.
3. Logging model size closes the remaining protocol requirement for speed/size trade-off reporting.

### Validation evidence
1. Compile/test checks:
   - `py -3.13 -m py_compile src/training.py src/run_phase2_benchmark.py src/phase2_reporting.py`
   - `py -3.13 -m unittest discover -s tests`
2. Full local multi-architecture smoke (non-dry):
   - `py -3.13 -m src.run_phase2_benchmark --models resnet18,resnet50,efficientnet_b0,vit_small_patch16_224 --seeds 41 --epochs 1 --batch-size 16 --num-workers 0 --no-pretrained --scheduler cosine --class-weighting inverse_frequency --max-train 192 --max-val 96 --max-test 96`
3. Generated/updated artifacts:
   - `results/phase2/model_seed_metrics.csv`
   - `results/phase2/model_summary_mean_std.csv`
   - `results/phase2/leaderboard.csv`
   - `results/phase2/runs/resnet18/seed_41/metrics.json`
   - `results/phase2/runs/resnet50/seed_41/metrics.json`
   - `results/phase2/runs/efficientnet_b0/seed_41/metrics.json`
   - `results/phase2/runs/vit_small_patch16_224/seed_41/metrics.json`

### Remaining blocker before full Phase 2 sweep
1. Launch full 4-model x 3-seed benchmark on Colab.

## Colab Dry-Run Closure and Notebook Standardization (2026-03-06)

### New validation evidence
1. Live Colab Phase 2 dry-run completed from `Google Colab/phase2_benchmark_runner.ipynb`.
2. Output confirmed frozen-split guard behavior:
   - existing `results/split_manifests/latest_split_manifest.json` detected
   - no split regeneration performed
3. Dry-run artifact refreshed at:
   - `results/phase2/phase2_dry_run_report.json`

### Notebook standardization changes
1. `Google Colab/phase2_benchmark_runner.ipynb`:
   - added concise one-line cell header comments for consistency
   - retained strict frozen-split guard in setup flow
2. `Google Colab/phase1_colab_live_smoke_artifact.ipynb`:
   - canonicalized setup to fixed repo root (no candidate search)
   - enforced strict frozen-split guard before smoke execution
3. `Google Colab/Plant_Disease.ipynb` retained as legacy context notebook only.

### Minor runtime messaging fix
1. Updated `src/run_phase2_benchmark.py`:
   - removed stale `--amp reserved` message
   - now prints accurate AMP status (enabled on CUDA, FP32 fallback otherwise).

## Colab Smoke Artifact Refresh (2026-03-06)
1. Replaced canonical latest smoke artifacts with files from live Colab rerun:
   - `results/colab_smoke/latest_colab_smoke.json`
   - `results/colab_smoke/latest_colab_smoke.txt`
2. Archived same run with timestamped filenames:
   - `results/colab_smoke/colab_smoke_20260306_192608.json`
   - `results/colab_smoke/colab_smoke_20260306_192608.txt`
3. Latest smoke status remains passing (`executed_in_colab=true`, `passed=true`).

## Cross-Environment Robustness Fixes (2026-03-07)

### Trigger
1. Colab benchmark run exposed two environment-specific issues:
   - split hash mismatch in strict validation despite intended frozen usage
   - CUDA device property access error in experiment logging (`total_mem` vs `total_memory`)

### Code changes
1. Updated `src/experiment_log.py`:
   - `set_environment()` now reads CUDA memory from `total_memory` with fallback to legacy `total_mem`.
   - Impact: environment logging now works across current and older PyTorch property naming.
2. Updated `src/split_guard.py`:
   - added line-ending-normalized CSV hash variants (raw/LF/CRLF) during split validation.
   - Impact: prevents false mismatches for equivalent CSV content across Windows and Linux/Colab.
   - Guardrail remains strict for non-line-ending content changes.

### Current behavior after fixes
1. Training can run on both CPU and GPU; `--amp` is CUDA-gated and falls back to FP32 on CPU.
2. Frozen-split validation remains enforced while tolerating pure newline-format differences.

### Operational note (Colab)
1. Notebook shell commands must use `!` prefix (for example `!python -m ...`).

## Phase 2 Colab Execution Modes Clarified (2026-03-12)

### Canonical interpretation
Use notebook cell **headers** as identifiers instead of absolute cell numbers.  
Reason: markdown/edit operations can shift numeric positions, while headers remain stable.

### Mode A: First-time clean run (fresh reviewer/device)
Recommended path:
1. `# Colab setup + repo bootstrap`
2. `# Canonical repo root`
3. `# Frozen split guard + dry-run benchmark` (recommended sanity check)
4. `# Full benchmark run`
5. `# Rebuild full 12-run Phase 2 summary from metrics.json files` (optional if step 4 completed cleanly)
6. `# Export Phase 2 artifacts to a zip and download to your laptop.`

### Mode B: Recovery/incremental run (existing stale partial outputs)
Use this when prior artifacts exist (for example old `seed_41` one-epoch runs):
1. `# Colab setup + repo bootstrap`
2. `# Canonical repo root`
3. `# Clear stale seed_41 artifacts before full rerun`
4. `# Full rerun for seed_41 across all 4 models`
5. `# Full benchmark run`
6. `# Rebuild full 12-run Phase 2 summary from metrics.json files`
7. `# Export Phase 2 artifacts to a zip and download to your laptop.`

### Why cells 5-7 are not always required
1. `# Minimal training smoke (1 model, 1 seed, 1 epoch)`:
   - Purpose: fast pipeline sanity only.
   - Not required for first-time full benchmark execution.
2. `# Clear stale seed_41 artifacts before full rerun`:
   - Purpose: prevent `--resume` from skipping stale seed-41 files.
   - Not needed on a clean first run with no previous artifacts.
3. `# Full rerun for seed_41 across all 4 models`:
   - Purpose: repair incomplete seed coverage.
   - Not needed when all seeds are being run fully from scratch.

## Phase 2 Continuation Across Colab Accounts (2026-03-14)

### Operational situation
1. Phase 2 full benchmarking exceeded the available GPU quota on the original Colab account.
2. The full `PlantVillage` Google Drive folder, including persisted artifacts and intermediate outputs, was copied to a second Google account and reused there.
3. The same canonical Colab notebook and repository workflow were then executed from the second account.

### Interpretation
1. This is a fresh Colab runtime but **not** a fresh experiment state.
2. Because checkpoints, split manifests, logs, partial results, and other benchmark artifacts were preserved, the second-account execution should be treated as a **continuation/recovery run**.
3. This is operationally equivalent to resuming the same benchmark on different compute access, not launching a new independent benchmark from zero.

### Why this is acceptable
1. Frozen splits, seeds, artifact paths, and benchmark logic remain the same across accounts.
2. Persisting the Drive folder preserves the evidence trail rather than fragmenting it across disconnected runs.
3. The only remaining variability is ordinary ML nondeterminism or resume/skip behavior, not a methodological change in the protocol.

### Honest dissertation/report wording
1. Phase 2 benchmarking was executed across multiple Google Colab sessions/accounts due GPU quota limits.
2. Artifacts and intermediate results were persisted in Google Drive.
3. Runs were resumed from saved state rather than restarted from scratch.

## Phase 2 Reporting Compatibility Fix (2026-03-14)

### Trigger
1. The notebook summary-rebuild cell failed on Colab with a `numpy.dtype size changed` error while importing `pandas` through `src.phase2_reporting`.
2. This indicates a temporary notebook-kernel binary mismatch between installed `numpy` and `pandas`, typically caused by package changes during a live Colab session.

### Fix
1. Rewrote `src/phase2_reporting.py` to use only the Python standard library (`csv`, `statistics`, `collections`) instead of `pandas`.
2. Output files remain the same:
   - `results/phase2/model_seed_metrics.csv`
   - `results/phase2/model_summary_mean_std.csv`
   - `results/phase2/leaderboard.csv`

### Why this approach was chosen
1. The reporting step is simple aggregation and does not need a heavy dataframe dependency.
2. Removing the `pandas` import makes the notebook summary rebuild more robust after Colab package churn.
3. This fixes the user-facing failure without changing the benchmark protocol itself.

## Phase 2 Full Benchmark Artifact Import and Result Review (2026-03-14)

### Artifact intake
1. Imported `phase2_artifacts_export.zip` from the completed Colab session into the canonical local paths under `results/phase2/`.
2. This import replaced older local seed-41 placeholder artifacts with the completed seed-41 rerun outputs from Colab.
3. The downloaded Colab notebook outputs were retained only as ignored context material under `code archives/`.

### Benchmark completion status
1. Core Phase 2 benchmark is now complete for the locked matrix: `4 models x 3 seeds = 12 runs`.
2. Aggregated outputs now correctly reflect all 12 completed runs:
   - `results/phase2/model_seed_metrics.csv`
   - `results/phase2/model_summary_mean_std.csv`
   - `results/phase2/leaderboard.csv`
3. Local repository state is now aligned with the latest Colab export for Phase 2 results.

### Mean performance summary
1. `resnet18`
   - accuracy mean: `0.99817`
   - macro F1 mean: `0.99845`
   - params: `11.18M`
   - model size: `44.81 MB`
2. `efficientnet_b0`
   - accuracy mean: `0.99795`
   - macro F1 mean: `0.99824`
   - params: `4.03M`
   - model size: `16.38 MB`
3. `vit_small_patch16_224`
   - accuracy mean: `0.99731`
   - macro F1 mean: `0.99757`
   - params: `21.67M`
   - model size: `86.73 MB`
4. `resnet50`
   - accuracy mean: `0.99623`
   - macro F1 mean: `0.99614`
   - params: `23.54M`
   - model size: `94.46 MB`

### Interpretation
1. Results are strong but not surprising for PlantVillage; this dataset is clean, standardized, and known to be high-ceiling for image classifiers.
2. `resnet18` currently gives the best overall balance of accuracy, macro F1, and model size.
3. `efficientnet_b0` is a very strong second-place result with the smallest checkpoint footprint, which is useful for efficiency discussion.
4. `vit_small_patch16_224` performs well but does not outperform the best CNN here, which is plausible on a relatively structured, medium-scale dataset.
5. `resnet50` is the weakest of the four on this benchmark despite being larger, which strengthens the argument that bigger is not automatically better on this task.

### Stability and caveats
1. Seed-to-seed variance is low across all models, which is a good sign for benchmark stability.
2. Some models stopped early before epoch 30; that is expected because the training loop uses early stopping.
3. Remaining rigor work is analytical, not infrastructural:
   - statistical comparison of best CNN vs best ViT
   - dissertation-grade write-up of why the ranking looks this way

### Error pattern observations
1. The remaining mistakes are concentrated in visually similar tomato classes rather than broad crop-level confusion.
2. The most repeated confusion pairs across runs include:
   - `Tomato - Target Spot -> Tomato - Spider Mites`
   - `Tomato - Early Blight <-> Tomato - Late Blight`
   - some `Tomato - Yellow Leaf Curl Virus` spillover into other tomato disease classes
3. This is expected and useful for later qualitative analysis/XAI discussion.

### Repository housekeeping
1. Renamed `helper scripts/` to `code archives/`.
2. Rationale: this folder holds non-canonical legacy utilities and downloaded context notebooks, so the new name is clearer and less misleading.

## Phase 2 Analysis Layer Added (2026-03-15)

### New scripts
1. Added `src/phase2_analysis.py`.
   - Purpose: generate dissertation-ready Phase 2 comparison plots from existing benchmark artifacts.
   - Output root: `results/phase2/analysis/`
2. Added `src/phase2_error_analysis.py`.
   - Purpose: load locally available checkpoints, run inference on the test split, and save wrong-prediction galleries/CSVs.
   - This script now verifies local checkpoint hashes against the experiment logs before doing any analysis.

### Generated plot outputs
1. `results/phase2/analysis/analysis_summary.json`
2. `results/phase2/analysis/plots/metric_summary.png`
3. `results/phase2/analysis/plots/seed_variance.png`
4. `results/phase2/analysis/plots/efficiency_tradeoff.png`
5. `results/phase2/analysis/plots/loss_curves.png`
6. `results/phase2/analysis/plots/accuracy_curves.png`
7. `results/phase2/analysis/plots/mean_confusion_heatmaps.png`
8. `results/phase2/analysis/plots/top_confusions.png`

### Why scripts instead of notebooks
1. These analysis steps are now part of the canonical pipeline, not one-off exploration.
2. Scripts are easier to rerun consistently across local and Colab workflows.
3. A notebook can still be added later for presentation, but the source of truth should stay in `src/`.

### Validation status
1. `src.phase2_analysis` executed successfully in the local project venv and generated the expected plot set.
2. `src.phase2_error_analysis` passed a smoke run on a subset, then was hardened with checkpoint-hash validation.
3. Full wrong-image extraction is currently **blocked locally** because the imported Colab artifact zip updated `results/phase2/...` but did not include the matching `models/phase2/.../best.pth` checkpoint files.
4. The script now fails explicitly instead of producing misleading galleries when local checkpoints are stale.

### Current operational meaning
1. Artifact-driven analysis is complete and trustworthy locally.
2. Checkpoint-driven image-level error analysis requires one of:
   - exporting the matching `models/phase2/.../best.pth` files from Colab, or
   - rerunning `src.phase2_error_analysis` in the Colab/Drive environment where those weights already exist.
