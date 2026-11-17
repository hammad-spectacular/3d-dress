"""
AI Virtual Try-On — Model-Independent Processing Pipeline

This module defines a pluggable pipeline for virtual try-on inference.
It works without GPU or model weights for pipeline logic validation.
The AI inference component is implemented via the TryOnModelInterface.

Usage:
    from ai_pipeline import VirtualTryOnPipeline, ValidationError, PreprocessingError, InferenceError, PostprocessingError

    pipeline = VirtualTryOnPipeline(model_adapter=None)  # model_adapter set later
    result = pipeline.run(person_image_path, garment_image_path, category="tops")
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, List, Optional, Protocol, Tuple

from PIL import Image

logger = logging.getLogger("ai_pipeline")
if not logger.handlers:
    _handler = logging.StreamHandler()
    _formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    _handler.setFormatter(_formatter)
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class PipelineError(Exception):
    """Base exception for all pipeline errors."""


class ValidationError(PipelineError):
    """Raised when input images fail validation."""


class PreprocessingError(PipelineError):
    """Raised when image preprocessing fails."""


class InferenceError(PipelineError):
    """Raised when the AI model inference fails."""


class PostprocessingError(PipelineError):
    """Raised when output post-processing fails."""


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


class GarmentCategory(str, Enum):
    TOPS = "tops"
    BOTTOMS = "bottoms"
    ONE_PIECES = "one-pieces"


class GarmentPhotoType(str, Enum):
    MODEL = "model"      # Garment worn by a person
    FLAT_LAY = "flat-lay"  # Garment on plain background


class PipelineStatus(str, Enum):
    PENDING = "pending"
    VALIDATING = "validating"
    PREPROCESSING = "preprocessing"
    INFERRING = "inferring"
    POSTPROCESSING = "postprocessing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TryOnRequest:
    """Input request for virtual try-on."""

    person_image_path: str
    garment_image_path: str
    category: GarmentCategory = GarmentCategory.TOPS
    garment_photo_type: GarmentPhotoType = GarmentPhotoType.MODEL
    num_samples: int = 1
    num_timesteps: int = 30
    guidance_scale: float = 1.5
    seed: int = 42
    segmentation_free: bool = True


@dataclass
class TryOnResult:
    """Result of virtual try-on inference."""

    status: PipelineStatus
    output_images: List[str] = field(default_factory=list)  # file paths
    processing_time_seconds: float = 0.0
    model_name: str = ""
    model_version: str = ""
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    @property
    def success(self) -> bool:
        return self.status == PipelineStatus.COMPLETED and len(self.output_images) > 0


@dataclass
class ImageInfo:
    """Validated image metadata."""

    path: str
    width: int
    height: int
    format: str
    mode: str
    size_bytes: int
    aspect_ratio: float


# ---------------------------------------------------------------------------
# Pluggable model interface
# ---------------------------------------------------------------------------


class TryOnModelInterface(Protocol):
    """
    Interface for pluggable AI try-on models.

    Any model adapter (FASHN VTON, IDM-VTON, CatVTON, etc.) must implement
    this interface to be used with VirtualTryOnPipeline.
    """

    model_name: str
    model_version: str
    supported_categories: List[GarmentCategory]
    requires_gpu: bool = False

    def load(self, weights_dir: str, device: str = "cpu") -> None:
        """Load model weights from disk. Called once at startup."""
        ...

    def is_loaded(self) -> bool:
        """Return True if model weights are loaded and ready."""
        ...

    def infer(
        self,
        person_image: Image.Image,
        garment_image: Image.Image,
        category: GarmentCategory,
        garment_photo_type: GarmentPhotoType,
        num_samples: int,
        num_timesteps: int,
        guidance_scale: float,
        seed: int,
        segmentation_free: bool,
    ) -> List[Image.Image]:
        """Run inference and return generated PIL images."""
        ...


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


class ImageValidator:
    """Validates input images before preprocessing."""

    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    MIN_DIMENSION = 64
    MAX_DIMENSION = 4096
    MAX_FILE_SIZE_MB = 50

    @classmethod
    def validate(cls, image_path: str) -> ImageInfo:
        """
        Validate a single image file.

        Returns ImageInfo if valid, raises ValidationError otherwise.
        """
        path = Path(image_path)

        if not path.exists():
            raise ValidationError(f"Image file not found: {image_path}")

        if path.suffix.lower() not in cls.ALLOWED_EXTENSIONS:
            raise ValidationError(
                f"Unsupported image format '{path.suffix}'. "
                f"Allowed: {', '.join(sorted(cls.ALLOWED_EXTENSIONS))}"
            )

        file_size_mb = path.stat().st_size / (1024 * 1024)
        if file_size_mb > cls.MAX_FILE_SIZE_MB:
            raise ValidationError(
                f"Image file too large: {file_size_mb:.1f} MB "
                f"(max {cls.MAX_FILE_SIZE_MB} MB)"
            )

        try:
            with Image.open(path) as img:
                img.verify()
            with Image.open(path) as img:
                width, height = img.size
                fmt = img.format or "UNKNOWN"
                mode = img.mode
        except Exception as exc:
            raise ValidationError(f"Invalid or corrupted image: {exc}") from exc

        if width < cls.MIN_DIMENSION or height < cls.MIN_DIMENSION:
            raise ValidationError(
                f"Image too small: {width}x{height} "
                f"(min {cls.MIN_DIMENSION}x{cls.MIN_DIMENSION})"
            )
        if width > cls.MAX_DIMENSION or height > cls.MAX_DIMENSION:
            raise ValidationError(
                f"Image too large: {width}x{height} "
                f"(max {cls.MAX_DIMENSION}x{cls.MAX_DIMENSION})"
            )

        aspect_ratio = width / height if height > 0 else 0.0

        return ImageInfo(
            path=str(path.resolve()),
            width=width,
            height=height,
            format=fmt,
            mode=mode,
            size_bytes=path.stat().st_size,
            aspect_ratio=aspect_ratio,
        )

    @classmethod
    def validate_pair(
        cls, person_path: str, garment_path: str
    ) -> Tuple[ImageInfo, ImageInfo]:
        """Validate both person and garment images."""
        person_info = cls.validate(person_path)
        garment_info = cls.validate(garment_path)
        return person_info, garment_info


# ---------------------------------------------------------------------------
# Preprocessor
# ---------------------------------------------------------------------------


class Preprocessor:
    """
    Prepares images for model inference.

    Operations are model-independent: resize, convert to RGB, basic checks.
    Model-specific preprocessing (pose detection, human parsing) is handled
    by the model adapter.
    """

    TARGET_SIZE = 768  # VITON-HD / FASHN VTON standard resolution
    MAX_UPSCALE_FACTOR = 1.0  # Never upscale — only downscale or keep

    @classmethod
    def preprocess(
        cls,
        person_image: Image.Image,
        garment_image: Image.Image,
        target_size: Tuple[int, int] = (768, 1024),
    ) -> Tuple[Image.Image, Image.Image]:
        """
        Preprocess person and garment images.

        Returns (person_image, garment_image) as RGB, resized to fit
        within target_size while preserving aspect ratio.
        """
        try:
            person_image = person_image.convert("RGB")
            garment_image = garment_image.convert("RGB")

            person_image = cls._fit_within(person_image, target_size)
            garment_image = cls._fit_within(garment_image, target_size)

            return person_image, garment_image
        except Exception as exc:
            raise PreprocessingError(f"Preprocessing failed: {exc}") from exc

    @staticmethod
    def _fit_within(image: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        """Resize image to fit within target_size, preserving aspect ratio."""
        img_w, img_h = image.size
        tgt_w, tgt_h = target_size

        scale = min(tgt_w / img_w, tgt_h / img_h, Preprocessor.MAX_UPSCALE_FACTOR)
        new_w = max(1, int(img_w * scale))
        new_h = max(1, int(img_h * scale))

        if (new_w, new_h) != (img_w, img_h):
            return image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        return image


# ---------------------------------------------------------------------------
# Postprocessor
# ---------------------------------------------------------------------------


class Postprocessor:
    """Handles output images after inference."""

    @classmethod
    def save_images(
        cls,
        images: List[Image.Image],
        output_dir: str,
        prefix: str = "tryon",
    ) -> List[str]:
        """
        Save generated images to disk.

        Returns list of output file paths.
        """
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        saved_paths: List[str] = []
        for idx, img in enumerate(images):
            out_path = out_dir / f"{prefix}_{idx:02d}.png"
            try:
                img.save(out_path, format="PNG")
                saved_paths.append(str(out_path.resolve()))
            except Exception as exc:
                raise PostprocessingError(
                    f"Failed to save output image {idx}: {exc}"
                ) from exc

        return saved_paths


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


class VirtualTryOnPipeline:
    """
    Model-independent virtual try-on pipeline.

    Orchestrates: validate → preprocess → infer → postprocess.

    The model adapter is pluggable. Set it via `set_model_adapter()` or
    pass it to the constructor. If no adapter is set, inference will fail
    with InferenceError (expected when model weights are unavailable).
    """

    def __init__(self, model_adapter: Optional[TryOnModelInterface] = None):
        self.model_adapter = model_adapter
        self.validator = ImageValidator()
        self.preprocessor = Preprocessor()
        self.postprocessor = Postprocessor()
        self.logger = logger

    def set_model_adapter(self, adapter: TryOnModelInterface) -> None:
        """Register a model adapter for inference."""
        self.model_adapter = adapter
        self.logger.info(f"Model adapter set: {getattr(adapter, 'model_name', 'unknown')}")

    def run(self, request: TryOnRequest, output_dir: str = "outputs") -> TryOnResult:
        """
        Execute the full try-on pipeline.

        Steps:
          1. Validate input images
          2. Preprocess images
          3. Run model inference (via adapter)
          4. Postprocess and save outputs

        Returns a TryOnResult with status, output paths, and timing.
        """
        start_time = time.time()
        result = TryOnResult(
            status=PipelineStatus.PENDING,
            model_name=getattr(self.model_adapter, "model_name", "none"),
            model_version=getattr(self.model_adapter, "model_version", "none"),
        )

        try:
            # ── Step 1: Validate ──────────────────────────────────────
            result.status = PipelineStatus.VALIDATING
            self.logger.info("Validating input images...")
            person_info, garment_info = self.validator.validate_pair(
                request.person_image_path, request.garment_image_path
            )
            self.logger.info(
                f"Person: {person_info.width}x{person_info.height} {person_info.format}; "
                f"Garment: {garment_info.width}x{garment_info.height} {garment_info.format}"
            )
            result.metadata["person_info"] = {
                "width": person_info.width,
                "height": person_info.height,
                "format": person_info.format,
                "size_bytes": person_info.size_bytes,
            }
            result.metadata["garment_info"] = {
                "width": garment_info.width,
                "height": garment_info.height,
                "format": garment_info.format,
                "size_bytes": garment_info.size_bytes,
            }

            # ── Step 2: Preprocess ────────────────────────────────────
            result.status = PipelineStatus.PREPROCESSING
            self.logger.info("Preprocessing images...")
            with Image.open(request.person_image_path) as p_img, Image.open(
                request.garment_image_path
            ) as g_img:
                person_img, garment_img = self.preprocessor.preprocess(
                    p_img, g_img, target_size=(768, 1024)
                )

            # ── Step 3: Infer ─────────────────────────────────────────
            result.status = PipelineStatus.INFERRING
            self.logger.info("Running model inference...")
            if self.model_adapter is None:
                raise InferenceError(
                    "No model adapter configured. "
                    "Set a TryOnModelAdapter via set_model_adapter() before running."
                )
            if not self.model_adapter.is_loaded():
                raise InferenceError(
                    "Model adapter is not loaded. "
                    "Call adapter.load(weights_dir) before running inference."
                )

            output_images = self.model_adapter.infer(
                person_image=person_img,
                garment_image=garment_img,
                category=request.category,
                garment_photo_type=request.garment_photo_type,
                num_samples=request.num_samples,
                num_timesteps=request.num_timesteps,
                guidance_scale=request.guidance_scale,
                seed=request.seed,
                segmentation_free=request.segmentation_free,
            )

            # ── Step 4: Postprocess ───────────────────────────────────
            result.status = PipelineStatus.POSTPROCESSING
            self.logger.info("Postprocessing and saving outputs...")
            output_paths = self.postprocessor.save_images(
                output_images, output_dir=output_dir, prefix="tryon"
            )
            result.output_images = output_paths

            # ── Complete ─────────────────────────────────────────────
            result.status = PipelineStatus.COMPLETED
            result.processing_time_seconds = round(time.time() - start_time, 3)
            self.logger.info(
                f"Pipeline completed in {result.processing_time_seconds}s. "
                f"Generated {len(output_paths)} image(s)."
            )

        except PipelineError as exc:
            result.status = PipelineStatus.FAILED
            result.error_message = str(exc)
            result.error_type = exc.__class__.__name__
            result.processing_time_seconds = round(time.time() - start_time, 3)
            self.logger.error(f"Pipeline failed: {exc}")
        except Exception as exc:  # pylint: disable=broad-except
            result.status = PipelineStatus.FAILED
            result.error_message = f"Unexpected error: {exc}"
            result.error_type = "UnexpectedError"
            result.processing_time_seconds = round(time.time() - start_time, 3)
            self.logger.exception("Pipeline failed with unexpected error")

        return result

    def run_from_paths(
        self,
        person_image_path: str,
        garment_image_path: str,
        category: str = "tops",
        output_dir: str = "outputs",
        **kwargs: Any,
    ) -> TryOnResult:
        """Convenience wrapper that builds a TryOnRequest from paths."""
        try:
            cat = GarmentCategory(category)
        except ValueError:
            cat = GarmentCategory.TOPS

        request = TryOnRequest(
            person_image_path=person_image_path,
            garment_image_path=garment_image_path,
            category=cat,
            **kwargs,
        )
        return self.run(request, output_dir=output_dir)
