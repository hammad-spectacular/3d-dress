# AI Virtual Try-On — Task 1: Existing Project Inspection Report

**Date:** November 17, 2026  
**Project:** AI Virtual Try-On (Member 3 — AI & Computer Vision Developer)  
**Machine:** 16 GB RAM, 256 GB SSD (~1 GB free), Python 3.14.3, No dedicated GPU  

---

## 1. Project Structure

```
ai-research/
├── README.md                              # Workspace purpose
├── research/
│   └── model_comparison.md                # Module 1: FASHN VTON, IDM-VTON, CatVTON analysis
├── dataset/
│   ├── people/                            # 6 person images (VITON-HD test split)
│   ├── clothing/                          # 12 clothing images (VITON-HD test split, shirts/tops)
│   ├── test_pairs/
│   │   └── test_pairs.json                # 12 person↔clothing pairs
│   └── dataset_documentation.md           # Module 2: dataset sources, licenses, actual status
├── testing/
│   ├── test_cases/
│   │   ├── TC-01 through TC-06            # Model-specific test cases
│   │   └── test_cases_definitions.md      # Master test case definitions
│   ├── testing_report.md                  # Testing report template
│   └── results/                           # Empty — for test outputs
├── prototype/                             # Empty — for prototype development
├── integration/                           # Empty — for integration interface
└── future_research/                       # Empty — for future features
```

**Git status:** Committed and pushed to `https://github.com/hammad-spectacular/3d-dress` (branch `main`, commit `b48b646`)

---

## 2. Installed FASHN VTON v1.5 Package

**Location:** `C:\Users\Hammad\Downloads\temp_fashn_vton\` (editable install)  
**Package:** `fashn-vton==1.5.0` (Apache-2.0)  
**Installed via:** `pip install -e temp_fashn_vton --no-deps`

### Package Architecture

| Module | Purpose |
|--------|---------|
| `pipeline.py` | Main `TryOnPipeline` class — loads models, preprocesses, runs sampling |
| `tryon_mmdit.py` | `TryOnModel` — the diffusion transformer model |
| `dwpose/` | DWPose pose detection (ONNX models) |
| `preprocessing/` | Image preprocessing (agnostic, masks, transforms) |
| `utils/` | Checkpoint loading, tensor utilities, logging |

### Key Pipeline Interface (from pipeline.py)

```python
class TryOnPipeline:
    def __init__(self, weights_dir: str, device: Optional[str] = None)
    def __call__(
        self,
        person_image: PIL.Image.Image,
        garment_image: PIL.Image.Image,
        category: Literal["tops", "bottoms", "one-pieces"],
        garment_photo_type: Literal["model", "flat-lay"] = "model",
        num_samples: int = 1,
        num_timesteps: int = 30,
        guidance_scale: float = 1.5,
        seed: int = 42,
        segmentation_free: bool = True,
    ) -> PipelineOutput  # Contains: images: List[PIL.Image.Image]
```

**Required weight files:**
- `weights/model.safetensors` (~2 GB) — TryOn model weights
- `weights/dwpose/yolox_l.onnx` — DWPose detection
- `weights/dwpose/dw-ll_ucoco_384.onnx` — DWPose pose estimation

**Status:** Weight download incomplete (~89 MB of ~2 GB before cleanup). Download stalled due to Hugging Face rate limiting on unauthenticated requests.

---

## 3. Python Environment Compatibility

| Component | Version | Status |
|-----------|---------|--------|
| Python | 3.14.3 | ✅ Installed |
| PyTorch | 2.15.0+cpu | ✅ Installed (CPU-only) |
| torchvision | 0.29.2 | ✅ Installed |
| safetensors | 0.8.0 | ✅ Installed |
| huggingface_hub | 2.4.0 | ✅ Installed |
| pillow | latest | ✅ Installed |
| numpy | latest | ✅ Installed |
| opencv-python | 5.0.0 | ✅ Installed |
| onnxruntime | 1.32.0 | ✅ Installed (CPU) |
| fashn-human-parser | 0.1.1 | ✅ Installed |
| fashn-vton | 1.5.0 | ✅ Installed (editable) |
| CUDA / GPU | None | ❌ Not available |

### Compatibility Notes
- **Python 3.14**: FASHN VTON pyproject.toml requires `>=3.10`, so 3.14 is compatible ✅
- **PyTorch CPU**: Can run on CPU but will be very slow for diffusion inference ⚠️
- **No CUDA**: Cannot use bfloat16, will fall back to float32 ⚠️
- **Disk space**: ~1 GB free — insufficient for model weights (~2 GB) ❌

---

## 4. Identified Problems

| Problem | Severity | Impact | Workaround |
|---------|----------|--------|------------|
| Model weights not downloaded | High | Cannot run inference | Cloud GPU (Kaggle/Colab) with HF auth |
| No dedicated GPU | High | CPU inference extremely slow | Cloud GPU T4 (16GB VRAM) |
| Disk space ~1 GB | Medium | Cannot fit weights locally | Cloud execution only |
| Hugging Face rate limiting | High | Weight download stalled (~87 KB/25 min) | Use platform secrets / HF token |

---

## 5. Recommendation

**Do not attempt local model weight download.** Disk space is insufficient (~1 GB free) and Hugging Face rate limits make the download impractical without authentication.

**Path forward:** Build the complete pipeline architecture and API interface now (Tasks 2-4), then execute on cloud GPU (Kaggle, once phone verification clears, or Colab) for actual inference (Task 5 validates everything except the model forward pass).
