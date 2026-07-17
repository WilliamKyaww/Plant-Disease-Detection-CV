"""Assemble a governed product release from a verified training candidate."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

import timm
import torch
import torchvision
from PIL import Image

try:
    from src.model_registry import build_model
    from src.transforms import get_val_transform
    from src.utils import CLASS_NAMES
except ImportError:
    from .model_registry import build_model
    from .transforms import get_val_transform
    from .utils import CLASS_NAMES


EXPECTED_ARCHITECTURE = "efficientnet_b0"
EXPECTED_SEED = 44
EXPECTED_CLASSES = 15
EXPECTED_SOURCE_COMMIT = "3dd00f7a92fed4537d53a24f0764ade26e3d5946"
EXPECTED_CANDIDATE_ID = "efficientnet_b0_seed44_replacement_20260717T205245Z"
EXPECTED_CANDIDATE_ARCHIVE_SHA256 = (
    "f03e51a55c0f43fef3eb74a149fb555a892ce936df8512b5f874348171a97d62"
)
EXPECTED_CHECKPOINT_SHA256 = "667f0d6c9c4031d9290c671913f45dc822efb6050637a9802a064965a495785a"
EXPECTED_CHECKPOINT_SIZE_BYTES = 16_382_373
DEFAULT_RELEASE_ID = "efficientnet-b0-pv15-seed44-v1"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _safe_archive_names(archive: ZipFile) -> list[str]:
    names = archive.namelist()
    for name in names:
        path = PurePosixPath(name.replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"Candidate archive contains an unsafe path: {name}")
    return names


def _single_name(names: list[str], suffix: str) -> str:
    matches = [name for name in names if name.endswith(suffix)]
    if len(matches) != 1:
        raise ValueError(f"Expected one archive entry ending {suffix!r}, found {matches}")
    return matches[0]


def _read_candidate(archive_path: Path) -> tuple[dict, dict, bytes, str]:
    if sha256_file(archive_path) != EXPECTED_CANDIDATE_ARCHIVE_SHA256:
        raise ValueError("Candidate archive SHA-256 does not match the reviewed export")
    with ZipFile(archive_path) as archive:
        names = _safe_archive_names(archive)
        manifest_name = _single_name(names, "/candidate_manifest.json")
        metrics_name = _single_name(names, "/runs/efficientnet_b0/seed_44/metrics.json")
        checkpoint_name = _single_name(names, "/model/best.pth")
        candidate = json.loads(archive.read(manifest_name))
        metrics = json.loads(archive.read(metrics_name))
        checkpoint = archive.read(checkpoint_name)

    expected = candidate["checkpoint"]
    if candidate.get("model") != EXPECTED_ARCHITECTURE:
        raise ValueError("Candidate architecture is not the approved EfficientNet-B0")
    if candidate.get("seed") != EXPECTED_SEED:
        raise ValueError("Candidate seed is not the approved replacement seed")
    if candidate.get("num_classes") != EXPECTED_CLASSES:
        raise ValueError("Candidate output count is not the canonical 15 classes")
    if candidate.get("source_commit") != EXPECTED_SOURCE_COMMIT:
        raise ValueError("Candidate source commit does not match the reviewed training source")
    if candidate.get("candidate_id") != EXPECTED_CANDIDATE_ID:
        raise ValueError("Candidate identifier does not match the reviewed export")
    if expected.get("size_bytes") != EXPECTED_CHECKPOINT_SIZE_BYTES:
        raise ValueError("Candidate manifest checkpoint size is not approved")
    if expected.get("sha256") != EXPECTED_CHECKPOINT_SHA256:
        raise ValueError("Candidate manifest checkpoint SHA-256 is not approved")
    if len(checkpoint) != EXPECTED_CHECKPOINT_SIZE_BYTES:
        raise ValueError("Checkpoint size does not match the candidate manifest")
    if sha256_bytes(checkpoint) != EXPECTED_CHECKPOINT_SHA256:
        raise ValueError("Checkpoint SHA-256 does not match the candidate manifest")
    if metrics.get("model") != EXPECTED_ARCHITECTURE or metrics.get("seed") != EXPECTED_SEED:
        raise ValueError("Candidate metrics identity does not match the checkpoint")
    return candidate, metrics, checkpoint, manifest_name


def _load_model(checkpoint: bytes):
    state_dict = torch.load(io.BytesIO(checkpoint), map_location="cpu", weights_only=True)
    if not isinstance(state_dict, dict) or not all(isinstance(key, str) for key in state_dict):
        raise ValueError("Checkpoint is not a string-keyed state dictionary")
    model = build_model(EXPECTED_ARCHITECTURE, num_classes=EXPECTED_CLASSES, pretrained=False)
    model.load_state_dict(state_dict, strict=True)
    model.eval()
    return model


def _write_reference_fixtures(fixtures_dir: Path) -> list[tuple[str, Path]]:
    fixtures_dir.mkdir(parents=True)

    gradient = Image.new("RGB", (257, 193))
    pixels = gradient.load()
    for y in range(gradient.height):
        for x in range(gradient.width):
            pixels[x, y] = (
                12 + (x * 73 // (gradient.width - 1)),
                48 + (y * 142 // (gradient.height - 1)),
                18 + ((x + y) * 67 // (gradient.width + gradient.height - 2)),
            )
    gradient_path = fixtures_dir / "synthetic-green-gradient.png"
    gradient.save(gradient_path, format="PNG", optimize=False, compress_level=9)
    gradient.close()

    checker = Image.new("RGB", (224, 224))
    checker_pixels = checker.load()
    colours = ((36, 78, 42), (184, 173, 118))
    for y in range(checker.height):
        for x in range(checker.width):
            checker_pixels[x, y] = colours[((x // 16) + (y // 16)) % 2]
    checker_path = fixtures_dir / "synthetic-checkerboard.png"
    checker.save(checker_path, format="PNG", optimize=False, compress_level=9)
    checker.close()

    (fixtures_dir / "README.md").write_text(
        "# Reference Fixtures\n\n"
        "These deterministic synthetic PNG files contain no participant, field, or "
        "PlantVillage imagery. They verify numeric preprocessing/model parity only and "
        "provide no semantic or field-validity evidence.\n",
        encoding="utf-8",
    )
    return [
        ("synthetic-green-gradient", gradient_path),
        ("synthetic-checkerboard", checker_path),
    ]


def _reference_outputs(model, fixtures: list[tuple[str, Path]], release_id: str) -> dict:
    transform = get_val_transform()
    records = []
    torch.set_num_threads(1)
    for fixture_id, path in fixtures:
        with Image.open(path) as image:
            tensor = transform(image.convert("RGB")).unsqueeze(0)
        with torch.inference_mode():
            logits = model(tensor)[0].detach().cpu().tolist()
        if len(logits) != EXPECTED_CLASSES or not all(float("-inf") < value < float("inf") for value in logits):
            raise ValueError(f"Fixture {fixture_id} produced an invalid model output")
        records.append(
            {
                "fixture_id": fixture_id,
                "relative_path": f"reference-fixtures/{path.name}",
                "image_sha256": sha256_file(path),
                "expected_logits": [float(value) for value in logits],
                "expected_top_class_index": max(range(len(logits)), key=logits.__getitem__),
            }
        )
    return {
        "schema_version": 1,
        "release_id": release_id,
        "absolute_tolerance": 1e-5,
        "relative_tolerance": 1e-4,
        "fixtures": records,
    }


def _model_card(candidate: dict, metrics: dict, release_id: str) -> str:
    errors = int(metrics["test_samples"] * (1 - metrics["test_accuracy"]) + 0.5)
    return f"""# Model Card: {release_id}

## Intended Use

Internal, invitation-only evaluation of a conservative potato field-image workflow. The
model is a PlantVillage baseline and the current product policy returns `uncertain` for
every otherwise-analysable image. It is not approved for autonomous decisions.

## Prohibited Use

- Disease diagnosis or exclusion of disease.
- Treatment, pesticide, dosage, or crop-protection recommendations.
- Public field-accuracy claims derived from the PlantVillage benchmark.
- General crop recognition, safety-critical automation, or unattended intervention.
- Training on participant images without separately governed consent and provenance.

## Training Domain

Controlled PlantVillage imagery across 15 pepper, potato, and tomato classes. The
replacement candidate used frozen CSV splits (14,446 train; 3,096 validation; 3,096 test),
seed {candidate['seed']}, inverse-frequency class weighting, ImageNet initialisation, and
early stopping under a 30-epoch maximum. It contains no field-domain training data.

## Data and Weights Provenance

- Research repository: `WilliamKyaww/Plant-Disease-Detection-CV`.
- Training source commit: `{candidate['source_commit']}`.
- Candidate identifier: `{candidate['candidate_id']}`.
- Checkpoint SHA-256: `{candidate['checkpoint']['sha256']}`.
- Architecture: timm EfficientNet-B0 with a 15-output classifier head.
- Initial weights: timm-provided ImageNet pretrained weights requested by the recorded run.
- Reference fixtures in this bundle are deterministic synthetic images, not dataset samples.

## Licensing Review

PlantVillage data provenance and the pretrained-weight redistribution terms require final
human/legal review before external model distribution. This bundle is approved only for
private local engineering and evaluation; it must not be published or committed to Git.

## Evaluation

On the frozen controlled test split the candidate achieved accuracy
`{metrics['test_accuracy']:.6f}` and macro F1 `{metrics['test_f1_macro']:.6f}`
({metrics['test_samples'] - errors}/{metrics['test_samples']} correct). Training completed
{len(metrics['history']['val_acc'])} epochs and selected a best validation accuracy of
`{max(metrics['history']['val_acc']):.6f}`. These are laboratory-style benchmark results,
not field performance estimates.

## Limitations

The model is closed-set, uncalibrated for field use, and lacks a validated semantic image-
quality or out-of-distribution detector. PlantVillage backgrounds, lighting, symptom
presentation, cultivars, devices, and class balance do not represent normal field use.
Pests, deficiencies, senescence, damage, unknown diseases, mixed symptoms, and non-leaf
content can still receive confident logits. The current policy therefore abstains.

## Rollback

Set `VERDANTA_INFERENCE_BACKEND=synthetic` or point
`VERDANTA_MODEL_RELEASE_DIR` to a previously reviewed immutable bundle, restart the API,
and verify `/v1/health/ready` before further testing. Never overwrite this release in place;
every replacement receives a new release identifier and checksum.
"""


def export_release(candidate_archive: Path, output_dir: Path, release_id: str) -> Path:
    candidate_archive = candidate_archive.resolve()
    output_dir = output_dir.resolve()
    if not candidate_archive.is_file():
        raise FileNotFoundError(candidate_archive)
    if output_dir.exists():
        raise FileExistsError(f"Immutable release directory already exists: {output_dir}")

    candidate, metrics, checkpoint, _ = _read_candidate(candidate_archive)
    model = _load_model(checkpoint)

    staging = output_dir.with_name(f".{output_dir.name}.staging")
    if staging.exists():
        raise FileExistsError(f"Inspect or remove the existing staging directory: {staging}")
    try:
        staging.mkdir(parents=True)
        checkpoint_path = staging / "checkpoint.pth"
        checkpoint_path.write_bytes(checkpoint)
        fixtures = _write_reference_fixtures(staging / "reference-fixtures")
        outputs = _reference_outputs(model, fixtures, release_id)
        (staging / "reference-outputs.json").write_text(
            json.dumps(outputs, indent=2) + "\n",
            encoding="utf-8",
        )
        (staging / "model-card.md").write_text(
            _model_card(candidate, metrics, release_id),
            encoding="utf-8",
        )

        manifest = {
            "schema_version": 1,
            "release_id": release_id,
            "source_repository": "WilliamKyaww/Plant-Disease-Detection-CV",
            "source_commit": candidate["source_commit"],
            "architecture": EXPECTED_ARCHITECTURE,
            "num_classes": EXPECTED_CLASSES,
            "artifact_filename": "checkpoint.pth",
            "artifact_sha256": sha256_bytes(checkpoint),
            "artifact_size_bytes": len(checkpoint),
            "checkpoint_format": "pytorch_state_dict",
            "weights_only_required": True,
            "framework": {
                "python": "3.12.13",
                "torch": "2.9.1",
                "torchvision": "0.24.1",
                "timm": "1.0.25",
            },
            "preprocessing": {
                "version": "pv15-resize224-imagenet-v1",
                "image_size": [224, 224],
                "resize_mode": "stretch",
                "interpolation": "bilinear",
                "antialias": True,
                "colour_mode": "RGB",
                "mean": [0.485, 0.456, 0.406],
                "std": [0.229, 0.224, 0.225],
            },
            "class_names": CLASS_NAMES,
            "label_map_version": "plantvillage-15-v1",
            "result_policy_version": "potato-pilot-interim-v1",
            "training_domain": "PlantVillage controlled imagery; no field-domain training data",
            "intended_use": "Private experimental potato field-pilot baseline evaluation",
            "prohibited_use": [
                "Validated disease diagnosis",
                "Treatment or crop-protection recommendation",
                "Public field-accuracy claim",
            ],
            "model_card_filename": "model-card.md",
            "reference_outputs_filename": "reference-outputs.json",
        }
        (staging / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )

        provenance = staging / "provenance"
        provenance.mkdir()
        (provenance / "candidate-manifest.json").write_text(
            json.dumps(candidate, indent=2) + "\n",
            encoding="utf-8",
        )
        (provenance / "assembly.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "assembled_at_utc": datetime.now(timezone.utc).isoformat(),
                    "candidate_archive_sha256": sha256_file(candidate_archive),
                    "assembler_script_sha256": sha256_file(Path(__file__).resolve()),
                    "export_runtime": {
                        "python": sys.version.split()[0],
                        "torch": torch.__version__,
                        "torchvision": torchvision.__version__,
                        "timm": timm.__version__,
                    },
                    "reference_fixture_purpose": "numeric parity only",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        staging.rename(output_dir)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return output_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate_archive", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--release-id", default=DEFAULT_RELEASE_ID)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = export_release(args.candidate_archive, args.output_dir, args.release_id)
    print(f"Release bundle created: {output}")
    print(f"Checkpoint SHA-256: {sha256_file(output / 'checkpoint.pth')}")


if __name__ == "__main__":
    main()
