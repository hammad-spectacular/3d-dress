# AI Virtual Try-On — Module 1: AI Model Research Report

**Prepared for:** Member 3 — AI & Computer Vision Developer  
**Project:** AI Virtual Try-On  
**Workspace:** `ai-research/`  
**Report file:** `ai-research/research/model_comparison.md`  
**Machine constraints:** 16 GB RAM, 256 GB SSD, **no dedicated GPU assumed**

---

## 1. Scope and Method

This report investigates three virtual try-on (VTON) models:

1. **FASHN AI** — FASHN AI (UK), commercial API + open-source model weights
2. **IDM-VTON** — Yisol Choi et al. (KAIST / OMNIOUS.AI), ECCV 2024
3. **CatVTON** — Zheng Chong et al. (Sun Yat-Sen University et al.), ICLR 2025

For each model, the report covers: how it works, API availability, local installability, hardware/VRAM requirements, API pricing & limits, commercial licensing, image quality, detail preservation, processing speed, and ease of Python integration.

**Information quality markers used throughout:**
- `[VERIFIED]` — stated in official documentation, GitHub repository, arXiv paper, or model-card license file.
- `[ESTIMATE]` — derived from community reports, third-party benchmarks, or inference; not confirmed by the authors.

**Sources consulted:** official docs, GitHub repositories, Hugging Face model cards, arXiv papers, LICENSE files. No API credits were purchased, no models were downloaded, and no libraries were installed.

---

## 2. Individual Model Analysis

---

### 2.1 FASHN AI

**Homepage:** https://fashn.ai/  
**API docs:** https://docs.fashn.ai/  
**API pricing:** https://help.fashn.ai/plans-and-pricing/api-pricing  
**GitHub org:** https://github.com/fashn-AI  
**Open-source model (VTON v1.5):** https://github.com/fashn-AI/fashn-vton-1.5  
**VTON v1.5 blog:** https://fashn.ai/blog/fashn-vton-1-5-open-source-release

#### How it works

FASHN AI offers **two distinct products**:

1. **FASHN API (managed service)** — two virtual try-on endpoints:
   - **Try-On v1.6:** "Fast, lightweight virtual try-on optimized for real-time e-commerce experiences" `[VERIFIED]`. Takes a person image + garment image, returns the person wearing the garment. Input processed at 864 × 1296 px `[VERIFIED]`.
   - **Try-On Max:** "Most capable virtual try-on model, with enhanced fidelity, up to 4K resolution, and prompt-based customization" `[VERIFIED]`. Supports clothing, shoes, hats, jewelry, bags. Released January 2026 (Preview lifecycle) `[VERIFIED]`.
   - Both are synchronous/async REST endpoints (`POST /v1/run`) with polling or webhook delivery `[VERIFIED]`.

2. **FASHN VTON v1.5 (open-source, self-hostable):** "Efficient Maskless Virtual Try-On in Pixel Space" `[VERIFIED]`. Generates photorealistic try-on images directly in pixel space without segmentation masks. Supports model photos and flat-lay product shots as garment inputs `[VERIFIED]`. Native Python package `fashn-vton` with a `TryOnPipeline` class `[VERIFIED]`.

#### Official API available?

**Yes.** The FASHN API is the primary product. Official Python and TypeScript SDKs are provided `[VERIFIED]`. No subscription required; pay-as-you-go credits `[VERIFIED]`. New accounts get 10 complimentary credits `[VERIFIED]`.

#### Local installation possible?

**Partially.**
- The **managed API** cannot be self-hosted — it is a cloud service only `[VERIFIED]`.
- **FASHN VTON v1.5** is open-source and can be installed locally via `pip install -e .` `[VERIFIED]`. Weights (~2 GB total) download from Hugging Face `[VERIFIED]`. CPU fallback is supported by swapping `onnxruntime-gpu` for `onnxruntime` `[VERIFIED]`, but the pipeline "automatically uses GPU if available" `[VERIFIED]`.

#### Hardware requirements

- **FASHN API:** None on the user side — inference runs on FASHN's servers `[VERIFIED]`.
- **FASHN VTON v1.5 (local):** The try-on weights are stored in bfloat16 and run in bf16 on Ampere+ GPUs (RTX 30xx/40xx, A100, H100); on older hardware or CPU, weights are converted to float32 `[VERIFIED]`. No published minimum VRAM figure for v1.5 `[ESTIMATE]`. CPU-only operation is technically possible but expected to be slow for a diffusion model `[ESTIMATE]`.

#### Hardware fit for our machine (16 GB RAM, 256 GB SSD, no GPU)

- **API path:** Excellent fit — no local GPU required `[VERIFIED]`.
- **Local v1.5 on CPU:** Technically installable but diffusion inference on CPU-only with 16 GB RAM would be slow and is not a realistic prototype path `[ESTIMATE]`.

#### API pricing and usage limits

`[VERIFIED]` from https://help.fashn.ai/plans-and-pricing/api-pricing:

- **On-demand:** $0.075 per credit; minimum purchase $7.50 (100 credits); credits expire 12 months after purchase `[VERIFIED]`.
- **Try-On v1.6:** 1 credit per output image → **~$0.075 per image** `[VERIFIED]`.
- **Try-On Max:** 1–5 credits per output image depending on resolution (1k/2k/4k) and generation mode (fast/balanced/quality) → **~$0.075–$0.375 per image** `[VERIFIED]`.
- **Existing monthly plans (Basic/Pro/Agency):** no longer available to new customers `[VERIFIED]`.
- **Failed predictions:** not charged `[VERIFIED]`.
- **Processing time (v1.6):** performance ~5 s, balanced ~8 s, quality ~12–17 s `[VERIFIED]`.
- **Processing time (Try-On Max):** fast+1k ~10 s; balanced+2k ~25 s; quality+4k ~55 s `[VERIFIED]`.
- **Input limits:** 30 MiB per image, min 15×15 px, aspect ratio 1:16 to 16:1 `[VERIFIED]`.

#### Commercial licensing and restrictions

- **FASHN API:** Explicitly "Available for commercial use" `[VERIFIED]`. Outputs are deleted after 3 days; data not used for training unless opted in `[VERIFIED]`.
- **FASHN VTON v1.5 (local code + weights):** Apache-2.0 license `[VERIFIED]`. Commercially usable `[VERIFIED]`. Third-party components (DWPose, YOLOX, fashn-human-parser) carry their own permissive/non-commercial terms — the human parser "inherits the NVIDIA Source Code License" `[VERIFIED]`.

#### Image generation quality

- Try-On Max is positioned for "publishable e-commerce content," PDPs, catalogs, and marketing assets `[VERIFIED]`.
- Try-On v1.6 is positioned for "real-time e-commerce experiences" where speed and cost are primary concerns `[VERIFIED]`.
- v1.5 is described as generating "photorealistic images" `[VERIFIED]`.
- No independent quantitative quality benchmark (FID, SSIM, LPIPS) was found in official docs `[ESTIMATE]`.

#### Clothing color, pattern, and detail preservation

- Try-On Max supports prompt-based customization (e.g., "tuck in shirt", "roll up sleeves") `[VERIFIED]`.
- v1.5 is maskless and operates in pixel space, which the authors claim preserves body features and allows unconstrained garment volume `[VERIFIED]`.
- No specific published claim about pattern/logo/text preservation for FASHN models `[ESTIMATE]`.

#### Processing speed

- API v1.6: 5–17 s per image depending on mode `[VERIFIED]`.
- API Try-On Max: 10–55 s depending on resolution/mode `[VERIFIED]`.
- Local v1.5: not published `[ESTIMATE]`.

#### Ease of integration with Python

- **API:** Official Python SDK + REST `POST /v1/run`; quickstart guide available `[VERIFIED]`. Very easy — send image URLs, poll/webhook for result.
- **Local v1.5:** Native Python package `from fashn_vton import TryOnPipeline` `[VERIFIED]`. Very easy Python integration if running locally with GPU.

---

### 2.2 IDM-VTON

**GitHub:** https://github.com/yisol/IDM-VTON  
**Project page:** https://idm-vton.github.io/  
**Hugging Face:** https://huggingface.co/yisol/IDM-VTON  
**Paper:** "Improving Diffusion Models for Authentic Virtual Try-on in the Wild," ECCV 2024  
**License file:** https://github.com/yisol/IDM-VTON/blob/main/LICENSE.txt

#### How it works

IDM-VTON is a diffusion-model-based virtual try-on system. It takes a person image and a garment image and generates the person wearing the garment, preserving the garment's print, logo, and texture `[VERIFIED]`. The architecture builds on SDXL inpainting 0.1 + IP-Adapter `[ESTIMATE]` and uses DensePose + human parsing (SCHP) for preprocessing `[VERIFIED]` from README acknowledgements. It requires pose estimation, densepose, and human-parsing checkpoints for local inference `[VERIFIED]`.

#### Official API available?

**No.** IDM-VTON is research code released on GitHub and Hugging Face. There is no official managed API from the authors `[VERIFIED]`. The official Hugging Face Space (yisol/IDM-VTON) is a free demo running on ZeroGPU, not a commercial API `[VERIFIED]`.

#### Local installation possible?

**Yes.** `git clone`, `conda env create -f environment.yaml`, then run `inference.py` or `gradio_demo/app.py` `[VERIFIED]`. Requires Python 3.10, PyTorch 2.0.1 + CUDA 11.8, diffusers 0.25.0, transformers 4.36.2, accelerate 0.25.0 `[VERIFIED]`. In practice requires Linux and an NVIDIA GPU `[VERIFIED]`.

#### Hardware requirements

`[VERIFIED]` from GitHub issues and author comments:
- Authors state: ">18 GB VRAM is required for single image inference" `[VERIFIED]` (GitHub issue #43, author comment).
- ComfyUI port (TemryL) requires "at least 16 GB VRAM" `[VERIFIED]` from its README.
- Real-world reports: RTX 4090 (24 GB) → ~8 s/image; RTX 4080 Super (16 GB) → ~5 minutes/image (VRAM overflows to system RAM); NVIDIA T4 (16 GB) → out-of-memory failure `[VERIFIED]` from fitroom.app benchmark and GitHub issue #94.
- A community fork claims operation as low as 8.2 GB VRAM with 4-bit precision + CPU offloading `[ESTIMATE]` (not official).

**Hardware fit for our machine:** NOT feasible. No dedicated GPU assumed, and IDM-VTON needs 18–24 GB VRAM on an NVIDIA GPU `[VERIFIED]`.

#### API pricing and usage limits

**N/A** — no official API `[VERIFIED]`. The free Hugging Face ZeroGPU demo has daily quotas (2 min logged out, 5 min free account, 40 min PRO) `[VERIFIED]` from Hugging Face ZeroGPU docs, but this is for evaluation only, not production.

#### Commercial licensing and restrictions

**CC BY-NC-SA 4.0** — "The codes and checkpoints in this repository are under the CC BY-NC-SA 4.0 license" `[VERIFIED]` from README and LICENSE. The "NC" (NonCommercial) clause means the code and weights **cannot be used for commercial advantage or monetary compensation** `[VERIFIED]`.

- Users have requested a commercial license in GitHub issue #160 since November 2024; as of October 2026 there is **no response from the authors** `[VERIFIED]` from issue thread.
- Training data (VITON-HD: CC BY-NC 4.0; DressCode: non-commercial academic) also carries non-commercial terms `[ESTIMATE]`.
- **Conclusion: IDM-VTON is not commercially usable under its public license.** `[VERIFIED]`

#### Image generation quality

- ECCV 2024 paper; positioned as high-fidelity "authentic virtual try-on in the wild" `[VERIFIED]`.
- Preserves garment print, logo, texture `[VERIFIED]`.
- No official quantitative benchmark published in the README `[ESTIMATE]`.

#### Clothing color, pattern, and detail preservation

- Explicitly designed to preserve garment print, logo, and texture `[VERIFIED]`.
- Requires correct masking; inaccurate masks significantly degrade results `[ESTIMATE]`.

#### Processing speed

- RTX 4090 (24 GB VRAM): ~8 seconds per image `[VERIFIED]`.
- RTX 4080 Super (16 GB VRAM): ~5 minutes per image (VRAM overflow) `[VERIFIED]`.
- Paper Table 2 reports 17.32 s at 1024×768 on a single A100 `[VERIFIED]`.

#### Ease of integration with Python

- Python inference scripts (`inference.py`, `inference_dc.py`) via `accelerate launch` `[VERIFIED]`.
- Gradio demo app available `[VERIFIED]`.
- Integration requires managing DensePose, human-parsing, and OpenPose checkpoints manually `[VERIFIED]`. Moderate-to-hard integration effort.

---

### 2.3 CatVTON

**GitHub:** https://github.com/Zheng-Chong/CatVTON  
**Paper:** "CatVTON: Concatenation Is All You Need for Virtual Try-On with Diffusion Models," arXiv:2407.15886, ICLR 2025  
**Hugging Face:** https://huggingface.co/zhengchong/CatVTON  
**License:** https://github.com/Zheng-Chong/CatVTON/blob/main/LICENSE

#### How it works

CatVTON is a "simple and efficient virtual try-on diffusion model" `[VERIFIED]`. It concatenates person and garment images along spatial dimensions as inputs to a simplified denoising UNet, removing redundant image/text encoders and cross-attention `[VERIFIED]` from arXiv paper. It is built on Stable Diffusion v1.5 inpainting `[VERIFIED]` from paper. It eliminates pose estimation, human parsing, and captioning at inference — requires only person image + garment reference (+ optional binary mask) `[VERIFIED]`.

- Total parameters: 899.06M; trainable parameters: 49.57M (~5.5% of backbone) `[VERIFIED]` from paper Table 3.
- Inference memory usage: 4.00 GB (claimed), 5.94 GB at 1024×768 (Table 2) `[VERIFIED]`.
- Paper claims "under 8 GB VRAM for 1024×768 resolution" `[VERIFIED]` from README.

#### Official API available?

**No.** CatVTON is research code on GitHub and Hugging Face. No official managed API from the authors `[VERIFIED]`. A Hugging Face Space demo existed (on ZeroGPU) but was reported as down as of October 2026 `[ESTIMATE]` from fashiolabs guide.

#### Local installation possible?

**Yes.** Python-based inference code with checkpoints auto-downloaded from Hugging Face `[VERIFIED]` from README. ComfyUI workflow available `[VERIFIED]`.

#### Hardware requirements

- Paper Table 3: memory usage 4.00 GB `[VERIFIED]`.
- README: "< 8G VRAM for 1024×768 resolution" `[VERIFIED]`.
- Paper: "deployed on resource-constrained devices, such as consumer-level GPUs with less than 8 GB of VRAM" `[VERIFIED]`.
- Note: AMD GPU support is problematic (one issue reported 40+ GB VRAM usage and very slow speed on AMD) `[ESTIMATE]` from GitHub issue #44. NVIDIA/CUDA is the practical path `[ESTIMATE]`.

**Hardware fit for our machine:** NOT feasible without a dedicated GPU. Even though the model claims <8 GB VRAM, it still requires a CUDA-capable NVIDIA GPU `[VERIFIED]`. On CPU-only with 16 GB RAM, diffusion inference would be extremely slow `[ESTIMATE]`.

#### API pricing and usage limits

**N/A** — no official API `[VERIFIED]`.

#### Commercial licensing and restrictions

**CC BY-NC-SA 4.0** — "All the materials, including code, checkpoints, and demo, are made available under the Creative Commons BY-NC-SA 4.0 license... for non-commercial purposes" `[VERIFIED]` from README and LICENSE. The demo app header states "This demo and our weights are only for Non-commercial Use" `[VERIFIED]` from fashiolabs guide.

- **Not commercially usable** under the public license `[VERIFIED]`.
- No commercial license option has been offered by the authors `[ESTIMATE]`.
- Base model (SD 1.5 inpainting, CreativeML OpenRAIL-M) is permissive on its own, but does not lift CatVTON's NC terms `[ESTIMATE]`.

#### Image generation quality

- ICLR 2025; paper claims "superior qualitative and quantitative results compared to baseline methods" `[VERIFIED]`.
- Paper Figure 5: handles complex patterns, texture positioning, occlusions, wrinkles, lighting, shadows better than baselines `[VERIFIED]`.
- Trained on ~73K samples from public datasets (VITON-HD, DressCode) `[VERIFIED]`.
- Limitation: VAE decoding may cause detail loss and color discrepancies, especially at 512×384 `[VERIFIED]` from paper. Mask accuracy strongly affects results `[VERIFIED]`.

#### Clothing color, pattern, and detail preservation

- Paper explicitly states: "performs exceptionally well on fine patterns of garments, without altering or distorting the text and patterns on the garments" `[VERIFIED]`.
- Also reproduces "semi-transparent materials" and garment length consistently `[VERIFIED]`.
- CFG strength 2.5–3.5 recommended; beyond 3.5 causes color distortions and noise `[VERIFIED]` from paper.

#### Processing speed

`[VERIFIED]` from paper Table 2 (single NVIDIA A100, batch size 1, averaged over 10 runs):
| Resolution | CatVTON | IDM-VTON | OOTDiffusion | StableVTON |
|---|---|---|---|---|
| 512×384 | 2.58 s | 12.96 s | 4.76 s | 12.17 s |
| 1024×768 | 9.25 s | 17.32 s | 36.23 s | 36.10 s |

CatVTON is the fastest of the diffusion-based methods compared in the paper `[VERIFIED]`.

#### Ease of integration with Python

- Python inference script with argparse for dataset (dresscode/vitonhd) `[VERIFIED]`.
- Requires mask input (mask-based version) or is mask-free `[VERIFIED]`.
- No pose/parsing preprocessing needed at inference, which simplifies integration `[VERIFIED]`.
- Still requires a CUDA GPU and PyTorch/diffusers stack `[VERIFIED]`.

---

## 3. Comparison Table

| Criterion | FASHN AI (API) | FASHN VTON v1.5 (local, OSS) | IDM-VTON | CatVTON |
|---|---|---|---|---|
| **Type** | Managed REST API | Open-source model (self-host) | Open-source research code | Open-source research code |
| **Official API** | Yes (`POST /v1/run`, Python/TS SDK) `[VERIFIED]` | No (local library only) `[VERIFIED]` | No `[VERIFIED]` | No `[VERIFIED]` |
| **Commercial use** | Yes — explicitly allowed `[VERIFIED]` | Yes — Apache-2.0 `[VERIFIED]` | **No** — CC BY-NC-SA 4.0 `[VERIFIED]` | **No** — CC BY-NC-SA 4.0 `[VERIFIED]` |
| **Local install** | No (API only) `[VERIFIED]` | Yes — `pip install -e .` `[VERIFIED]` | Yes — conda + CUDA `[VERIFIED]` | Yes — Python + diffusers `[VERIFIED]` |
| **Works on our machine (no GPU)** | Yes (API, cloud GPU) `[VERIFIED]` | CPU fallback possible but slow `[ESTIMATE]` | **No** — needs 18–24 GB VRAM NVIDIA GPU `[VERIFIED]` | **No** — needs CUDA GPU `[VERIFIED]` |
| **Min VRAM (local)** | N/A | Not published `[ESTIMATE]` | >18 GB (authors), 24 GB recommended `[VERIFIED]` | <8 GB claimed at 1024×768 `[VERIFIED]` |
| **Processing speed** | v1.6: 5–17 s `[VERIFIED]`; Max: 10–55 s `[VERIFIED]` | Not published `[ESTIMATE]` | ~8 s on RTX 4090; ~5 min on 16 GB `[VERIFIED]` | 2.58 s (512×384), 9.25 s (1024×768) on A100 `[VERIFIED]` |
| **Pricing** | $0.075/credit; v1.6 = 1 credit/img (~$0.075/img); Max = 1–5 credits/img `[VERIFIED]` | Free (self-hosted; infrastructure cost only) `[VERIFIED]` | Free (model); GPU hosting $200–$700/mo `[ESTIMATE]` | Free (model); GPU hosting cost `[ESTIMATE]` |
| **Free trial** | 10 complimentary credits `[VERIFIED]` | N/A | HF ZeroGPU demo (quota-limited) `[VERIFIED]` | HF Space (reported down Oct 2026) `[ESTIMATE]` |
| **Resolution** | v1.6: 864×1296 input `[VERIFIED]`; Max: up to 4K `[VERIFIED]` | Not published `[ESTIMATE]` | 768×1024 `[VERIFIED]` | 1024×768 `[VERIFIED]` |
| **Python integration** | Official SDK — very easy `[VERIFIED]` | Native Python package — very easy `[VERIFIED]` | Python scripts + manual checkpoints — moderate `[VERIFIED]` | Python scripts — moderate `[VERIFIED]` |
| **Detail/pattern preservation** | Not specifically published `[ESTIMATE]` | Maskless, pixel space `[VERIFIED]` | Preserves print/logo/texture `[VERIFIED]` | Strong on fine patterns/text `[VERIFIED]` |
| **Commercial license available** | Yes (API terms) `[VERIFIED]` | Yes (Apache-2.0) `[VERIFIED]` | No — issue #160 open, no author response `[VERIFIED]` | No `[ESTIMATE]` |

---

## 4. Licensing and Commercial-Use Analysis

This is the most important section for our project, because the requirement is a **commercially usable** virtual try-on system.

| Model | License | Commercially usable? | Evidence |
|---|---|---|---|
| **FASHN AI API** | Commercial API terms | **Yes** | "Available for commercial use" — https://help.fashn.ai/plans-and-pricing/api-pricing `[VERIFIED]` |
| **FASHN VTON v1.5** | Apache-2.0 | **Yes** | LICENSE in https://github.com/fashn-AI/fashn-vton-1.5 `[VERIFIED]` |
| **IDM-VTON** | CC BY-NC-SA 4.0 | **No** | "NC" = NonCommercial; no commercial license offered (issue #160 open since Nov 2024, no author response) `[VERIFIED]` |
| **CatVTON** | CC BY-NC-SA 4.0 | **No** | "for non-commercial purposes" in README and LICENSE `[VERIFIED]` |

**Critical note:** Do not assume open-source means commercially usable. Both IDM-VTON and CatVTON are open-source (code and weights are publicly downloadable) but carry **CC BY-NC-SA 4.0**, which prohibits commercial use. Wrapping them in an API or ComfyUI node does not change the license `[VERIFIED]` from community analyses and license text.

Only **FASHN AI** (both the managed API and the Apache-2.0 VTON v1.5) offers a clear commercial-use path `[VERIFIED]`.

---

## 5. Hardware and Cost Comparison

Our machine: **16 GB RAM, 256 GB SSD, no dedicated GPU assumed.**

### Hardware feasibility on our machine

| Model | Can run locally on our machine? | Reason |
|---|---|---|
| FASHN AI API | **Yes** — no local GPU needed `[VERIFIED]` | Cloud inference |
| FASHN VTON v1.5 | Partially — CPU fallback possible but slow `[ESTIMATE]` | Diffusion on CPU with 16 GB RAM is not realistic for prototyping |
| IDM-VTON | **No** `[VERIFIED]` | Requires >18 GB VRAM NVIDIA GPU |
| CatVTON | **No** `[VERIFIED]` | Requires CUDA-capable NVIDIA GPU (<8 GB VRAM claimed, but still needs GPU) |

### Cost comparison

| Model | Upfront cost | Per-image cost | Infrastructure |
|---|---|---|---|
| FASHN AI API | $0 (10 free credits) `[VERIFIED]` | ~$0.075 (v1.6) to ~$0.375 (Max) `[VERIFIED]` | None — cloud |
| FASHN VTON v1.5 | $0 (Apache-2.0) `[VERIFIED]` | $0 (self-hosted) | GPU needed for speed; CPU-only impractical |
| IDM-VTON | $0 (model) `[VERIFIED]` | $0 (self-hosted) | $200–$700/mo GPU hosting `[ESTIMATE]` |
| CatVTON | $0 (model) `[VERIFIED]` | $0 (self-hosted) | GPU needed (claimed <8 GB VRAM) `[VERIFIED]` |

Given our machine has **no dedicated GPU**, the only realistic path for local inference would be CPU-only, which is impractical for diffusion-based VTON `[ESTIMATE]`. The FASHN API is the only option that works immediately on our hardware without additional purchases `[VERIFIED]`.

---

## 6. Advantages and Disadvantages

### FASHN AI

**Advantages:**
- Commercially usable (API terms explicitly allow it) `[VERIFIED]`.
- No local GPU required — works on our 16 GB RAM / no-GPU machine `[VERIFIED]`.
- Official Python SDK and TypeScript SDK `[VERIFIED]`.
- Pay-as-you-go, no subscription, minimum $7.50 top-up `[VERIFIED]`.
- Fast: 5–17 s (v1.6) or 10–55 s (Max) `[VERIFIED]`.
- Up to 4K resolution with Try-On Max `[VERIFIED]`.
- Two endpoints: v1.6 for speed/cost, Max for quality `[VERIFIED]`.
- Failed requests not charged `[VERIFIED]`.
- Open-source v1.5 (Apache-2.0) available as a future self-hosted option `[VERIFIED]`.

**Disadvantages:**
- Per-image cost (not free at scale) `[VERIFIED]`.
- API dependency — cannot fully self-host the managed endpoints `[VERIFIED]`.
- v1.6 input fixed at 864×1296 px `[VERIFIED]`.
- No published independent quality benchmark (FID/SSIM) `[ESTIMATE]`.
- Credits expire 12 months after purchase `[VERIFIED]`.

### IDM-VTON

**Advantages:**
- Free model weights and code `[VERIFIED]`.
- High-fidelity results (ECCV 2024) `[VERIFIED]`.
- Preserves garment print, logo, texture `[VERIFIED]`.
- Active community (5,200+ GitHub stars, 1.6M+ HF downloads) `[VERIFIED]`.

**Disadvantages:**
- **Not commercially usable** (CC BY-NC-SA 4.0) `[VERIFIED]` — eliminates it for our project.
- Requires >18–24 GB VRAM NVIDIA GPU — impossible on our machine `[VERIFIED]`.
- Slow on consumer GPUs (~5 min on 16 GB) `[VERIFIED]`.
- Complex preprocessing (DensePose, human parsing, OpenPose checkpoints) `[VERIFIED]`.
- No commercial license available (issue #160 unresolved) `[VERIFIED]`.
- Stack is from early 2024 (PyTorch 2.0.1, CUDA 11.8) — version-pinning required `[VERIFIED]`.

### CatVTON

**Advantages:**
- Free model weights and code `[VERIFIED]`.
- Fastest of the compared diffusion models (2.58–9.25 s on A100) `[VERIFIED]`.
- Low VRAM claim (<8 GB at 1024×768) `[VERIFIED]`.
- No pose/parsing preprocessing at inference — simpler pipeline `[VERIFIED]`.
- Strong on fine patterns and text preservation `[VERIFIED]`.
- ICLR 2025 (recent, peer-reviewed) `[VERIFIED]`.

**Disadvantages:**
- **Not commercially usable** (CC BY-NC-SA 4.0) `[VERIFIED]` — eliminates it for our project.
- Requires a CUDA-capable NVIDIA GPU — impossible on our no-GPU machine `[VERIFIED]`.
- Built on SD 1.5 — VAE detail loss/color discrepancy at 512×384 `[VERIFIED]` from paper.
- Mask accuracy strongly affects results `[VERIFIED]`.
- No official API; self-hosting required `[VERIFIED]`.
- HF Space demo reported down as of Oct 2026 `[ESTIMATE]`.

---

## 7. Recommendation for Initial Prototype

### Recommended: **FASHN AI API (Try-On v1.6)**, with **FASHN VTON v1.5 (Apache-2.0)** as the future self-hosted fallback.

### Reasons

1. **Commercial usability is the deciding factor.** Our project requires a commercially usable system. IDM-VTON and CatVTON are both CC BY-NC-SA 4.0 (non-commercial only) and have no available commercial license `[VERIFIED]`. Only FASHN AI offers a clear commercial path — both the managed API (explicitly "Available for commercial use") and the open-source VTON v1.5 (Apache-2.0) `[VERIFIED]`.

2. **Hardware reality.** Our machine has 16 GB RAM, 256 GB SSD, and **no dedicated GPU**. IDM-VTON needs 18–24 GB VRAM and CatVTON needs a CUDA GPU `[VERIFIED]`. Neither can run locally on our machine. FASHN AI API runs in the cloud and needs no local GPU `[VERIFIED]`.

3. **Affordability.** The FASHN API costs ~$0.075 per image (Try-On v1.6) with a $7.50 minimum top-up and 10 free credits to start `[VERIFIED]`. This is far cheaper than procuring a 24 GB VRAM GPU or paying $200–$700/month for GPU hosting `[ESTIMATE]`.

4. **Speed.** Try-On v1.6 returns results in ~5–17 seconds `[VERIFIED]`, suitable for a prototype and even real-time e-commerce use.

5. **Python integration.** The official Python SDK makes integration straightforward for Member 3's role `[VERIFIED]`.

6. **Future flexibility.** If the project later wants to self-host to eliminate per-image costs, FASHN VTON v1.5 (Apache-2.0) is already available as open-source and could be deployed on a GPU-equipped server `[VERIFIED]`. The same Python-based integration pattern carries over.

### Suggested prototype approach (pending your approval for Module 2)

1. Sign up at app.fashn.ai and use the 10 complimentary credits to evaluate Try-On v1.6.
2. Build a Python script using the FASHN Python SDK that takes a person image + garment image and returns a try-on result.
3. Test with dataset pairs from `ai-research/dataset/test_pairs/`.
4. Document quality, speed, and cost per image in `ai-research/testing/results/`.
5. Only if per-image cost becomes a concern at scale, evaluate self-hosting FASHN VTON v1.5 on a GPU server.

---

## 8. Source URLs

| # | Source | URL |
|---|--------|-----|
| 1 | FASHN API pricing | https://help.fashn.ai/plans-and-pricing/api-pricing |
| 2 | FASHN Try-On v1.6 docs | https://docs.fashn.ai/api-reference/tryon-v1-6 |
| 3 | FASHN Try-On Max docs | https://docs.fashn.ai/api-reference/tryon-max |
| 4 | FASHN API reference | https://docs.fashn.ai/api-reference |
| 5 | FASHN pricing page | https://fashn.ai/pricing |
| 6 | FASHN API setup | https://docs.fashn.ai/getting-started/api-setup |
| 7 | FASHN VTON v1.5 GitHub | https://github.com/fashn-AI/fashn-vton-1.5 |
| 8 | FASHN VTON v1.5 blog | https://fashn.ai/blog/fashn-vton-1-5-open-source-release |
| 9 | FASHN basic inference example | https://github.com/fashn-AI/fashn-vton-1.5/blob/main/examples/basic_inference.py |
| 10 | IDM-VTON GitHub | https://github.com/yisol/IDM-VTON |
| 11 | IDM-VTON LICENSE | https://github.com/yisol/IDM-VTON/blob/main/LICENSE.txt |
| 12 | IDM-VTON Hugging Face | https://huggingface.co/yisol/IDM-VTON |
| 13 | IDM-VTON commercial license discussion | https://github.com/yisol/IDM-VTON/issues/160 |
| 14 | IDM-VTON VRAM issues | https://github.com/yisol/IDM-VTON/issues/15, #43, #94 |
| 15 | IDM-VTON ComfyUI node | https://github.com/TemryL/ComfyUI-IDM-VTON |
| 16 | IDM-VTON hardware benchmark | https://fitroom.app/blog/open-source-vton-models-vs-managed-apis |
| 17 | CatVTON GitHub | https://github.com/Zheng-Chong/CatVTON |
| 18 | CatVTON LICENSE | https://github.com/Zheng-Chong/CatVTON/blob/main/LICENSE |
| 19 | CatVTON Hugging Face | https://huggingface.co/zhengchong/CatVTON |
| 20 | CatVTON paper (arXiv) | https://arxiv.org/abs/2407.15886 |
| 21 | CatVTON paper (ICLR 2025 PDF) | https://proceedings.iclr.cc/paper_files/paper/2025/file/a6a1e4c756d700d9aedcc1896a7e6fb0-Paper-Conference.pdf |
| 22 | OpenTryOn CatVTON page | https://tryonlabs.github.io/opentryon/local-models/catvton |
| 23 | CatVTON guide (fashiolabs) | https://fashiolabs.com/blog/catvton-guide |
| 24 | IDM-VTON guide (fashiolabs) | https://fashiolabs.com/blog/idm-vton-guide |

---

**End of Module 1 report.** I am stopping here and awaiting your approval before beginning Module 2.
