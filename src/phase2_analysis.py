"""
Phase 2 artifact-driven analysis and plot generation.

This script reads completed benchmark artifacts under results/phase2/ and
produces dissertation-ready comparison figures without rerunning training.
"""

import argparse
import json
import os
from collections import Counter, defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

try:
    from src.model_registry import CANONICAL_MODELS
    from src.utils import PROJECT_ROOT
except ImportError:
    from .model_registry import CANONICAL_MODELS
    from .utils import PROJECT_ROOT


PLOT_STYLE = "whitegrid"


def _load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _build_run_df(results_dir: str) -> pd.DataFrame:
    rows = []
    runs_root = os.path.join(results_dir, "runs")
    for model_name in CANONICAL_MODELS:
        model_dir = os.path.join(runs_root, model_name)
        if not os.path.isdir(model_dir):
            continue
        for seed_name in sorted(os.listdir(model_dir)):
            metrics_path = os.path.join(model_dir, seed_name, "metrics.json")
            if not os.path.exists(metrics_path):
                continue
            metrics = _load_json(metrics_path)
            history = metrics.get("history", {})
            rows.append(
                {
                    "model": metrics["model"],
                    "seed": int(metrics["seed"]),
                    "test_accuracy": float(metrics["test_accuracy"]),
                    "test_f1_macro": float(metrics["test_f1_macro"]),
                    "elapsed_seconds": float(metrics["elapsed_seconds"]),
                    "trainable_params": int(metrics["trainable_params"]),
                    "model_size_bytes": int(metrics["model_size_bytes"]),
                    "epochs_ran": int(len(history.get("train_loss", []))),
                    "metrics_path": metrics_path,
                    "classification_report": metrics.get("classification_report", {}),
                    "history": history,
                }
            )

    if not rows:
        raise FileNotFoundError(f"No phase2 metrics.json files found under: {runs_root}")

    df = pd.DataFrame(rows)
    return df.sort_values(["model", "seed"]).reset_index(drop=True)


def _build_summary_df(run_df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        run_df.groupby("model")
        .agg(
            accuracy_mean=("test_accuracy", "mean"),
            accuracy_std=("test_accuracy", "std"),
            f1_macro_mean=("test_f1_macro", "mean"),
            f1_macro_std=("test_f1_macro", "std"),
            elapsed_mean_sec=("elapsed_seconds", "mean"),
            elapsed_std_sec=("elapsed_seconds", "std"),
            params=("trainable_params", "max"),
            model_size_bytes=("model_size_bytes", "max"),
            runs=("seed", "count"),
            epochs_mean=("epochs_ran", "mean"),
        )
        .reset_index()
    )

    for col in ("accuracy_std", "f1_macro_std", "elapsed_std_sec"):
        summary[col] = summary[col].fillna(0.0)

    summary["model_size_mb"] = summary["model_size_bytes"] / (1024 * 1024)
    summary["params_millions"] = summary["params"] / 1_000_000.0
    return summary


def _model_order(summary_df: pd.DataFrame) -> list[str]:
    ranked = summary_df.sort_values(
        ["f1_macro_mean", "accuracy_mean"], ascending=[False, False]
    )["model"].tolist()
    return ranked


def _save_figure(fig, path: str) -> None:
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def _plot_metric_summary(summary_df: pd.DataFrame, plots_dir: str) -> str:
    ranked = _model_order(summary_df)
    df = summary_df.set_index("model").loc[ranked].reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    metrics = [
        ("accuracy_mean", "accuracy_std", "Test Accuracy", axes[0]),
        ("f1_macro_mean", "f1_macro_std", "Test Macro F1", axes[1]),
    ]

    for mean_col, std_col, title, ax in metrics:
        ax.bar(df["model"], df[mean_col], yerr=df[std_col], capsize=5, color="#4C72B0")
        ax.set_title(title)
        ax.set_xlabel("Model")
        ax.set_ylabel(title)
        ax.tick_params(axis="x", rotation=20)
        ax.set_ylim(bottom=max(0.0, df[mean_col].min() - 0.01), top=min(1.01, df[mean_col].max() + 0.002))

    path = os.path.join(plots_dir, "metric_summary.png")
    _save_figure(fig, path)
    return path


def _plot_seed_variance(run_df: pd.DataFrame, plots_dir: str) -> str:
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for ax, metric, title in (
        (axes[0], "test_accuracy", "Seed Variance: Test Accuracy"),
        (axes[1], "test_f1_macro", "Seed Variance: Test Macro F1"),
    ):
        sns.stripplot(
            data=run_df,
            x="model",
            y=metric,
            hue="seed",
            dodge=True,
            size=7,
            ax=ax,
        )
        ax.set_title(title)
        ax.set_xlabel("Model")
        ax.set_ylabel(metric.replace("_", " ").title())
        ax.tick_params(axis="x", rotation=20)
        ax.legend(title="Seed", loc="best")

    path = os.path.join(plots_dir, "seed_variance.png")
    _save_figure(fig, path)
    return path


def _plot_efficiency_tradeoff(summary_df: pd.DataFrame, plots_dir: str) -> str:
    fig, ax = plt.subplots(figsize=(8, 6))
    df = summary_df.copy()
    point_sizes = 80 + (df["elapsed_mean_sec"] / df["elapsed_mean_sec"].max()) * 320
    scatter = ax.scatter(
        df["model_size_mb"],
        df["f1_macro_mean"],
        s=point_sizes,
        c=df["params_millions"],
        cmap="viridis",
        alpha=0.85,
        edgecolors="black",
    )

    for _, row in df.iterrows():
        ax.annotate(row["model"], (row["model_size_mb"], row["f1_macro_mean"]), xytext=(6, 4), textcoords="offset points")

    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Trainable params (millions)")
    ax.set_title("Efficiency Trade-off: Model Size vs Macro F1")
    ax.set_xlabel("Checkpoint size (MB)")
    ax.set_ylabel("Macro F1 mean")

    path = os.path.join(plots_dir, "efficiency_tradeoff.png")
    _save_figure(fig, path)
    return path


def _plot_history_grid(run_df: pd.DataFrame, plots_dir: str, value_key: str, out_name: str, ylabel: str) -> str:
    colors = {41: "#4C72B0", 42: "#55A868", 43: "#C44E52"}
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=False)
    axes = axes.flatten()

    for ax, model_name in zip(axes, CANONICAL_MODELS):
        subset = run_df[run_df["model"] == model_name].sort_values("seed")
        for _, row in subset.iterrows():
            history = row["history"]
            seed = int(row["seed"])
            train_values = history.get(f"train_{value_key}", [])
            val_values = history.get(f"val_{value_key}", [])
            if train_values:
                ax.plot(
                    range(1, len(train_values) + 1),
                    train_values,
                    linestyle="--",
                    linewidth=1.8,
                    color=colors.get(seed, "#999999"),
                    label=f"seed {seed} train",
                )
            if val_values:
                ax.plot(
                    range(1, len(val_values) + 1),
                    val_values,
                    linestyle="-",
                    linewidth=2.0,
                    color=colors.get(seed, "#999999"),
                    label=f"seed {seed} val",
                )
        ax.set_title(model_name)
        ax.set_xlabel("Epoch")
        ax.set_ylabel(ylabel)
        ax.legend(fontsize=8)

    path = os.path.join(plots_dir, out_name)
    _save_figure(fig, path)
    return path


def _load_confusion_payloads(results_dir: str) -> list[dict]:
    payloads = []
    runs_root = os.path.join(results_dir, "runs")
    for model_name in CANONICAL_MODELS:
        model_dir = os.path.join(runs_root, model_name)
        if not os.path.isdir(model_dir):
            continue
        for seed_name in sorted(os.listdir(model_dir)):
            confusion_path = os.path.join(model_dir, seed_name, "confusion_matrix.json")
            if not os.path.exists(confusion_path):
                continue
            payload = _load_json(confusion_path)
            payloads.append(payload)
    return payloads


def _plot_top_confusions(confusion_payloads: list[dict], plots_dir: str, top_k: int = 10) -> tuple[str, list[dict]]:
    pair_counter = Counter()
    for payload in confusion_payloads:
        class_names = payload["class_names"]
        matrix = payload["matrix"]
        for i, row in enumerate(matrix):
            for j, count in enumerate(row):
                if i != j and count:
                    pair_counter[(class_names[i], class_names[j])] += int(count)

    top_pairs = pair_counter.most_common(top_k)
    labels = [f"{src}\n-> {dst}" for (src, dst), _ in top_pairs]
    values = [count for _, count in top_pairs]

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.barh(range(len(labels)), values, color="#8172B3")
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Total off-diagonal count across all runs")
    ax.set_title("Most Frequent Confusion Pairs")

    path = os.path.join(plots_dir, "top_confusions.png")
    _save_figure(fig, path)

    structured = [
        {"true_class": src, "predicted_class": dst, "count": int(count)}
        for (src, dst), count in top_pairs
    ]
    return path, structured


def _plot_mean_confusion_heatmaps(confusion_payloads: list[dict], plots_dir: str) -> str:
    grouped = defaultdict(list)
    class_names = None
    for payload in confusion_payloads:
        matrix = np.array(payload["matrix"], dtype=float)
        row_sums = matrix.sum(axis=1, keepdims=True)
        normalized = np.divide(matrix, row_sums, out=np.zeros_like(matrix), where=row_sums != 0)
        grouped[payload["model"]].append(normalized)
        class_names = payload["class_names"]

    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    axes = axes.flatten()
    for ax, model_name in zip(axes, CANONICAL_MODELS):
        model_mats = grouped.get(model_name, [])
        if not model_mats:
            ax.axis("off")
            continue
        mean_mat = np.mean(np.stack(model_mats, axis=0), axis=0)
        sns.heatmap(
            mean_mat,
            ax=ax,
            cmap="Blues",
            cbar=False,
            xticklabels=class_names,
            yticklabels=class_names,
        )
        ax.set_title(model_name)
        ax.tick_params(axis="x", rotation=90, labelsize=7)
        ax.tick_params(axis="y", rotation=0, labelsize=7)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("True")

    path = os.path.join(plots_dir, "mean_confusion_heatmaps.png")
    _save_figure(fig, path)
    return path


def _build_analysis_summary(run_df: pd.DataFrame, summary_df: pd.DataFrame, top_pairs: list[dict], plot_paths: dict) -> dict:
    ranked = summary_df.sort_values(
        ["f1_macro_mean", "accuracy_mean"], ascending=[False, False]
    ).reset_index(drop=True)

    hardest_by_model = {}
    for model_name in CANONICAL_MODELS:
        subset = run_df[run_df["model"] == model_name]
        hardest = []
        for _, row in subset.iterrows():
            report = row["classification_report"]
            for class_name, metrics in report.items():
                if class_name in ("accuracy", "macro avg", "weighted avg"):
                    continue
                hardest.append(
                    {
                        "class_name": class_name,
                        "seed": int(row["seed"]),
                        "f1_score": float(metrics["f1-score"]),
                    }
                )
        hardest.sort(key=lambda item: item["f1_score"])
        hardest_by_model[model_name] = hardest[:5]

    return {
        "coverage": {
            "models": sorted(run_df["model"].unique().tolist()),
            "seeds": sorted(int(seed) for seed in run_df["seed"].unique().tolist()),
            "run_count": int(len(run_df)),
        },
        "leaderboard": ranked.to_dict(orient="records"),
        "top_confusion_pairs": top_pairs,
        "hardest_classes_by_model": hardest_by_model,
        "plots": plot_paths,
    }


def main():
    parser = argparse.ArgumentParser(description="Generate Phase 2 comparison plots and analysis summaries.")
    parser.add_argument("--results-dir", default=os.path.join(PROJECT_ROOT, "results", "phase2"))
    parser.add_argument("--out-dir", default=os.path.join(PROJECT_ROOT, "results", "phase2", "analysis"))
    args = parser.parse_args()

    sns.set_theme(style=PLOT_STYLE)
    out_dir = args.out_dir
    plots_dir = os.path.join(out_dir, "plots")
    _ensure_dir(plots_dir)

    run_df = _build_run_df(args.results_dir)
    summary_df = _build_summary_df(run_df)
    confusion_payloads = _load_confusion_payloads(args.results_dir)

    plot_paths = {
        "metric_summary": _plot_metric_summary(summary_df, plots_dir),
        "seed_variance": _plot_seed_variance(run_df, plots_dir),
        "efficiency_tradeoff": _plot_efficiency_tradeoff(summary_df, plots_dir),
        "loss_curves": _plot_history_grid(run_df, plots_dir, value_key="loss", out_name="loss_curves.png", ylabel="Loss"),
        "accuracy_curves": _plot_history_grid(run_df, plots_dir, value_key="acc", out_name="accuracy_curves.png", ylabel="Accuracy"),
        "mean_confusion_heatmaps": _plot_mean_confusion_heatmaps(confusion_payloads, plots_dir),
    }
    top_confusions_path, top_pairs = _plot_top_confusions(confusion_payloads, plots_dir)
    plot_paths["top_confusions"] = top_confusions_path

    summary_payload = _build_analysis_summary(run_df, summary_df, top_pairs, plot_paths)
    summary_json_path = os.path.join(out_dir, "analysis_summary.json")
    with open(summary_json_path, "w", encoding="utf-8") as handle:
        json.dump(summary_payload, handle, indent=2)

    print("Saved analysis summary:", summary_json_path)
    for name, path in plot_paths.items():
        print(f"Saved plot ({name}): {path}")


if __name__ == "__main__":
    main()
