# Phase 3 Notes

## Research scope

Research Phase 3 remains responsible for XAI, region-alignment analysis, and
further model investigation. The commercial Verdanta Mobile App has a separate
product phase also called Phase 3; that product phase covers governed model
release and safe inference. The two phase numbers must not be treated as the
same milestone.

## Product handoff completed on 2026-07-17

The exact historical EfficientNet-B0 seed-41 checkpoint was unavailable. Rather
than changing historical benchmark identity, one distinct seed-44 replacement
candidate was trained from research commit
`3dd00f7a92fed4537d53a24f0764ade26e3d5946` using the frozen 15-class
PlantVillage splits.

Verified candidate facts:

- architecture: EfficientNet-B0;
- seed: `44`;
- 30-epoch maximum with early stopping after 22 epochs;
- best validation accuracy: `0.998062`;
- controlled test accuracy: `0.997093`;
- controlled macro F1: `0.997616`;
- checkpoint SHA-256:
  `667f0d6c9c4031d9290c671913f45dc822efb6050637a9802a064965a495785a`;
- strict local state-dict reload and finite `(1, 15)` output passed.

The clean canonical notebook is
`Google Colab/mvp_efficientnet_release_candidate.ipynb`. The executed notebook
and original candidate ZIP are retained as private source evidence outside Git.
The clean notebook restores the dataset-integrity cell that was accidentally
absent from the executed copy and removes a corrected duplicate configuration
cell. Successful train/validation/test decoding and prior integrity evidence
meant this notebook cleanup did not require another retraining run.

## Repository boundary

`src/export_model_release.py` is the supported handoff tool. It constructs a
governed bundle only after validating candidate provenance, metrics identity,
the independently reviewed candidate ZIP hash, checkpoint size/hash,
architecture, class order, and strict safe loading. The product repository owns
serving, startup parity, conservative result policy, API behaviour, operational
limits, and mobile integration. It must not import this research runtime directly.

Model weights, raw Colab evidence, and assembled releases remain in private
artifact storage outside both repositories. Seed 44 must never be merged into
the original 12-run aggregate or presented as field evidence.
