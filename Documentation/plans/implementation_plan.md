# 🌿 Plant Disease Detection — Phased Implementation Plan (15 Months)

## My Honest Assessment of Gemini's Advice

Before the timeline, let me give you a straight take on each of Gemini's suggestions:

| Suggestion | My Verdict | Why |
|---|---|---|
| Kill the mobile app focus | **Partially agree** | Don't kill it — just make it a **Streamlit/Gradio demo** (2-3 days of work, not weeks). It demonstrates end-to-end thinking, which Imperial actually values. But yes, 90% of effort should be on the AI. |
| Bayesian Neural Networks | **Skip this** | BNNs are genuinely painful to implement properly and won't give you better results on this task. Instead, use **Monte Carlo Dropout** — you get uncertainty estimates for free with ~20 lines of code. Same intellectual flex, 1/10th the effort. |
| Vision Transformers vs CNNs | **Yes, essential** | Architecture comparison is the backbone of a strong dissertation. Do this. |
| Grad-CAM / XAI | **Yes, essential** | This is your single most impressive visual artifact. Examiners and Imperial admissions will remember heatmaps showing "the model looks at the lesion, not the background." |
| Edge AI / Pruning / Quantization | **Deprioritize** | Interesting but orthogonal to your research story. Only do this if you have time left at the end. The "farmer's phone" angle is an engineering story, not a research story. |
| Multimodal fusion (weather data) | **Skip** | Sounds impressive but PlantVillage has no metadata. You'd need a different dataset entirely. Not worth the pivot. |
| Few-shot / Zero-shot with CLIP | **Yes, good fit** | You've already started down this road with severity labelling. Lean into it. |
| GANs for synthetic data | **Skip** | Training GANs reliably is a PhD-level headache. Your time is better spent elsewhere. |

> [!IMPORTANT]
> **Can you do a web app AND make it research-heavy?** Yes, absolutely. A simple **Streamlit** app takes 2-3 days and becomes a nice cherry on top. The mistake would be spending weeks on a React/Flutter frontend. The app should just be a thin demo wrapper around your trained model.

---

## Suggested Research Title

> *"Beyond Binary Diagnosis: Explainable Multi-Task Vision Models for Plant Disease Classification and Severity Estimation with Uncertainty Quantification"*

This title signals: multi-task learning (novel), explainability (Imperial's Safe AI group), uncertainty (mathematical rigor), and goes beyond simple classification.

---

## The Plan: 6 Phases Over 15 Months

### Phase 1: Foundation & Cleanup (Weeks 1–3)
*Goal: Get a solid, professional codebase with all data included.*

- [ ] **Unzip the full PlantVillage dataset** — include ALL classes (add Tomato_LateBlight and Potato_LateBlight)
- [ ] **Create `README.md`** with project description, setup instructions, preliminary results
- [ ] **Create `requirements.txt`** — pin all versions (`torch==2.x`, `torchvision`, `scikit-learn`, `matplotlib`, `Pillow`, `captum`, `timm`, etc.)
- [ ] **Refactor code into a `src/` package:**
  - `src/datasets.py` — `PlantBinaryDataset`, `PlantMultiClassDataset`, `PlantSeverityDataset`
  - `src/transforms.py` — train/val/test transform pipelines, including stronger augmentations
  - `src/training.py` — generic `train_model()` and `evaluate_model()` functions
  - `src/visualization.py` — plotting functions (loss curves, confusion matrices, Grad-CAM)
  - `src/utils.py` — config constants, path management, seed setting
- [ ] **Convert from binary to multi-class classification** — the label should now be the disease type (healthy, bacterial_spot, early_blight, late_blight), not just 0/1
- [ ] **Re-run notebook 01** with all 8 folders, generate new CSVs
- [ ] **Add model saving** — `torch.save()` after training, `torch.load()` for inference
- [ ] **Set random seeds everywhere** for reproducibility (`torch.manual_seed`, `numpy.random.seed`, `random.seed`)
- [ ] **Move NB06 to an `experiments/` folder** — it's fine to keep, just separate it from the main pipeline
- [ ] **Add a proper EDA (Exploratory Data Analysis) notebook:**
  - Class distribution bar charts
  - Sample images from each class
  - Image dimension statistics
  - Channel-wise mean/std calculation (instead of hardcoded ImageNet values)

**Time: ~15-20 hours of focused work**

---

### Phase 2: Core Research — Architecture Comparison (Weeks 4–10)
*Goal: This becomes a central chapter of your dissertation.*

- [ ] **Train and compare 4+ architectures:**
  - ResNet18 (your baseline)
  - ResNet50 (deeper, does more depth help?)
  - EfficientNet-B0 (efficiency-focused, from `timm` library)
  - ViT-Small or ViT-Base (Vision Transformer, from `timm`)
  - Optional: ConvNeXt-Tiny (modern CNN that competes with ViTs)
- [ ] **For each architecture, run the same fair experiment:**
  - Same data splits, same augmentations, same optimizer (AdamW)
  - Same number of epochs (e.g., 30 with early stopping)
  - Add **learning rate scheduler** (CosineAnnealingWarmRestarts or ReduceLROnPlateau)
  - Log all training curves
- [ ] **Full evaluation for each model:**
  - Accuracy, Precision, Recall, F1-score per class
  - Confusion matrix heatmap
  - ROC curves and AUC per class (one-vs-rest)
  - Inference time per image (latency comparison)
  - Model size (parameter count + disk size)
- [ ] **Ablation study notebook:**
  - Augmentation ablation: which augmentations help? (test ColorJitter, CutMix, RandAugment)
  - Learning rate ablation: 1e-3 vs 1e-4 vs 1e-5
  - Feature extraction vs fine-tuning: freeze all layers except FC vs fine-tune everything
- [ ] **Results table** comparing all models — this becomes a key figure in the dissertation

| Model | Params | Accuracy | F1 (macro) | AUC | Inference (ms) |
|---|---|---|---|---|---|
| ResNet18 | 11.7M | ? | ? | ? | ? |
| ResNet50 | 25.6M | ? | ? | ? | ? |
| EfficientNet-B0 | 5.3M | ? | ? | ? | ? |
| ViT-Small | 22M | ? | ? | ? | ? |

**ML libraries to use:**
- `timm` (PyTorch Image Models) — for ViT and EfficientNet
- `sklearn.metrics` — for classification_report, roc_auc_score, confusion_matrix
- `torch.optim.lr_scheduler` — for learning rate scheduling

**Time: ~30-40 hours**

---

### Phase 3: Explainability / XAI (Weeks 11–15)
*Goal: Prove your model is learning the right features. This is visually stunning and academically rigorous.*

- [ ] **Grad-CAM implementation:**
  - Use Facebook's `captum` library (or implement from scratch for extra credit)
  - Generate heatmaps for correct AND incorrect predictions
  - Show side-by-side: original image → Grad-CAM overlay → disease region highlighted
- [ ] **Compare Grad-CAM across architectures:**
  - Does ResNet look at the same regions as ViT?
  - ViTs have attention maps built-in — visualize the self-attention heads
  - This comparison is a genuine **research contribution**
- [ ] **Botanical validation:**
  - For 20-30 images, annotate where the disease symptoms actually are (bounding box or rough region)
  - Compute overlap between Grad-CAM activations and actual disease regions
  - This bridges AI with domain knowledge — Imperial will love this
- [ ] **Write-up:** Frame this as "Can we trust the model's predictions?" Align with Imperial's Safe & Trusted AI research group

**ML libraries:**
- `captum` — Grad-CAM, Integrated Gradients, SHAP
- `matplotlib` / `PIL` — for overlaying heatmaps

**Time: ~20-25 hours**

---

### Phase 4: Severity Estimation (Weeks 16–22)
*Goal: This is your unique angle. Most undergrad projects stop at classification.*

- [ ] **Severity labelling strategy** (choose one or combine):
  - **Option A: Semi-supervised with CLIP** — Use CLIP scores as weak labels, manually verify a subset (100-200 images). You've already prototyped this.
  - **Option B: Manual labelling with a simple tool** — Build a quick labelling script (show image → press 0/1/2/3 → save). 200-300 labels is enough if balanced.
  - **Option C: Continuous severity regression** — Instead of 0/1/2/3, have CLIP output a continuous score 0.0–1.0 and train a regression head
- [ ] **Multi-task learning model:**
  - Shared CNN/ViT backbone
  - Classification head → disease type
  - Regression/ordinal head → severity score
  - Joint loss = `disease_loss + lambda * severity_loss`
  - This is a genuine novel architecture contribution
- [ ] **Ordinal regression** for severity (the ordering 0 < 1 < 2 < 3 matters):
  - Use the CORAL framework or simple cumulative logits
  - Compare against standard classification and regression
- [ ] **Evaluate severity independently:**
  - MAE and RMSE (for regression)
  - Quadratic Weighted Kappa (standard for ordinal scales)
  - Per-class accuracy (for classification)

**Time: ~35-40 hours**

---

### Phase 5: Robustness & Uncertainty + Demo (Weeks 23–28)
*Goal: This is what separates a 1st from a high 1st.*

- [ ] **Out-of-distribution testing:**
  - Collect 50-100 real-world leaf images from Google Images, iNaturalist, or your own phone
  - Run your best model on these — expect a significant accuracy drop
  - Analyze WHY it fails (background differences, lighting, angle, leaf variety)
  - This honest analysis is more valuable than 99.72% accuracy on PlantVillage
- [ ] **Monte Carlo Dropout for uncertainty:**
  - At inference, run the model 30 times with dropout enabled
  - Compute mean prediction and standard deviation (= uncertainty)
  - Show that uncertain predictions correlate with incorrect predictions
  - Plot calibration curve: does 80% confidence = 80% actual accuracy?
  - Compute **Expected Calibration Error (ECE)** — an advanced metric Imperial will recognize
  - **This is ~20 lines of code but worth an entire dissertation section**
- [ ] **Streamlit demo app:**
  - Upload image → get disease prediction + severity + confidence + Grad-CAM heatmap
  - Simple, clean, and demonstrates the full pipeline
  - Takes 2-3 days max with Streamlit

**ML libraries:**
- `streamlit` — for the demo app
- `torch.nn.functional.dropout` — MC Dropout (just keep dropout on during eval)
- `netcal` or manual implementation — for calibration curves

**Time: ~25-30 hours**

---

### Phase 6: Dissertation Writing & Polish (Weeks 29–40+)
*Goal: Convert all your work into a polished, submission-ready document.*

- [ ] **Introduction** — Problem statement, motivation, research questions
- [ ] **Literature Review** — CNNs for plant disease, ViTs, XAI in agriculture, severity estimation
- [ ] **Methodology** — Dataset, preprocessing, architectures, training procedure, evaluation metrics
- [ ] **Results** — Tables, figures, Grad-CAMs, calibration curves, severity results
- [ ] **Discussion** — What worked, what didn't, the generalization gap, uncertainty analysis
- [ ] **Conclusion & Future Work** — Limitations, what you'd do with another year
- [ ] **Clean up all notebooks** — make them presentation-ready with markdown headers and explanations
- [ ] **Generate all final figures** in high resolution for the dissertation
- [ ] **Proofread, get feedback from supervisor, iterate**

**Time: ~60-80 hours (writing always takes longer than you think)**

---

## Timeline Summary

| Phase | Duration | Cumulative | Focus |
|---|---|---|---|
| 1: Foundation | Weeks 1–3 | 3 weeks | Code quality, all data, multi-class |
| 2: Architecture Comparison | Weeks 4–10 | 10 weeks | ResNet vs EfficientNet vs ViT + ablation |
| 3: XAI / Grad-CAM | Weeks 11–15 | 15 weeks | Explainability, botanical validation |
| 4: Severity | Weeks 16–22 | 22 weeks | CLIP labels, multi-task, ordinal regression |
| 5: Robustness + Demo | Weeks 23–28 | 28 weeks | OOD testing, MC Dropout, Streamlit app |
| 6: Writing | Weeks 29–40 | 40 weeks | Full dissertation + figures |
| Buffer | Weeks 41–44+ | ~11 months total | Margin for delays, revisions, supervisor feedback |

> [!TIP]
> You have **~15 months but only need ~11**. The 4-month buffer is intentional — things always take longer. Use it for revision cycles with your supervisor, or to go deeper on whichever phase interests you most.

---

## Evaluation Metrics to Include

For an Imperial-level project, go beyond accuracy:

| Metric | What it Shows | Library |
|---|---|---|
| Accuracy | Basic correctness | `sklearn` |
| Precision / Recall / F1 | Per-class performance | `sklearn.metrics.classification_report` |
| Macro F1 | Handles class imbalance fairly | `sklearn` |
| ROC-AUC (per class) | Ranking quality | `sklearn.metrics.roc_auc_score` |
| Confusion Matrix | Error patterns | `sklearn.metrics.confusion_matrix` |
| ECE (Expected Calibration Error) | Confidence reliability | Manual or `netcal` |
| Calibration Curve | Visual confidence check | `sklearn.calibration.calibration_curve` |
| QWK (Quadratic Weighted Kappa) | Ordinal severity agreement | `sklearn.metrics.cohen_kappa_score` |
| MAE / RMSE | Severity regression error | `sklearn.metrics` |
| Inference Latency | Practical deployment cost | `time.perf_counter` |
| Parameter Count | Model complexity | `sum(p.numel() for p in model.parameters())` |

---

## The Labelling Question

> *"Should I keep manually labelling while unzipping?"*

**Short answer: Not yet.** Here's why:

1. First finish Phase 1 (get all data included, multi-class working)
2. In Phase 4, when you actually need severity labels, build a **proper labelling tool** — a simple Python script that shows an image and waits for a keypress (0/1/2/3). This is 10x faster than whatever you were doing before
3. You only need **~200-300 labelled images** because you'll also use CLIP as a weak labeller for the rest
4. The semi-supervised approach (CLIP labels + small manual validation set) is itself a research contribution

---

## What This Plan Achieves

If you complete Phases 1–5, your project will have:
- ✅ Multi-class disease classification (not trivial binary)
- ✅ 4+ architecture comparison with fair benchmarking
- ✅ Comprehensive evaluation with advanced metrics
- ✅ Grad-CAM visualizations proving model trustworthiness
- ✅ Severity estimation via multi-task learning (novel)
- ✅ Uncertainty quantification via MC Dropout
- ✅ Out-of-distribution robustness analysis
- ✅ A working demo application
- ✅ Clean, well-documented code

This is genuinely more than most MSc dissertations, let alone undergraduate ones. It will absolutely support a first-class grade and make a strong case in an Imperial application.
