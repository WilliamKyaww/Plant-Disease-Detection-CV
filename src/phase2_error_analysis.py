"""
Phase 2 checkpoint-based misclassification analysis.

Loads the best locally available checkpoint for each model, runs inference on
the test split, and saves per-model wrong-prediction summaries and galleries.
"""

import argparse
import json
import os
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, Subset

try:
    from src.datasets import PlantDiseaseDataset
    from src.experiment_log import sha256_file
    from src.model_registry import CANONICAL_MODELS, build_model
    from src.split_guard import resolve_project_path
    from src.training import load_model
    from src.transforms import get_val_transform
    from src.utils import CLASS_NAMES, DATASETS_DIR, NUM_CLASSES, PROJECT_ROOT, get_device
except ImportError:
    from .datasets import PlantDiseaseDataset
    from .experiment_log import sha256_file
    from .model_registry import CANONICAL_MODELS, build_model
    from .split_guard import resolve_project_path
    from .training import load_model
    from .transforms import get_val_transform
    from .utils import CLASS_NAMES, DATASETS_DIR, NUM_CLASSES, PROJECT_ROOT, get_device


def _load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _resolve_image_path(image_path: str) -> str:
    norm_path = image_path.replace("\\", "/")
    if os.path.isabs(norm_path):
        return norm_path
    if norm_path.lower().startswith("datasets/"):
        relative = norm_path.split("/", 1)[1]
        return os.path.join(DATASETS_DIR, *relative.split("/"))
    return resolve_project_path(norm_path, project_root=PROJECT_ROOT)


def _discover_best_available_runs(results_dir: str, models_dir: str, requested_models: list[str] | None) -> list[dict]:
    selected = []
    target_models = requested_models or list(CANONICAL_MODELS)

    for model_name in target_models:
        model_root = os.path.join(models_dir, model_name)
        results_root = os.path.join(results_dir, "runs", model_name)
        if not os.path.isdir(model_root) or not os.path.isdir(results_root):
            continue

        best_run = None
        for seed_name in sorted(os.listdir(model_root)):
            checkpoint_path = os.path.join(model_root, seed_name, "best.pth")
            metrics_path = os.path.join(results_root, seed_name, "metrics.json")
            if not os.path.exists(checkpoint_path) or not os.path.exists(metrics_path):
                continue
            metrics = _load_json(metrics_path)
            run_log_path = os.path.join(
                results_root,
                seed_name,
                f"phase2_{model_name}_seed{int(metrics['seed'])}.json",
            )
            if not os.path.exists(run_log_path):
                print(f"Warning: run log missing for {model_name} seed {metrics['seed']}; skipping checkpoint validation.")
                continue

            run_log = _load_json(run_log_path)
            expected_hash = (
                run_log.get("artifacts", {})
                .get("model_checkpoint_file", {})
                .get("sha256")
            )
            observed_hash = sha256_file(checkpoint_path)
            if expected_hash and observed_hash != expected_hash:
                print(
                    f"Warning: local checkpoint hash mismatch for {model_name} seed {metrics['seed']} "
                    f"(expected {expected_hash[:12]}..., observed {observed_hash[:12]}...). "
                    "Skipping stale local checkpoint."
                )
                continue

            candidate = {
                "model": model_name,
                "seed": int(metrics["seed"]),
                "checkpoint_path": checkpoint_path,
                "metrics_path": metrics_path,
                "run_log_path": run_log_path,
                "metrics": metrics,
            }
            if best_run is None or candidate["metrics"]["test_accuracy"] > best_run["metrics"]["test_accuracy"]:
                best_run = candidate

        if best_run is not None:
            selected.append(best_run)

    return selected


def _build_test_loader(test_csv: str, batch_size: int, num_workers: int, limit_samples: int):
    df = pd.read_csv(test_csv).dropna(subset=["class_label"]).reset_index(drop=True)
    dataset = PlantDiseaseDataset(test_csv, label_column="class_label", transform=get_val_transform())

    if limit_samples > 0:
        limit = min(limit_samples, len(df))
        df = df.iloc[:limit].reset_index(drop=True)
        dataset = Subset(dataset, list(range(limit)))

    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    return df, loader


def _run_inference(model, loader, device) -> tuple[list[int], list[int], list[float]]:
    model.eval()
    all_preds = []
    all_true = []
    all_conf = []

    with torch.no_grad():
        for inputs, labels in loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            probs = torch.softmax(outputs, dim=1)
            confs, preds = torch.max(probs, dim=1)

            all_preds.extend(preds.cpu().tolist())
            all_true.extend(labels.cpu().tolist())
            all_conf.extend(confs.cpu().tolist())

    return all_true, all_preds, all_conf


def _save_gallery(mistakes_df: pd.DataFrame, out_path: str, top_k: int) -> None:
    top = mistakes_df.head(top_k)
    if top.empty:
        return

    n_cols = 4
    n_rows = int(np.ceil(len(top) / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4.5 * n_rows))
    axes = np.atleast_1d(axes).flatten()

    for ax, (_, row) in zip(axes, top.iterrows()):
        image = plt.imread(row["resolved_image_path"])
        ax.imshow(image)
        title = "\n".join(
            [
                textwrap.shorten(row["true_label_name"], width=32, placeholder="..."),
                "pred: " + textwrap.shorten(row["pred_label_name"], width=28, placeholder="..."),
                f"conf: {row['pred_confidence']:.3f}",
            ]
        )
        ax.set_title(title, fontsize=9)
        ax.axis("off")

    for ax in axes[len(top):]:
        ax.axis("off")

    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Generate Phase 2 misclassification galleries.")
    parser.add_argument("--results-dir", default=os.path.join(PROJECT_ROOT, "results", "phase2"))
    parser.add_argument("--models-dir", default=os.path.join(PROJECT_ROOT, "models", "phase2"))
    parser.add_argument("--out-dir", default=os.path.join(PROJECT_ROOT, "results", "phase2", "analysis", "misclassifications"))
    parser.add_argument("--models", default="all", help="Comma-separated model names or 'all'.")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--limit-samples", type=int, default=0, help="Optional smoke limit for fast verification.")
    parser.add_argument("--top-k", type=int, default=16, help="Number of top-confidence mistakes to visualize per model.")
    args = parser.parse_args()

    requested_models = None
    if args.models.strip().lower() != "all":
        requested_models = [name.strip() for name in args.models.split(",") if name.strip()]

    device = get_device()
    _ensure_dir(args.out_dir)

    selected_runs = _discover_best_available_runs(
        results_dir=args.results_dir,
        models_dir=args.models_dir,
        requested_models=requested_models,
    )
    if not selected_runs:
        raise FileNotFoundError(
            "No local Phase 2 checkpoints with matching run-log hashes were found. "
            "Import the corresponding model weights from Colab or rerun error analysis where the checkpoints live."
        )

    selection_payload = []
    for run in selected_runs:
        metrics = run["metrics"]
        test_csv = resolve_project_path(metrics["source_split_paths"]["test"], project_root=PROJECT_ROOT)
        df_test, loader = _build_test_loader(
            test_csv=test_csv,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            limit_samples=args.limit_samples,
        )

        # For checkpoint analysis we only need the architecture skeleton.
        # Loading pretrained backbone weights here can trigger unnecessary downloads.
        model = build_model(run["model"], num_classes=NUM_CLASSES, pretrained=False)
        model = load_model(model, run["checkpoint_path"], device=device)
        true_labels, pred_labels, pred_conf = _run_inference(model, loader, device)

        mistakes = []
        for idx, (true_label, pred_label, confidence) in enumerate(zip(true_labels, pred_labels, pred_conf)):
            if true_label == pred_label:
                continue
            row = df_test.iloc[idx]
            resolved_path = _resolve_image_path(str(row["image_path"]))
            mistakes.append(
                {
                    "row_index": int(idx),
                    "image_path": str(row["image_path"]),
                    "resolved_image_path": resolved_path,
                    "true_label": int(true_label),
                    "pred_label": int(pred_label),
                    "true_label_name": CLASS_NAMES[int(true_label)],
                    "pred_label_name": CLASS_NAMES[int(pred_label)],
                    "pred_confidence": float(confidence),
                }
            )

        if mistakes:
            mistakes_df = pd.DataFrame(mistakes).sort_values("pred_confidence", ascending=False)
        else:
            mistakes_df = pd.DataFrame(
                columns=[
                    "row_index",
                    "image_path",
                    "resolved_image_path",
                    "true_label",
                    "pred_label",
                    "true_label_name",
                    "pred_label_name",
                    "pred_confidence",
                ]
            )
        model_out_dir = os.path.join(args.out_dir, run["model"])
        _ensure_dir(model_out_dir)

        mistakes_csv = os.path.join(model_out_dir, "misclassified_examples.csv")
        mistakes_json = os.path.join(model_out_dir, "misclassified_examples.json")
        gallery_png = os.path.join(model_out_dir, "top_misclassifications.png")
        mistakes_df.to_csv(mistakes_csv, index=False)
        with open(mistakes_json, "w", encoding="utf-8") as handle:
            json.dump(mistakes, handle, indent=2)
        _save_gallery(mistakes_df, gallery_png, top_k=args.top_k)

        selection_payload.append(
            {
                "model": run["model"],
                "selected_seed": run["seed"],
                "checkpoint_path": run["checkpoint_path"],
                "metrics_path": run["metrics_path"],
                "mistake_count": int(len(mistakes_df)),
                "gallery_path": gallery_png,
            }
        )
        print(f"Saved misclassification artifacts for {run['model']} to {model_out_dir}")

    selection_path = os.path.join(args.out_dir, "selected_checkpoints.json")
    with open(selection_path, "w", encoding="utf-8") as handle:
        json.dump(selection_payload, handle, indent=2)
    print("Saved checkpoint selection summary:", selection_path)


if __name__ == "__main__":
    main()
