"""
AI Virtual Try-On — Integration Package

Contains the model-independent AI pipeline and model adapters.

Modules:
  - ai_pipeline: Model-independent processing pipeline (validate → preprocess → infer → postprocess)
  - fashn_vton_adapter: FASHN VTON v1.5 model adapter (requires model weights + GPU for inference)
"""

from .ai_pipeline import (
    VirtualTryOnPipeline,
    TryOnRequest,
    TryOnResult,
    TryOnModelInterface,
    ImageValidator,
    Preprocessor,
    Postprocessor,
    ValidationError,
    PreprocessingError,
    InferenceError,
    PostprocessingError,
    PipelineError,
    PipelineStatus,
    GarmentCategory,
    GarmentPhotoType,
    ImageInfo,
)

from .fashn_vton_adapter import FASHNVTONAdapter

__all__ = [
    "VirtualTryOnPipeline",
    "TryOnRequest",
    "TryOnResult",
    "TryOnModelInterface",
    "ImageValidator",
    "Preprocessor",
    "Postprocessor",
    "FASHNVTONAdapter",
    "ValidationError",
    "PreprocessingError",
    "InferenceError",
    "PostprocessingError",
    "PipelineError",
    "PipelineStatus",
    "GarmentCategory",
    "GarmentPhotoType",
    "ImageInfo",
]
