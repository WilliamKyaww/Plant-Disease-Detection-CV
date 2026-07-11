# Computer Vision Plant Disease Classification - External AI Project Context

Last updated: 2026-06-23

## Purpose of This Document

This document is a standalone handover brief for an external AI model, supervisor, collaborator, or future project reviewer. It is intended to explain the project without requiring access to previous conversations, internal planning notes, or the full repository.

The project is an undergraduate final-year Computer Science and Artificial Intelligence dissertation project. The current working title is:

**Computer Vision Plant Disease Classification**

The project has evolved from an early "plant disease stress detection" idea into a more rigorous empirical computer vision study focused on 15-class plant disease classification, model benchmarking, reproducibility, and later explainability/robustness analysis.

## 1. Project Overview

### What the Project Is

This is a computer vision and deep learning project for classifying plant leaf images into 15 crop+disease classes using the PlantVillage dataset. The implemented system builds a reproducible machine learning pipeline around:

1. Dataset integrity checks.
2. Frozen stratified train/validation/test splits.
3. PyTorch dataloaders and transforms.
4. Multi-architecture model benchmarking.
5. Multi-seed evaluation.
6. Artifact logging and result analysis.

The project is currently focused on image classification, not object detection, segmentation, multimodal learning, or field deployment.

### Problem Being Solved

Plant diseases can reduce crop yield and food security. Computer vision models can assist plant health diagnosis from leaf imagery, but model performance can depend heavily on dataset quality, train/test leakage, class imbalance, architecture choice, and evaluation protocol.

The project therefore asks a practical research question:

Can a reproducible deep learning benchmark identify which architecture family gives the best performance and efficiency trade-off for 15-class PlantVillage disease classification?

### Project Goals

The project has two parallel goals:

1. Research goal: produce a defensible empirical comparison of CNN and transformer-based architectures on plant disease classification.
2. Software goal: build a clean, reproducible pipeline that makes the experimental claims auditable.

The project deliberately prioritizes rigorous evaluation and documentation over simply achieving high accuracy.

### Why This Project Exists

The initial project idea was too broad and included disease severity classification. After review, the scope was tightened because severity labeling requires manual annotation, a clear rubric, and much more validation effort. The current primary task is 15-class disease classification, with severity kept as a gated optional extension.

The project exists to become a strong final-year dissertation and a credible portfolio project for later postgraduate applications. It is intentionally above the minimum expected standard for an undergraduate project.

### Intended Users

The direct users are:

1. The student/project author, for final-year dissertation work.
2. A project supervisor or marker, reviewing methodology, implementation, and results.
3. A future collaborator or AI coding assistant, continuing the project.
4. Potentially a non-technical demo user later, if a lightweight app is built.

The current codebase is not yet a public-facing production tool. It is primarily a research and experimentation pipeline.

### Research Objectives

The current research objectives are:

1. Compare CNN and ViT-style architectures on a controlled 15-class plant disease classification task.
2. Report mean and standard deviation across multiple random seeds.
3. Evaluate accuracy, macro F1, confusion patterns, model size, parameters, and runtime.
4. Determine whether the top CNN and top ViT differ meaningfully, ideally using a statistical comparison.
5. Later, compare explainability maps across architectures using Grad-CAM or an appropriate equivalent.
6. Later, evaluate robustness and uncertainty on out-of-distribution real-world images.

### Software Objectives

The software objectives are:

1. Keep source modules in `src/` as the single source of truth.
2. Use notebooks only as orchestration/presentation layers.
3. Ensure splits are frozen and validated before model runs.
4. Log key artifacts, metrics, environment details, split hashes, and model checkpoints.
5. Make local and Google Colab execution use the same code path.

## 2. Current Progress

### Completed

Phase 1 is complete and signed off. It established:

1. Scope lock around 15-class PlantVillage classification.
2. Dataset integrity reports.
3. Frozen stratified split CSV files.
4. Split manifest with hashes, class counts, and seed.
5. PyTorch dataset and dataloader pipeline.
6. Baseline smoke training.
7. Colab smoke validation.
8. Repeat-run stability checks.
9. Minimal tests for schema, leakage, and integrity logic.

Phase 2 core benchmarking is also substantially complete:

1. Four architectures were benchmarked.
2. Three seeds were used for each architecture.
3. All 12 model/seed runs are represented in the result artifacts.
4. Per-run metrics, confusion matrices, aggregate leaderboard, and analysis plots exist.
5. The benchmark is based on frozen 15-class splits.

The completed Phase 2 architectures are:

1. `resnet18`
2. `resnet50`
3. `efficientnet_b0`
4. `vit_small_patch16_224`

### Partially Completed

The Phase 2 analysis layer is partially complete:

1. Aggregate plots have been generated.
2. Per-model mean/std metrics exist.
3. Confusion-pattern analysis exists from confusion matrices.
4. Image-level mistake galleries are implemented in code but currently blocked locally because not all matching checkpoint files are present.

The code has a checkpoint-hash guard to prevent misleading image-level error analysis when local model weights do not match the imported Colab result logs.

### Not Yet Implemented

Important remaining items:

1. Statistical comparison between the best CNN (`resnet18`) and best ViT (`vit_small_patch16_224`).
2. Formal Phase 2 methodology/results write-up.
3. Explainability phase using Grad-CAM or equivalent.
4. Manual annotation of disease regions for XAI overlap evaluation.
5. Out-of-distribution robustness set.
6. Calibration and uncertainty analysis.
7. Optional severity classification track.
8. Optional demo interface.

### Current Project Maturity

The project is mature enough to be considered a strong Phase 1/Phase 2 research prototype. It has:

1. A stable dataset pipeline.
2. Reproducibility controls.
3. Meaningful benchmark results.
4. Good documentation discipline.
5. A clear roadmap.

It is not yet dissertation-complete. It still needs the higher-level research analysis layers that turn strong engineering into a strong academic contribution.

### Current Limitations

1. The dataset is PlantVillage, which is clean and controlled. High accuracy is expected and should not be overclaimed as real-world deployment readiness.
2. The current task is image-only, not multimodal.
3. The current benchmark is in-distribution only.
4. Local image-level mistake analysis is blocked until matching model checkpoints are recovered or analysis is run where the checkpoints exist.
5. Statistical significance testing has not yet been completed.
6. XAI and OOD robustness phases are planned but not implemented.

## 3. Research Context

### Academic Motivation

Many plant disease classification projects stop at a single high accuracy number. That is weak academically because PlantVillage is a high-ceiling dataset and may allow inflated claims if leakage, duplicate images, or poor split discipline are not controlled.

This project is motivated by the need for a more careful empirical study:

1. Use frozen splits.
2. Check duplicates and near-duplicates.
3. Compare multiple architectures.
4. Use multiple seeds.
5. Report variance and efficiency metrics.
6. Analyze errors rather than only reporting headline accuracy.

### Research Questions

The current implementation plan defines these research questions:

1. Which architecture family, CNN or ViT, gives the best performance-efficiency trade-off on 15-class PlantVillage?
2. Are observed differences between the top models statistically meaningful?
3. Do model attention maps align with disease regions better for some architectures than others?
4. How much do performance and calibration degrade on out-of-distribution real-world images?

### Why the Approach Has Research Value

The research value is not "I built a classifier." The value is in controlled empirical comparison and evidence quality:

1. The same frozen splits are used for all models.
2. The benchmark uses 3 seeds per architecture.
3. The comparison includes model size, parameter count, runtime, accuracy, macro F1, and confusion behavior.
4. The results challenge a simplistic "larger model is better" story.
5. The planned future work adds explainability and robustness, which are more dissertation-relevant than simply adding more architectures.

### How It Avoids Becoming Just an Engineering Project

The project avoids being purely engineering by framing the implementation around questions and evidence:

1. Architecture comparison: ResNet, EfficientNet, and ViT are compared under the same protocol.
2. Stability: seed variance is explicitly measured.
3. Efficiency: model size and parameter count are reported.
4. Error analysis: confusion patterns are studied.
5. Planned statistical testing: top CNN vs top ViT will be tested.
6. Planned XAI: heatmaps and disease-region overlap will be evaluated.
7. Planned OOD work: robustness beyond the clean dataset will be measured.

### Novel or Investigatory Aspects

The project should not claim novel model architecture. Its stronger claim is:

This is a rigorous empirical study of architecture trade-offs, reproducibility, and model behavior for PlantVillage disease classification.

Potentially interesting findings so far:

1. `resnet18` currently outperforms larger/more complex models on this controlled task.
2. `efficientnet_b0` is nearly as strong as `resnet18` while being much smaller.
3. `vit_small_patch16_224` performs well but does not dominate the CNNs.
4. `resnet50` performs worst despite having more parameters than `resnet18`.
5. Errors concentrate in visually similar tomato diseases rather than broad crop-level confusion.

### Planned Evaluations

Planned or pending evaluations include:

1. McNemar-style comparison of top CNN vs top ViT on paired test predictions.
2. Per-class error analysis.
3. Image-level misclassification galleries.
4. Grad-CAM or equivalent XAI comparison.
5. Disease-region annotation and IoU-style overlap metrics.
6. OOD image set evaluation.
7. Calibration and uncertainty metrics, possibly including ECE and MC Dropout.

## 4. Technical Architecture

### System Architecture

The project is structured as a script-driven machine learning pipeline:

1. `src/` contains reusable source modules.
2. `CSV/` contains canonical labels and split artifacts.
3. `results/` contains manifests, logs, metrics, plots, and reports.
4. `models/` contains model checkpoints.
5. `Google Colab/` contains thin orchestration notebooks for GPU execution.
6. `notebooks/` contains legacy/local notebooks and early exploration.

The important architectural decision is that `src/` is the source of truth. Notebooks should call scripts and modules, not contain independent training logic.

### Conceptual Data Flow

The current data flow is:

1. Raw PlantVillage images are stored under `Datasets/`.
2. Folder names are mapped to metadata in `src/utils.py`.
3. `src.prepare_splits` creates `CSV/plantvillage_multiclass_labels.csv`.
4. Stratified train/validation/test CSVs are created.
5. `results/split_manifests/latest_split_manifest.json` records split hashes, row counts, class counts, and seed.
6. `src.split_guard` validates the frozen split manifest before benchmark runs.
7. `src.datasets.PlantDiseaseDataset` reads image paths and labels from CSVs.
8. `src.transforms` applies training/validation transforms.
9. `src.run_phase2_benchmark` builds models, trains, evaluates, and logs artifacts.
10. `src.phase2_analysis` turns Phase 2 artifacts into summary plots.

### Training Pipeline

The Phase 2 training pipeline:

1. Validates frozen splits.
2. Selects models from `src.model_registry`.
3. Builds dataloaders from CSV splits.
4. Applies ImageNet-style transforms.
5. Uses class-weighted cross entropy by default (`inverse_frequency`).
6. Uses AdamW optimizer.
7. Uses a cosine scheduler by default.
8. Supports early stopping.
9. Supports AMP on CUDA when requested.
10. Logs metrics and artifacts per run.

### Evaluation Pipeline

Evaluation includes:

1. Test accuracy.
2. Macro F1.
3. Per-class classification report.
4. Confusion matrix JSON and PNG.
5. Trainable parameter count.
6. Saved model size in bytes.
7. Per-run training history.
8. Aggregate mean and standard deviation across seeds.

### Deployment Approach

There is no production deployment yet. A lightweight Streamlit demo is listed as optional future work, but robustness/uncertainty analysis is prioritized over demo polish.

## 5. Technology Stack

### Language

Python is the primary language. It is used for data processing, model training, evaluation, plotting, and scripting.

### ML Framework

PyTorch is the main deep learning framework. It was chosen because:

1. It is widely used in research.
2. It gives direct control over training loops.
3. It works well with torchvision and timm.
4. It is suitable for both local and Colab execution.

The project does **not** use TensorFlow.

### Model Libraries

The project uses:

1. `torchvision` for ResNet18 and ResNet50.
2. `timm` for EfficientNet-B0 and ViT-Small.

These libraries were chosen to use well-tested standard model implementations rather than hand-rolling architectures.

### Data and Metrics Libraries

The project uses:

1. `pandas` for CSV handling.
2. `numpy` for numerical work.
3. `scikit-learn` for metrics such as accuracy, macro F1, classification reports, and confusion matrices.
4. `Pillow` for image loading.

The project does **not** use OpenCV in its current implementation.

### Visualization

The project uses:

1. `matplotlib`
2. `seaborn`

These generate benchmark plots and confusion visualizations.

### Explainability

`captum` is included for planned explainability work, though the main XAI phase is not implemented yet.

### Environment and Tooling

The recommended local interpreter is Python 3.13 on the current machine. Google Colab is used for heavier GPU training.

The project uses:

1. Git/GitHub for version control.
2. Jupyter/Colab notebooks as orchestration layers.
3. Plain JSON/CSV artifacts for reproducibility.
4. A Windows batch script `run_phase1.bat` for Phase 1 execution.

## 6. Dataset Strategy

### Dataset Used

The project uses PlantVillage-style folder images stored locally under `Datasets/`.

There are 15 classes:

1. Pepper - Healthy
2. Pepper - Bacterial Spot
3. Potato - Healthy
4. Potato - Early Blight
5. Potato - Late Blight
6. Tomato - Healthy
7. Tomato - Bacterial Spot
8. Tomato - Early Blight
9. Tomato - Late Blight
10. Tomato - Leaf Mold
11. Tomato - Septoria Leaf Spot
12. Tomato - Spider Mites
13. Tomato - Target Spot
14. Tomato - Yellow Leaf Curl Virus
15. Tomato - Mosaic Virus

### Dataset Size

The generated label CSV contains 20,638 images across 15 classes.

Split sizes:

1. Train: 14,446 images.
2. Validation: 3,096 images.
3. Test: 3,096 images.

### Dataset Preparation

Dataset preparation is handled by `src.prepare_splits`.

It:

1. Reads expected folder metadata from `src.utils.FOLDER_METADATA`.
2. Builds the multiclass label CSV.
3. Creates stratified train/validation/test splits.
4. Writes frozen CSVs.
5. Writes a split manifest with SHA256 hashes and class distributions.

### Data Cleaning and Integrity

Integrity checking is handled by `src.integrity` and `src.integrity_report`.

The current integrity report shows:

1. No missing class folders.
2. No corrupt/unreadable images.
3. No exact cross-class duplicates.
4. 14 dHash near-duplicate cross-class warning pairs at threshold `<=5`.

Important interpretation:

The integrity report has `passed: false` because warning-level dHash near-duplicate pairs exist. The project policy treats these as review flags, not automatic data-removal failures, because exact cross-class duplicates are zero and dHash can over-flag visually similar leaf images.

### Splitting Strategy

The split strategy is stratified by the 15-class label and uses seed 42.

The split manifest records:

1. File paths.
2. SHA256 hashes.
3. Row counts.
4. Per-class counts.
5. Seed.
6. Git commit at generation time.

`src.split_guard` validates the manifest before benchmark runs. It also tolerates line-ending-only CSV hash differences between Windows and Linux/Colab, while still failing on real content changes.

### Augmentation Strategy

Training transforms include:

1. Resize to 224 x 224.
2. Random horizontal flip.
3. Random vertical flip.
4. Random rotation.
5. Tensor conversion.
6. ImageNet normalization.

An optional stronger augmentation mode exists with color jitter, affine transforms, and perspective transforms, but the canonical benchmark uses the standard transform family.

Validation/test transforms use:

1. Resize to 224 x 224.
2. Tensor conversion.
3. ImageNet normalization.

### Class Imbalance

The dataset is imbalanced. For example:

1. Tomato Yellow Leaf Curl Virus has 3,208 total images.
2. Potato Healthy has 152 total images.
3. Tomato Mosaic Virus has 373 total images.

The Phase 2 benchmark uses `--class-weighting inverse_frequency` by default to mitigate class imbalance.

### Dataset Limitations

PlantVillage is clean, controlled, and visually standardized. This makes it excellent for controlled benchmarking but weak evidence for field deployment by itself. The project should explicitly avoid claiming real-world robustness until OOD evaluation is completed.

## 7. Model Strategy

### Models Implemented

The Phase 2 benchmark implements:

1. ResNet18
2. ResNet50
3. EfficientNet-B0
4. ViT-Small (`vit_small_patch16_224`)

### Why These Models Were Selected

ResNet18:

1. Strong lightweight CNN baseline.
2. Good for testing whether small models are enough for PlantVillage.

ResNet50:

1. Larger CNN baseline.
2. Useful for testing whether increased capacity helps.

EfficientNet-B0:

1. Compact modern CNN.
2. Strong performance/efficiency candidate.

ViT-Small:

1. Transformer-family comparison point.
2. Useful for investigating whether ViT-style architectures outperform CNNs on this dataset.

### Current Experimentation Status

The core 4-model x 3-seed benchmark is complete in the result artifacts. Training was run primarily in Google Colab due GPU needs.

### Alternative Approaches Considered

Considered or planned alternatives include:

1. Additional ablations, limited to avoid scope creep.
2. Severity classification, now optional and gated.
3. Grad-CAM/XAI analysis, planned for Phase 3.
4. OOD robustness and uncertainty, planned for Phase 5.
5. Demo UI, optional and lower priority than robustness.

## 8. Results So Far

### Experiments Performed

The main experiment completed so far is:

4 architectures x 3 seeds x frozen 15-class split benchmark.

Seeds:

1. 41
2. 42
3. 43

Training settings:

1. Epoch budget: 30.
2. Early stopping patience: 7.
3. Batch size: 32 for full Colab runs.
4. Scheduler: cosine.
5. Class weighting: inverse frequency.
6. Pretrained weights: enabled for benchmark runs.
7. AMP: supported and used when CUDA is available.

### Aggregate Results

Current leaderboard:

| Model | Accuracy Mean | Accuracy Std | Macro F1 Mean | Macro F1 Std | Params | Approx Checkpoint Size |
|---|---:|---:|---:|---:|---:|---:|
| resnet18 | 0.99817 | 0.00067 | 0.99845 | 0.00061 | 11.18M | 42.73 MB |
| efficientnet_b0 | 0.99795 | 0.00075 | 0.99824 | 0.00055 | 4.03M | 15.62 MB |
| vit_small_patch16_224 | 0.99731 | 0.00075 | 0.99757 | 0.00081 | 21.67M | 82.72 MB |
| resnet50 | 0.99623 | 0.00104 | 0.99614 | 0.00156 | 23.54M | 90.08 MB |

### Per-Seed Results

| Model | Seed | Test Accuracy | Macro F1 |
|---|---:|---:|---:|
| efficientnet_b0 | 41 | 0.99839 | 0.99867 |
| efficientnet_b0 | 42 | 0.99709 | 0.99763 |
| efficientnet_b0 | 43 | 0.99839 | 0.99843 |
| resnet18 | 41 | 0.99742 | 0.99780 |
| resnet18 | 42 | 0.99871 | 0.99899 |
| resnet18 | 43 | 0.99839 | 0.99855 |
| resnet50 | 41 | 0.99742 | 0.99765 |
| resnet50 | 42 | 0.99548 | 0.99453 |
| resnet50 | 43 | 0.99580 | 0.99624 |
| vit_small_patch16_224 | 41 | 0.99645 | 0.99665 |
| vit_small_patch16_224 | 42 | 0.99774 | 0.99821 |
| vit_small_patch16_224 | 43 | 0.99774 | 0.99784 |

### What Worked Well

1. The 15-class task is highly learnable.
2. All models reached very high accuracy.
3. Results are stable across seeds.
4. Smaller models performed extremely well.
5. The pipeline successfully produced auditable artifacts.

### What Did Not Work As Well

1. The dataset is too clean to prove real-world robustness.
2. `resnet50` did not outperform smaller CNNs.
3. ViT-Small did not beat the best CNN.
4. Google Colab quota limits made training operationally awkward.
5. Not all matching checkpoints are currently available locally for image-level error galleries.

### Key Findings

1. `resnet18` is currently the best overall model by aggregate accuracy and macro F1.
2. `efficientnet_b0` is the best efficiency/performance candidate because it is close to `resnet18` while being much smaller.
3. `vit_small_patch16_224` performs well but does not dominate the CNNs.
4. `resnet50` being last supports the argument that model capacity alone did not determine performance.
5. Most errors occur among visually similar tomato diseases.

### Common Confusion Patterns

Most repeated confusion pairs include:

1. Tomato Target Spot predicted as Tomato Spider Mites.
2. Tomato Late Blight predicted as Tomato Early Blight.
3. Tomato Early Blight predicted as Tomato Late Blight.
4. Tomato Yellow Leaf Curl Virus predicted as Tomato Bacterial Spot.
5. Tomato Spider Mites predicted as Tomato Target Spot.

These are plausible and useful for later qualitative discussion and explainability analysis.

## 9. Design Decisions

### Scope: 15-Class First, Severity Later

Decision:

The primary task is 15-class classification. Severity classification is optional and gated.

Reason:

Severity classification requires manual labeling, a severity rubric, reliability checks, and more time. Doing it too early would risk weakening the core project.

### Scripts as Canonical Pipeline

Decision:

Use `src/` scripts as the canonical pipeline and keep notebooks thin.

Reason:

This reduces notebook drift, makes reruns easier, and keeps local/Colab execution aligned.

### Frozen Splits

Decision:

Generate frozen CSV splits and enforce them using a split guard.

Reason:

Architecture comparisons are invalid if models are trained or tested on different splits.

### Multi-Seed Evaluation

Decision:

Use 3 seeds per architecture.

Reason:

Single-run accuracy is weak evidence. Mean and standard deviation give stronger claims about stability.

### Class Weighting

Decision:

Use inverse-frequency class weighting by default.

Reason:

The dataset is imbalanced, and macro F1 matters for minority classes.

### dHash Near-Duplicate Screening

Decision:

Use dHash near-duplicate scanning for Phase 1 integrity checks.

Reason:

dHash is fast and simple for standardized leaf images. Near-duplicate findings are treated as warning-level review flags rather than automatic hard failures.

### Colab for Heavy Training

Decision:

Use a hybrid workflow: laptop for coding and analysis, Colab for GPU training.

Reason:

Full multi-seed model sweeps are too slow on a typical laptop CPU.

### Standard-Library Reporting Fix

Decision:

`src.phase2_reporting.py` was rewritten to avoid depending on pandas.

Reason:

A Colab session hit a NumPy/pandas binary incompatibility during summary rebuild. Reporting only needed simple CSV aggregation, so the dependency was unnecessary.

### Checkpoint Hash Validation

Decision:

`src.phase2_error_analysis.py` refuses to generate image-level mistake galleries unless local checkpoint hashes match the recorded run logs.

Reason:

Generating qualitative examples from stale model weights would be actively misleading.

## 10. Future Implementation Plan

### Immediate Next Steps

1. Recover matching `models/phase2/.../best.pth` checkpoints from Colab/Drive if possible.
2. Run `src.phase2_error_analysis --models all` once matching checkpoints are available.
3. Generate wrong-prediction CSVs and image galleries.
4. Implement statistical comparison between `resnet18` and `vit_small_patch16_224`.
5. Start writing the Phase 2 methodology/results section.

### Phase 2 Remaining Work

1. Statistical testing for top CNN vs top ViT.
2. Image-level error analysis if checkpoints are recovered.
3. Dissertation-ready tables and captions.
4. Clear limitations section around PlantVillage.

### Phase 3: Explainability

Planned:

1. Generate Grad-CAM or equivalent heatmaps.
2. Compare attention behavior across architectures.
3. Manually annotate 50-60 disease-region images.
4. Compute IoU-style overlap metrics.
5. Discuss whether attention aligns with disease symptoms.

### Phase 4: Optional Severity Track

Only start if core work is ahead of schedule.

Possible tasks:

1. Define severity rubric.
2. Label 200-300 images.
3. Compute intra-rater agreement after relabeling a subset.
4. Train a severity baseline.
5. Treat severity as a pilot if labels are noisy.

### Phase 5: Robustness and Uncertainty

Planned:

1. Build small OOD image set.
2. Evaluate benchmark models on OOD data.
3. Compute calibration metrics such as ECE.
4. Explore MC Dropout uncertainty.
5. Relate uncertainty to error rate.

### Phase 6: Writing and Finalization

Planned:

1. Assemble dissertation from rolling write-ups.
2. Finalize figures and tables.
3. Include limitations and future work.
4. Prepare clean evidence package.

## 11. Risks and Challenges

### Technical Risks

1. Colab GPU quota can interrupt long runs.
2. Local and Colab environments may differ.
3. Large checkpoint files may be hard to version or transfer.
4. Notebook outputs can drift from source scripts if not managed.

### Research Risks

1. PlantVillage performance may saturate, making architectural differences small.
2. High accuracy can look impressive but may not translate to real-world robustness.
3. Without statistical testing, model ranking may be overinterpreted.
4. XAI can be subjective unless grounded in annotation metrics.

### Dataset Risks

1. PlantVillage images are controlled and may not represent field conditions.
2. Class imbalance is present.
3. dHash near-duplicate warnings exist and should remain documented.
4. Some classes are visually similar, especially tomato diseases.

### Evaluation Risks

1. Test-set results are in-distribution.
2. Checkpoint mismatch can invalidate image-level mistake galleries.
3. Confusion matrices are useful but not enough without qualitative examples.
4. Claims should distinguish benchmark performance from deployment readiness.

### Time Risks

The student has significant time remaining, but scope creep is still the main danger. The project should avoid adding many features before writing up the strong results already obtained.

### Known Weaknesses

1. Statistical testing is pending.
2. OOD evaluation is pending.
3. XAI is pending.
4. Matching checkpoints for all 12 Phase 2 runs are not fully available locally.
5. The current analysis is strong but still needs dissertation narrative.

## 12. Advice for Another AI Assistant

### Important Context

This project has a lot of history. Do not treat it as a blank repo or a simple classifier project. The owner deliberately pushed the project toward reproducibility, rigorous evidence, and dissertation-quality framing.

The current project name is:

**Computer Vision Plant Disease Classification**

Avoid older names such as "stress detection" unless referring to historical scope changes.

### Common Misunderstandings to Avoid

1. Do not call the project multimodal. It is currently image-only.
2. Do not say TensorFlow is used. It is not.
3. Do not say OpenCV is used. It is not currently part of the implementation.
4. Do not overclaim novelty. The novelty is not a new architecture; it is the rigor of the empirical study and planned explainability/robustness analysis.
5. Do not interpret high PlantVillage accuracy as real-world deployment readiness.
6. Do not regenerate splits casually. Frozen splits are central to the project.
7. Do not create qualitative mistake galleries from mismatched checkpoints.
8. Do not push severity classification too early; it is intentionally optional and gated.

### Current Priorities

The best next work is not more model training. The best next work is:

1. Recover matching Phase 2 checkpoints if available.
2. Run image-level error analysis.
3. Implement statistical comparison of best CNN vs best ViT.
4. Begin writing Phase 2 methodology and results.
5. Prepare for Phase 3 explainability only after Phase 2 analysis is complete.

### Areas Requiring Caution

Checkpoint handling:

Only `seed_41` checkpoint files are visible locally at the time of this document. The result artifacts cover all 12 runs, but image-level inference needs matching checkpoint files. The error-analysis script validates hashes for this reason.

Integrity report:

The latest integrity report has `passed: false` due dHash near-duplicate warnings. This is expected under the current policy and does not mean Phase 1 failed.

Colab continuation:

Some Phase 2 work was run across multiple Colab sessions/accounts due GPU quota limits. This should be described honestly as continuation/recovery using persisted Google Drive artifacts, not as fully fresh independent runs.

Markdown folders:

Some local documentation folders are ignored by git, but they contain important project memory. If reviewing only tracked GitHub files, some context may be missing.

### Suggested Framing for Feedback

When reviewing this project, assess it on:

1. Research question clarity.
2. Experimental protocol fairness.
3. Reproducibility and artifact discipline.
4. Validity of claims given PlantVillage limitations.
5. Quality of Phase 2 analysis.
6. Readiness for Phase 3 XAI and Phase 5 robustness work.

The project is already stronger than a basic undergraduate classifier project. The main remaining challenge is turning the strong implementation and benchmark evidence into a polished research narrative with statistical testing, qualitative analysis, and honest limitations.

## Appendix A: Key Repository Areas

`src/`

Canonical implementation modules for dataset loading, transforms, split generation, model registry, training, benchmarking, logging, and analysis.

`CSV/`

Canonical label and split CSVs:

1. `plantvillage_multiclass_labels.csv`
2. `plantvillage_train.csv`
3. `plantvillage_val.csv`
4. `plantvillage_test.csv`

`results/`

Stores manifests, smoke artifacts, Phase 2 run logs, confusion matrices, leaderboards, and analysis plots.

`models/`

Stores model checkpoints. Large weights are generally not suitable for normal git tracking.

`Google Colab/`

Contains thin notebooks for Colab execution:

1. Phase 1 live smoke artifact notebook.
2. Phase 2 benchmark runner notebook.
3. Legacy Plant Disease notebook retained for context.

`notebooks/`

Legacy/local notebooks. `01` to `03` are aligned with current `src` pipeline; severity notebooks are parked/deprecated.

`Markdown Files/`

Local planning, documentation, reviews, and phase checklists. This folder may be gitignored but is important for project history.

## Appendix B: Commands Worth Knowing

Run Phase 1 locally:

```bash
run_phase1.bat
```

Generate Phase 2 analysis plots:

```bash
py -3.13 -m src.phase2_analysis
```

Attempt checkpoint-based error analysis:

```bash
py -3.13 -m src.phase2_error_analysis --models all
```

Run Phase 2 benchmark dry run:

```bash
py -3.13 -m src.run_phase2_benchmark --dry-run --models resnet18,resnet50,efficientnet_b0,vit_small_patch16_224 --seeds 41 --epochs 1 --batch-size 4 --num-workers 0
```

Full Phase 2 benchmark command used in Colab-style execution:

```bash
python -m src.run_phase2_benchmark --models resnet18,resnet50,efficientnet_b0,vit_small_patch16_224 --seeds 41,42,43 --epochs 30 --batch-size 32 --num-workers 2 --scheduler cosine --class-weighting inverse_frequency --pretrained --amp --resume
```

## Appendix C: Recommended Project Title

Recommended title:

**Computer Vision Plant Disease Classification**

Possible dissertation-style title:

**A Reproducible Comparative Study of CNN and Vision Transformer Architectures for Plant Disease Classification**

Avoid:

1. "Multimodal" unless a non-image modality is actually added.
2. "Stress detection" unless the severity/stress track becomes active again.
3. "Novel architecture" unless a genuinely new model contribution is developed.
