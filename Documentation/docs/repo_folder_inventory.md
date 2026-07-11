# Repository Folder Inventory

Last updated: 2026-03-14

This is a quick reference for what each top-level folder is used for and whether it is ignored by `.gitignore`.

| Folder | What it is | Gitignore status |
|---|---|---|
| `CSV` | Label and split CSV artifacts used by the pipeline. | `Partially ignored` (folder itself is not ignored, but `CSV/*` is ignored except canonical split files explicitly unignored). |
| `Datasets` | Raw image dataset folders (PlantVillage class directories). | `Ignored` (`.gitignore:4`). |
| `experiments` | Ad-hoc/scratch experiment area (currently empty). | `Not ignored`. |
| `FYP` | External context material: past reports, metadata slides, and local analysis notes (including extracted text under `FYP/past_reports_text_extracts`). | `Ignored` (`.gitignore:89`). |
| `Google Colab` | Colab orchestration notebooks (`phase1` live smoke, `phase2` benchmark, legacy helper notebook). | `Not ignored`. |
| `code archives` | Ignored archive for legacy one-off utilities and downloaded context notebooks from Colab runs. | `Ignored` (`.gitignore:10`). |
| `Markdown Files` | Local planning/checklist/docs/review markdown tree. | `Ignored` (`.gitignore:88`). |
| `models` | Model checkpoints and weights. | `Partially ignored` (top-level folder not ignored; root `models/*.pth|*.pt|*.ckpt` ignored; nested directories may still be tracked unless separately ignored). |
| `notebooks` | Legacy notebook workflow (`01`-`06`), including older severity exploration notebooks. | `Not ignored` (kept visible for traceability). |
| `results` | Generated run artifacts, manifests, reports, and summaries. | `Partially ignored` (folder not ignored; many timestamped/raw artifacts ignored, selected canonical `latest_*` + summary outputs tracked by allowlist rules). |
| `src` | Canonical source code used by scripts and benchmarks. | `Not ignored`. |
| `tests` | Minimal test suite (schema/leakage/integrity checks). | `Not ignored`. |

## Notes on recent cleanup

- Moved `_tmp_fyp_text` to `FYP/past_reports_text_extracts` to keep FYP review context in one place.
- Removed legacy `Main/` folder (it only contained an empty `Google Colab` subfolder).
- Renamed `helper scripts` to `code archives` so legacy/context material is clearly separated from canonical pipeline code.
- Left `notebooks/` visible (not ignored) so historical notebook context remains available when needed.
