# 🌿 Plant Disease Detection — Revised Implementation Plan (15 Months)

> [!NOTE]
> **v2 — Updated after ChatGPT 5.3 peer review.** Key additions: dataset integrity checks, multi-seed statistical protocol, go/no-go gates, expanded XAI validation, severity annotation rubric, rolling write-ups, and reframed novelty claims.

---

## Gemini Advice Assessment (Unchanged from v1)

| Suggestion | Verdict | Why |
|---|---|---|
| Kill the mobile app focus | **Partially agree** | Make a **Streamlit/Gradio demo** (2-3 days). 90% effort on AI. |
| Bayesian Neural Networks | **Skip** | Use **Monte Carlo Dropout** instead — same uncertainty, 1/10th effort. |
| Vision Transformers vs CNNs | **Essential** | Architecture comparison = backbone of the dissertation. |
| Grad-CAM / XAI | **Essential** | Single most impressive visual artifact for examiners. |
| Edge AI / Pruning | **Deprioritize** | Only if time remains at the end. |
| Multimodal fusion | **Skip** | PlantVillage has no metadata. Not worth the pivot. |
| Few-shot / CLIP | **Good fit** | Already started with severity labelling. Lean in. |
| GANs | **Skip** | PhD-level headache. Not worth it. |

---

## Research Title

> *"Beyond Binary Diagnosis: Explainable Multi-Task Vision Models for Plant Disease Classification and Severity Estimation with Uncertainty Quantification"*

---

## The Plan: 6 Phases Over 15 Months

### Phase 1: Foundation & Cleanup (Weeks 1–4)

*Goal: Professional codebase, clean data, reproducible pipeline.*

- [ ] **Include ALL PlantVillage classes** (uncomment Tomato_LateBlight, Potato_LateBlight)
- [ ] **Dataset integrity checks** *(new)*:
  - Run perceptual hash (pHash) to detect near-duplicate images across classes
  - Verify no filename overlap between train/val/test splits (leakage test)
  - Audit for missing/corrupt files
  - Document total counts per class per split
- [ ] **Convert to multi-class classification** (healthy, bacterial_spot, early_blight, late_blight)
- [ ] **Re-run notebook 01** with all 8 folders, generate new CSVs
- [ ] **Freeze splits** — save train/val/test CSVs and never regenerate them again
- [ ] **Refactor code into `src/` package:**
  - `src/datasets.py`, `src/transforms.py`, `src/training.py`, `src/visualization.py`, `src/utils.py`
- [ ] **Add model saving/loading** — `torch.save()` / `torch.load()`
- [ ] **Set random seeds everywhere** (torch, numpy, random, CUDA)
- [ ] **Set up experiment tracking** *(new)*:
  - Simple option: JSON log per run (model, hyperparams, metrics, seed)
  - Better option: `wandb` (free for academics, 5 min setup)
- [ ] **Create [requirements.txt](file:///c:/Users/willi/Documents/GitHub/Plant%20Disease%20Detection%20CV/Main/requirements.txt)** with pinned versions
- [ ] **EDA notebook**: class distributions, sample images, image dimensions, channel-wise mean/std
- [ ] **Move NB06 to `experiments/`**

**Time: ~20-25 hours** *(adjusted +30%)*

> [!IMPORTANT]
> **Go/No-Go Gate (end of Phase 1):**
> ✅ All 8 class folders present, no duplicates across splits, multi-class CSV generated, `src/` importable, one model trains + saves successfully.
> ❌ If dataset issues found: fix before proceeding. Do NOT start Phase 2 with unverified data.

---

### Phase 2: Architecture Comparison (Weeks 5–12)

*Goal: Rigorous empirical comparison — the central dissertation chapter.*

- [ ] **Train 4 architectures** with identical setup:
  - ResNet18 (baseline), ResNet50, EfficientNet-B0, ViT-Small (all via `timm`)
  - Same splits, augmentations, optimizer (AdamW), epochs (30 + early stopping)
  - Learning rate scheduler (CosineAnnealingWarmRestarts or ReduceLROnPlateau)
- [ ] **Multi-seed protocol** *(new)*:
  - Run each model with **3 seeds** (e.g., 42, 123, 456)
  - Report **mean ± std** for all metrics
  - This is ~12 training runs total (4 models × 3 seeds)
- [ ] **Full evaluation per model**:
  - Accuracy, Precision, Recall, F1 (macro), ROC-AUC (one-vs-rest)
  - Confusion matrix heatmap
  - Inference latency, parameter count, disk size
- [ ] **Paired significance test** *(new)*:
  - McNemar's test between best CNN and ViT on the test set
  - Report p-value — "the difference is/is not statistically significant"
- [ ] **Ablation study**:
  - Augmentation ablation (ColorJitter, CutMix, RandAugment)
  - Learning rate comparison (1e-3, 1e-4, 1e-5)
  - Feature extraction vs full fine-tuning
- [ ] **Results table** with mean±std across seeds:

| Model | Params | Accuracy | F1 (macro) | AUC | Latency (ms) |
|---|---|---|---|---|---|
| ResNet18 | 11.7M | ?±? | ?±? | ?±? | ? |
| ResNet50 | 25.6M | ?±? | ?±? | ?±? | ? |
| EfficientNet-B0 | 5.3M | ?±? | ?±? | ?±? | ? |
| ViT-Small | 22M | ?±? | ?±? | ?±? | ? |

- [ ] **Rolling write-up** *(new)*: Draft methodology section (dataset, preprocessing, training protocol)

**Time: ~40-50 hours** *(adjusted +30%)*

> [!IMPORTANT]
> **Go/No-Go Gate (end of Phase 2):**
> ✅ All 4 models trained (3 seeds each), results table complete, significance test run, methodology draft written.
> ❌ **Fallback**: If ViT fails to converge or hardware is too slow, keep 3 models and deepen analysis quality instead of adding breadth.

---

### Phase 3: Explainability / XAI (Weeks 13–17)

*Goal: Prove your model looks at disease symptoms, not background artifacts.*

- [ ] **Grad-CAM implementation** (via `captum` or from scratch):
  - Heatmaps for correct AND incorrect predictions
  - Side-by-side: original → Grad-CAM overlay → disease region
- [ ] **Cross-architecture comparison**:
  - Does ResNet attend to the same regions as ViT?
  - Visualize ViT self-attention heads
  - This is a strong empirical comparison (not "novel research," but rigorous and valuable)
- [ ] **Botanical validation** (expanded from 20-30 to **50-60 images** *(revised)*):
  - Manually annotate disease symptom regions (bounding boxes)
  - Compute IoU between Grad-CAM activations and annotations
  - Report mean IoU ± std per architecture
  - This sample size supports basic statistical conclusions
- [ ] **Rolling write-up**: Draft XAI results section

**Time: ~25-30 hours** *(adjusted +20%)*

> [!IMPORTANT]
> **Go/No-Go Gate (end of Phase 3):**
> ✅ Grad-CAM heatmaps generated for all architectures, IoU computed on 50+ images, XAI results draft written.
> ❌ **Fallback**: If IoU results are weak, reframe as "analysis of model attention patterns" rather than "trustworthiness proof."

---

### Phase 4: Severity Estimation (Weeks 18–25)

*Goal: Move beyond classification. This differentiates the project from standard plant disease work.*

- [ ] **Annotation rubric** *(new)*:
  - Define severity levels with explicit visual criteria:
    - 0 = Healthy (no visible symptoms)
    - 1 = Mild (< 10% leaf affected)
    - 2 = Moderate (10-50% affected)
    - 3 = Severe (> 50% affected)
  - Include reference images for each level
- [ ] **Labelling protocol**:
  - Build simple labelling script (show image → keypress 0/1/2/3)
  - Label 200-300 images manually
  - **Intra-rater agreement check** *(new)*: Re-label 50 images after 2 weeks, compute Cohen's kappa
  - Use CLIP as weak labeller for remaining images
- [ ] **Multi-task learning model**:
  - Shared backbone (best architecture from Phase 2)
  - Classification head → disease type
  - Ordinal/regression head → severity
  - Joint loss = `disease_loss + λ * severity_loss`
- [ ] **Ordinal regression** (CORAL framework or cumulative logits)
- [ ] **Severity evaluation**: MAE, RMSE, Quadratic Weighted Kappa
- [ ] **Rolling write-up**: Draft severity methodology + results

**Time: ~45-55 hours** *(adjusted +30%)*

> [!IMPORTANT]
> **Go/No-Go Gate (end of Phase 4):**
> ✅ 200+ images labelled, intra-rater kappa > 0.6, multi-task model trained, severity metrics reported.
> ❌ **Fallback**: If CLIP weak labels are too noisy (kappa < 0.4 vs manual), drop CLIP and use only the manual labels with a simpler ordinal model.

---

### Phase 5: Robustness & Uncertainty + Demo (Weeks 26–32)

*Goal: Honest analysis of where the model fails. This separates a 1st from a high 1st.*

- [ ] **Out-of-distribution testing**:
  - Collect 50-100 real-world leaf images (Google Images, iNaturalist, own phone)
  - Run best model — report accuracy drop honestly
  - Analyze failure modes (background, lighting, angle, variety)
- [ ] **Monte Carlo Dropout for uncertainty**:
  - 30 forward passes with dropout enabled at inference
  - Compute mean prediction + std (= uncertainty)
  - Calibration curve + Expected Calibration Error (ECE)
  - Show: uncertain predictions correlate with incorrect predictions
- [ ] **Streamlit demo app**:
  - Upload image → disease prediction + severity + confidence + Grad-CAM
  - 2-3 days of work
- [ ] **Rolling write-up**: Draft robustness + uncertainty sections

**Time: ~30-40 hours** *(adjusted +30%)*

> [!IMPORTANT]
> **Go/No-Go Gate (end of Phase 5):**
> ✅ OOD results documented, ECE computed, demo functional, all rolling write-ups merged into draft.
> ❌ **Fallback**: If time is tight, skip the Streamlit app — it's nice-to-have, not essential for the grade.

---

### Phase 6: Dissertation Writing & Polish (Weeks 33–44+)

*Goal: Convert rolling drafts into a polished, submission-ready document.*

- [ ] **Introduction** — Problem statement, motivation, research questions
- [ ] **Literature Review** — CNNs for plant disease, ViTs, XAI in agriculture, severity estimation
- [ ] **Methodology** — Merge rolling drafts, add dataset + evaluation protocol details
- [ ] **Results** — Final tables, figures, Grad-CAMs, calibration curves
- [ ] **Discussion** — What worked, what didn't, generalization gap, uncertainty analysis
- [ ] **Conclusion & Future Work** — Limitations, what you'd do with another year
- [ ] **Clean up all notebooks** — presentation-ready with markdown headers
- [ ] **Generate final figures** in high resolution
- [ ] **Proofread + supervisor feedback cycles**

**Time: ~80-100 hours** *(adjusted significantly — writing always takes longer than expected)*

---

## Timeline Summary

| Phase | Duration | Cumulative | Focus | Go/No-Go |
|---|---|---|---|---|
| 1: Foundation | Weeks 1–4 | 4 weeks | Data integrity, multi-class, `src/` | All data verified, pipeline works |
| 2: Architecture | Weeks 5–12 | 12 weeks | 4 models × 3 seeds + ablation | Results table complete |
| 3: XAI | Weeks 13–17 | 17 weeks | Grad-CAM, 50+ IoU annotations | Heatmaps + IoU computed |
| 4: Severity | Weeks 18–25 | 25 weeks | Labelling, multi-task, ordinal | 200+ labels, kappa > 0.6 |
| 5: Robustness | Weeks 26–32 | 32 weeks | OOD, MC Dropout, demo | Draft sections written |
| 6: Writing | Weeks 33–44 | 44 weeks | Full dissertation | Submission-ready |
| Buffer | Weeks 45–60 | ~15 months | Revisions, supervisor feedback | — |

> [!TIP]
> **Rolling write-ups** from Phase 2 onward mean Phase 6 is mostly assembly + polish, not starting from scratch.

---

## Evaluation Metrics

| Metric | What it Shows | Library |
|---|---|---|
| Accuracy (mean±std) | Basic correctness across seeds | `sklearn` |
| Precision / Recall / F1 | Per-class performance | `sklearn.metrics.classification_report` |
| Macro F1 (mean±std) | Handles class imbalance fairly | `sklearn` |
| ROC-AUC per class | Ranking quality | `sklearn.metrics.roc_auc_score` |
| Confusion Matrix | Error patterns | `sklearn.metrics.confusion_matrix` |
| McNemar's test p-value | Statistical significance between models | `statsmodels` or manual |
| ECE | Confidence reliability | Manual or `netcal` |
| Calibration Curve | Visual confidence check | `sklearn.calibration` |
| QWK | Ordinal severity agreement | `sklearn.metrics.cohen_kappa_score` |
| Cohen's kappa (intra-rater) | Label consistency | `sklearn.metrics.cohen_kappa_score` |
| MAE / RMSE | Severity regression error | `sklearn.metrics` |
| IoU (Grad-CAM vs annotation) | XAI correctness | Manual computation |
| Inference Latency | Deployment cost | `time.perf_counter` |
| Parameter Count | Model complexity | `sum(p.numel() ...)` |

---

## What This Plan Achieves

If you complete Phases 1–5, your project will have:
- ✅ Multi-class disease classification with verified, leakage-free data
- ✅ 4-architecture comparison with 3-seed statistical protocol
- ✅ Significance testing between key models
- ✅ Comprehensive evaluation with 14+ metrics
- ✅ Grad-CAM visualizations validated against 50+ manual annotations
- ✅ Severity estimation via multi-task learning with defensible labels
- ✅ Uncertainty quantification via MC Dropout + calibration analysis
- ✅ Honest out-of-distribution robustness analysis
- ✅ A working demo application
- ✅ Clean, well-documented, reproducible code

This represents rigorous empirical work that goes significantly beyond a typical undergraduate project. The combination of statistical protocol, explainability validation, and multi-task severity estimation provides strong evidence of research capability for a postgraduate application.
