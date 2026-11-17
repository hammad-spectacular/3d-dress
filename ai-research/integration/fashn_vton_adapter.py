"""
FASHN VTON v1.5 Model Adapter

Implements the TryOnModelInterface for the FASHN VTON v1.5 model.
This adapter wraps the installed `fashn_vton` package.

NOTE: Model weights (~2 GB) are NOT downloaded. The adapter's `load()`
method will raise FileNotFoundError if weights are missing. Inference
cannot run until weights are available on a GPU-enabled machine.
"""

from __future__ import annotations

import logging
import os
from typing import Any, List, Optional

from PIL import Image

from ai_pipeline import (
    GarmentCategory,
    GarmentPhotoType,
    TryOnModelInterface,
)

logger = logging.getLogger("fashn_vton_adapter")
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(_h)
    logger.setLevel(logging.INFO)


class FASHNVTONAdapter:
    """
    Adapter for FASHN VTON v1.5 model.

    Wraps the `fashn_vton.TryOnPipeline` class. Requires model weights
    (model.safetensors, dwpose/ ONNX files) to be present in weights_dir.
    """

    model_name = "FASHN VTON v1.5"
    model_version = "1.5.0"
    supported_categories = [
        GarmentCategory.TOPS,
        GarmentCategory.BOTTOMS,
        GarmentCategory.ONE_PIECES,
    ]
    requires_gpu = False  # Can run on CPU but very slow; GPU recommended

    def __init__(self):
        self._pipeline = None
        self._weights_dir: Optional[str] = None
        self._device: str = "cpu"
        self._loaded: bool = False

    def load(self, weights_dir: str, device: str = "cpu") -> None:
        """
        Load FASHN VTON v1.5 model weights.

        Args:
            weights_dir: Directory containing model.safetensors and dwpose/ ONNX files.
            device: "cpu" or "cuda".

        Raises:
            FileNotFoundError: If required weight files are missing.
            ImportError: If fashn_vton package is not installed.
        """
        try:
            from fashn_vton import TryOnPipeline as _TryOnPipeline
        except ImportError as exc:
            raise ImportError(
                "fashn-vton package is not installed. "
                "Install with: pip install -e <path-to-fashn-vton-repo> --no-deps"
            ) from exc

        self._weights_dir = os.path.abspath(weights_dir)
        self._device = device

        # Validate required weight files before constructing pipeline
        required_files = [
            os.path.join(weights_dir, "model.safetensors"),
            os.path.join(weights_dir, "dwpose", "yolox_l.onnx"),
            os.path.join(weights_dir, "dwpose", "dw-ll_ucoco_384.onnx"),
        ]
        missing = [f for f in required_files if not os.path.exists(f)]
        if missing:
            raise FileNotFoundError(
                "Missing FASHN VTON v1.5 weight files:\n"
                + "\n".join(f"  - {m}" for m in missing)
                + f"\n\nDownload weights first:\n"
                f"  python scripts/download_weights.py --weights-dir {weights_dir}"
            )

        self._pipeline = _TryOnPipeline(weights_dir=weights_dir, device=device)
        self._loaded = True
        logger.info(f"FASHN VTON v1.5 loaded on device={device}")

    def is_loaded(self) -> bool:
        return self._loaded and self._pipeline is not None

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
        """
        Run FASHN VTON v1.5 inference.

        Returns a list of generated PIL Image objects.
        """
        if not self.is_loaded():
            raise RuntimeError(
                "FASHN VTON adapter is not loaded. Call load() first."
            )

        from ai_pipeline import PipelineError

        try:
            from fashn_vton import PipelineOutput
        except ImportError as exc:
            raise PipelineError("fashn-vton package not available") from exc

        result: PipelineOutput = self._pipeline(
            person_image=person_image,
            garment_image=garment_image,
            category=category.value,
            garment_photo_type=garment_photo_type.value,
            num_samples=num_samples,
            num_timesteps=num_timesteps,
            guidance_scale=guidance_scale,
            seed=seed,
            segmentation_free=segmentation_free,
        )

        return list(result.images)

    def get_requirements(self) -> dict:
        """Return hardware/software requirements for this model."""
        return {
            "model_name": self.model_name,
            "model_version": self.model_version,
            "requires_gpu": self.requires_gpu,
            "recommended_vram_gb": 8,
            "min_vram_gb": 8,
            "supports_cpu": True,
            "cpu_slow": True,
            "weight_files": [
                "model.safetensors (~2 GB)",
                "dwpose/yolox_l.onnx",
                "dwpose/dw-ll_ucoco_384.onnx",
            ],
            "supported_categories": [c.value for c in self.supported_categories],
        }
