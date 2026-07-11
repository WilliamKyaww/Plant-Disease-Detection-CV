# Plant Disease Detection - Implementation Plan v2 (ChatGPT Edited)

## Purpose
This plan is optimized for a high-first undergrad dissertation with strong reproducibility and clear scope control.

## Scope Lock
1. Primary task: 15-class crop+disease classification (PlantVillage folder-level classes).
2. Side analysis: 4-disease subset analysis (healthy, bacterial_spot, early_blight, late_blight) for interpretability/comparison.
3. Severity (0-3) is optional and gated. Do it only if core phases finish on time with stable results.

## Research Questions (define early)
1. Which architecture family (CNN vs ViT) gives the best performance-efficiency tradeoff on 15-class PlantVillage?
2. Are observed differences between top models statistically significant?
3. Do model attention maps align with disease regions better for some architectures than others?
4. How much performance and calibration degrade on out-of-distribution (OOD) real-world images?

## Environment Strategy (Hybrid)
1. Local laptop: coding, data checks, split generation, debugging, labeling, plotting, writing.
2. Colab: heavy training, multi-seed experiments, long runs, architecture sweeps.
3. Keep codepath identical between local and Colab by using `src` modules and path auto-detection.

## Phase 1 - Data + Reproducibility Foundation (Weeks 1-4)
Goal: a trustworthy, reproducible pipeline before heavy training.

### Deliverables
- [ ] Validate all 15 dataset folders exist and contain images.
- [ ] Run integrity checks: missing/corrupt files, exact duplicates, near-duplicates (dHash, Hamming distance threshold).
- [ ] Build/freeze stratified splits with `python -m src.prepare_splits` (not notebook-only generation).
- [ ] Produce split manifest artifact containing:
  - timestamp
  - seed
  - SHA256 for each split CSV
  - row counts and class counts per split
  - git commit hash
- [ ] Make `src` modules the single source of truth; notebooks become thin orchestration/analysis layers.
- [ ] Ensure one baseline model trains, saves, evaluates, and logs successfully.
- [ ] Pin dependencies and record runtime environment (Python/torch/CUDA/device).

### Go/No-Go Gate
Proceed only if:
1. Integrity checks pass (or exceptions are documented and handled).
2. Frozen split manifest is generated and saved.
3. Baseline run completes and logs are written.

## Phase 2 - Core Modeling (15-Class) (Weeks 5-12)
Goal: rigorous architecture comparison.

### Model Set
- ResNet18
- ResNet50
- EfficientNet-B0
- ViT-Small

### Protocol
- [ ] Same splits, transforms, optimizer family, epoch budget, early stopping logic.
- [ ] 3-seed protocol for every model (report mean +/- std).
- [ ] Record latency, params, model size, and full classification metrics.
- [ ] Run McNemar test for top CNN vs top ViT on test predictions.
- [ ] Keep ablation budget capped (max 2 ablation families) unless schedule buffer is healthy.

### Go/No-Go Gate
Proceed only if:
1. All models complete multi-seed runs (or fallback invoked and documented).
2. Results table and significance test are complete.
3. Methodology draft for Phase 2 is written.

### Fallback
If ViT training cost is too high on available hardware/time:
1. Keep ResNet18/ResNet50/EfficientNet-B0.
2. Improve analysis depth instead of adding breadth.

## Phase 3 - Explainability (Weeks 13-17)
Goal: empirical attention analysis, not overclaimed novelty.

### Deliverables
- [ ] Grad-CAM (or equivalent) for correct and incorrect predictions.
- [ ] Cross-architecture comparison of attention behavior.
- [ ] 50-60 manually annotated disease-region images.
- [ ] IoU-style overlap metric summary (mean +/- std).
- [ ] Write XAI section draft with limitations explicitly stated.

### Go/No-Go Gate
Proceed only if heatmaps and overlap metrics are generated and reviewed.

## Phase 4 - Optional Severity Track (0-3) (Weeks 18-25)
Goal: add value only if core track is stable.

### Decision Rule
Start Phase 4 only if by end of Phase 3:
1. Phase 2/3 deliverables are complete.
2. At least 3-4 weeks of schedule buffer remain.

### If started
- [ ] Finalize severity rubric with reference examples.
- [ ] Label 200-300 images manually.
- [ ] Intra-rater agreement: relabel 50 images after >=2 weeks, compute Cohen's kappa.
- [ ] Train simpler severity baseline first, then optional multi-task model.
- [ ] Use CLIP weak labels only if validated against manual labels.

### Fallback
If severity labels are noisy or time is tight:
1. Keep severity as pilot/appendix analysis.
2. Prioritize stronger core 15-class evidence.

## Phase 5 - Robustness, Uncertainty, Demo (Weeks 26-32)
Goal: honest performance characterization beyond in-distribution accuracy.

### Deliverables
- [ ] OOD set (50-100 images) and error analysis.
- [ ] MC Dropout uncertainty and calibration metrics (ECE + curve).
- [ ] Correlate uncertainty with error rate.
- [ ] Lightweight Streamlit demo (optional if schedule allows).

### Priority Rule
If tradeoff is needed: robustness/uncertainty analysis > demo UI polish.

## Phase 6 - Writing and Finalization (Weeks 33-44+)
Goal: dissertation-quality narrative and evidence packaging.

### Deliverables
- [ ] Integrate rolling write-ups into full dissertation draft.
- [ ] Final figures/tables from frozen artifacts.
- [ ] Clear limitations and future work section.
- [ ] Supervisor feedback cycles with tracked revisions.

## Artifact Logging Policy (Mandatory)
Every key run should log:
1. run name + timestamp
2. hyperparameters (including seed)
3. metrics
4. environment metadata (Python, torch, CUDA, device)
5. git commit hash
6. split artifact manifest (CSV hashes + class counts + seed)

## Success Criteria
By submission, the project should provide:
1. Reproducible 15-class benchmark results with uncertainty estimates.
2. Statistical comparison of key architectures.
3. Explainability analysis with annotated-region overlap evidence.
4. OOD robustness analysis and calibration behavior.
5. Optional severity track only if quality and time gates were met.

## Notes
- This plan intentionally prioritizes rigor and reproducibility over feature sprawl.
- Claims should be phrased as strong empirical findings, not novelty claims unless justified.
