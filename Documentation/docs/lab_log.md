# Lab Log (Dated Execution Record)

Use this log to maintain a concise date-stamped record of implementation actions, outcomes, and next actions.

## Entry Template
Date: YYYY-MM-DD  
Focus:  
Changes made:  
Evidence/artifacts:  
Issues/risks:  
Next actions:

---

Date: 2026-02-28  
Focus: Phase 1 reproducibility hardening and gate preparation.  
Changes made:
1. Standardized scope and execution flow around `src` modules.
2. Added integrity artifact writer (`src.integrity_report`) and report outputs.
3. Added script-based baseline smoke run (`src.run_baseline_smoke`) with checkpoint/metrics/log outputs.
4. Added Colab path sanity smoke checks (`src.colab_smoke`) and evidence artifacts.
5. Added repeat-run stability report (`src.stability_check`) for multi-seed variance summary.
6. Added/updated checklists and documentation history files in `Markdown Files/`.
Evidence/artifacts:
1. `Main/results/integrity_reports/latest_integrity_report.json`
2. `Main/results/split_manifests/latest_split_manifest.json`
3. `Main/results/baseline_smoke/latest_metrics_snapshot.json`
4. `Main/results/baseline_smoke/latest_confusion_matrix.png`
5. `Main/results/baseline_smoke/latest_experiment_log.json`
6. `Main/results/colab_smoke/latest_colab_smoke.json`
7. `Main/results/stability_checks/latest_stability_check.json`
Issues/risks:
1. Near-duplicate pairs are still flagged by integrity checks and need manual review policy.
2. Default shell `python` may still point to 3.14; use `py -3.13`.
Next actions:
1. Review Phase 1 gate evidence.
2. Record formal Step 12 sign-off decision.

---

Date: 2026-03-01  
Focus: External review closure (Claude feedback) before Phase 2.  
Changes made:
1. Added detailed cross-review agreement/disagreement analysis to `phase1_claude_feedback_checklist.md`.
2. Fixed scheduler compatibility in `Main/src/training.py` for `ReduceLROnPlateau` (`scheduler.step(val_loss)`).
3. Added class-imbalance mitigation option in `Main/src/run_baseline_smoke.py` with `--class-weighting inverse_frequency`.
4. Converted canonical artifact paths to repo-relative form across split manifest, integrity report, and baseline smoke artifacts.
5. Added explicit smoke-run note in metrics/log artifacts to clarify expected low baseline performance.
6. Re-ran tests and regenerated `latest_*` artifacts for split/integrity/baseline.
Evidence/artifacts:
1. `Main/results/split_manifests/latest_split_manifest.json` (paths now relative)
2. `Main/results/integrity_reports/latest_integrity_report.json` (paths now relative)
3. `Main/results/baseline_smoke/latest_metrics_snapshot.json` (class weighting + smoke note + relative paths)
4. `Main/results/baseline_smoke/latest_experiment_log.json` (relative artifact paths)
Issues/risks:
1. `Main/results/colab_smoke/latest_colab_smoke.json` still indicates local simulation (`executed_in_colab=false`).
2. dHash near-duplicate warnings remain expected at threshold `<=5` and require policy-based monitoring.
Decision record:
1. dHash near-duplicate pairs are treated as warning-level flags, not automatic hard-fail removals, because exact cross-class duplicates are zero and dHash can over-flag visually similar leaves.
2. Continue reporting these pairs each run; escalate to manual remediation only if counts/patterns worsen in Phase 2.
Next actions:
1. Run one live Colab smoke check and archive artifact (`Executed in Colab: True`).
2. Record final Step 12 sign-off once above evidence is attached.

---

Date: 2026-03-02  
Focus: Colab live artifact closure + repository layout cleanup.  
Changes made:
1. Captured live Colab smoke artifacts and moved canonical files into `results/colab_smoke`.
2. Updated Colab notebooks to use repo-root candidate paths (no hard dependency on `/Main` suffix).
3. Renamed Colab smoke notebook to `Google Colab/phase1_colab_live_smoke_artifact.ipynb` for clearer intent.
4. Updated `.gitignore`: unignored `Google Colab/`; ignored `Markdown Files/` per owner preference.
Evidence/artifacts:
1. `results/colab_smoke/latest_colab_smoke.json` (`executed_in_colab=true`, `passed=true`)
2. `results/colab_smoke/latest_colab_smoke.txt`
3. `results/colab_smoke/colab_smoke_20260302_170804.json`
4. `results/colab_smoke/colab_smoke_20260302_170804.txt`
Issues/risks:
1. Git metadata still resides under `Main/.git`; deleting `Main` without relocating git metadata would break repo history/commands.
Next actions:
1. Decide whether to keep `Main/.git` as gitdir anchor or perform a controlled gitdir relocation.
2. Record formal Phase 1 Step 12 sign-off.

---

Date: 2026-03-02  
Focus: Markdown folder reorganization + Phase 2 code kickoff.  
Changes made:
1. Reorganized `Markdown Files/` into subfolders by function/phase (`plans`, `docs`, `reviews`, `phase1`, `phase2`, `phase3`, `archive`).
2. Added `Markdown Files/README.md` as navigation index.
3. Added first Phase 2 code units:
   - `src/model_registry.py`
   - `src/run_phase2_benchmark.py`
4. Implemented dry-run validation path in Phase 2 runner and executed local dry-run across all 4 target architectures.
Evidence/artifacts:
1. `results/phase2/phase2_dry_run_report.json`
2. `Markdown Files/phase2/phase2_execution_checklist.md` (updated status ticks for implemented items)
3. `Markdown Files/docs/documentation.md` (Phase 2 implementation start section)
Issues/risks:
1. `split_guard.py` and `phase2_reporting.py` are currently inline responsibilities in the benchmark script, pending extraction.
Next actions:
1. Extract split guard and reporting into dedicated Phase 2 modules.
2. Add Colab thin-runner notebook for Phase 2 script execution.
3. Run first 1-epoch non-dry benchmark pass (all models, single seed) before full 3-seed sweep.

---

Date: 2026-03-02  
Focus: Phase 2 modular refactor + smoke benchmark execution.  
Changes made:
1. Added `src/split_guard.py` and moved split-manifest hash validation out of the benchmark runner.
2. Added `src/phase2_reporting.py` and moved aggregate CSV generation into dedicated reporting module.
3. Added `Google Colab/phase2_benchmark_runner.ipynb` (thin orchestration notebook).
4. Added optional sampled-split smoke flags to benchmark runner (`--max-train`, `--max-val`, `--max-test`) for fast local validation.
5. Executed both all-model dry-run and one non-dry resnet18 smoke benchmark.
Evidence/artifacts:
1. `results/phase2/phase2_dry_run_report.json`
2. `results/phase2/model_seed_metrics.csv`
3. `results/phase2/model_summary_mean_std.csv`
4. `results/phase2/leaderboard.csv`
5. `results/phase2/runs/resnet18/seed_41/metrics.json`
Issues/risks:
1. Full 4-model x 3-seed benchmark has not started yet.
2. Colab Phase 2 notebook is prepared but still needs live execution evidence.
Next actions:
1. Run 1-epoch x 1-seed smoke across all 4 models (preferably Colab).
2. If stable, launch full 3-seed Phase 2 sweep.

---

Date: 2026-03-02  
Focus: Phase 2 protocol hardening and 4-model local smoke completion.  
Changes made:
1. Added AMP support in `src/training.py` (`use_amp` in training loop, CUDA-gated).
2. Hardened `src/run_phase2_benchmark.py`:
   - Added explicit `--pretrained`/`--no-pretrained`.
   - Reused per-seed split files across all models (split identity guarantee).
   - Logged split hashes and model size bytes per run.
3. Updated `src/phase2_reporting.py` to include `model_size_bytes` in per-model summary outputs.
4. Executed full local multi-architecture smoke run (all 4 models, 1 seed, 1 epoch, sampled splits).
Evidence/artifacts:
1. `results/phase2/model_seed_metrics.csv`
2. `results/phase2/model_summary_mean_std.csv`
3. `results/phase2/leaderboard.csv`
4. `results/phase2/runs/resnet18/seed_41/metrics.json`
5. `results/phase2/runs/resnet50/seed_41/metrics.json`
6. `results/phase2/runs/efficientnet_b0/seed_41/metrics.json`
7. `results/phase2/runs/vit_small_patch16_224/seed_41/metrics.json`
Issues/risks:
1. Live Colab Phase 2 dry-run artifact is still pending.
2. AMP path now uses `torch.amp.GradScaler("cuda", ...)` when available; legacy fallback remains for compatibility.
Next actions:
1. Run `Google Colab/phase2_benchmark_runner.ipynb` dry-run cell and archive outputs.
2. Launch full 4-model x 3-seed Phase 2 benchmark on Colab.

---

Date: 2026-03-06  
Focus: Live Colab dry-run closure + Colab notebook consistency.  
Changes made:
1. Confirmed live Colab Phase 2 dry-run execution from `Google Colab/phase2_benchmark_runner.ipynb`.
2. Confirmed strict frozen-split behavior in Colab (manifest detected, no regeneration).
3. Standardized Colab notebooks:
   - added concise one-line header comments in all Phase 2 runner code cells
   - renamed smoke notebook to `Google Colab/phase1_colab_live_smoke_artifact.ipynb`
4. Fixed stale runtime message in `src/run_phase2_benchmark.py` for `--amp`.
Evidence/artifacts:
1. `results/phase2/phase2_dry_run_report.json`
2. `results/split_manifests/latest_split_manifest.json`
3. `results/colab_smoke/latest_colab_smoke.json`
4. `results/colab_smoke/latest_colab_smoke.txt`
Issues/risks:
1. Full 4-model x 3-seed Phase 2 benchmark is not complete yet.
Next actions:
1. Continue current non-dry Phase 2 run to completion.
2. Launch full benchmark command with 3 seeds if current smoke run is stable.

---

Date: 2026-03-06  
Focus: Colab smoke artifacts refreshed from rerun download files.  
Changes made:
1. Promoted downloaded rerun files to canonical paths:
   - `results/colab_smoke/latest_colab_smoke.json`
   - `results/colab_smoke/latest_colab_smoke.txt`
2. Saved timestamped archive copies:
   - `results/colab_smoke/colab_smoke_20260306_192608.json`
   - `results/colab_smoke/colab_smoke_20260306_192608.txt`
Evidence/artifacts:
1. `results/colab_smoke/latest_colab_smoke.json` (`executed_in_colab=true`, `passed=true`, timestamp `2026-03-06T19:26:08.867407`)
2. `results/colab_smoke/latest_colab_smoke.txt`

---

Date: 2026-03-07  
Focus: Cross-environment robustness fixes (Colab benchmark blockers).  
Changes made:
1. Patched `src/experiment_log.py` GPU memory capture:
   - use `total_memory` with fallback to `total_mem`.
2. Patched `src/split_guard.py` split hash validation:
   - accept equivalent CSV hashes under LF/CRLF normalization to avoid false Windows/Linux mismatches.
3. Clarified README operational behavior:
   - CPU+GPU support
   - CUDA-gated AMP behavior
   - split guard line-ending normalization policy
Evidence/artifacts:
1. Source updates:
   - `src/experiment_log.py`
   - `src/split_guard.py`
   - `README.md`
Issues/risks:
1. Full 4-model x 3-seed Phase 2 benchmark is still pending completion.
Next actions:
1. Pull latest code in Colab (`git pull`) and rerun Phase 2 dry-run + benchmark commands.

---

Date: 2026-07-17
Focus: Recover the missing product checkpoint path without rewriting Phase 2 evidence.
Changes made:
1. Trained one distinct EfficientNet-B0 seed-44 release candidate from source
   commit `3dd00f7a92fed4537d53a24f0764ade26e3d5946`.
2. Reviewed the 23-file candidate export, its executed notebook, metrics,
   confusion matrix, histories, split evidence, checkpoint size, and hashes.
3. Confirmed strict local state-dict reload and finite 15-class output.
4. Added clean canonical notebook
   `Google Colab/mvp_efficientnet_release_candidate.ipynb` with dataset integrity,
   isolated dry run, training, validation, and export cells.
5. Added `src/export_model_release.py` for governed research-to-product handoff.
6. Moved raw executed notebook/ZIP and the assembled release outside Git into
   private artifact storage; no checkpoint is committed.
Evidence:
1. Candidate ID: `efficientnet_b0_seed44_replacement_20260717T205245Z`.
2. Candidate ZIP SHA-256:
   `f03e51a55c0f43fef3eb74a149fb555a892ce936df8512b5f874348171a97d62`.
3. Checkpoint SHA-256:
   `667f0d6c9c4031d9290c671913f45dc822efb6050637a9802a064965a495785a`.
4. Controlled test accuracy `0.997093`; macro F1 `0.997616`; nine test errors.
Decision:
1. Preserve the original 12-run benchmark unchanged. Seed 44 is a separate
   product release candidate and must not enter Phase 2 aggregate reporting.
2. Keep training/evaluation/export provenance here; keep serving and mobile
   integration in the separate Verdanta Mobile App repository.
Risks/limitations:
1. PlantVillage is controlled-domain data; these metrics do not establish field
   performance.
2. Licensing, independent model-card review, physical-device integration, and
   operational serving evidence remain product release gates.
Validation:
1. All six research `unittest` tests passed and `src/` compiled successfully.
2. The nine-cell canonical notebook is valid JSON, has no saved execution output,
   and its Python portions parse when Colab shell directives are treated as
   notebook directives.
3. A fresh temporary bundle reproduced from the archived candidate had the exact
   expected checkpoint SHA-256 and passed the product's strict loader plus both
   parity fixtures (approximately seven seconds on the current Windows laptop).
4. A one-byte-modified copy of the candidate ZIP was rejected against the
   independently anchored reviewed archive SHA-256 before bundle creation.
5. The temporary reproducibility bundle was deleted after validation; the
   immutable private release remained unchanged.
