# AI Virtual Try-On — Module 3: Test Case Definitions

**Project:** AI Virtual Try-On (Member 3 — AI & Computer Vision Developer)  
**Module:** 3 — AI Model Testing Preparation  
**Workspace:** `ai-research/testing/test_cases/`  
**Project use:** Personal use and experimentation only (non-commercial)  
**Budget:** Zero — no purchases, no subscriptions, no API credits  
**Machine:** 16 GB RAM, 256 GB SSD, no dedicated GPU assumed  

---

## 1. Test Data Source

All test cases use the 12 test pairs defined in `ai-research/dataset/test_pairs/test_pairs.json`:

| Pair ID | Person Image | Clothing Image | Category | Pair Type |
|---------|-------------|----------------|----------|-----------|
| P01 | 00891_00.jpg | 01260_00.jpg | Shirt | Standard |
| P02 | 03615_00.jpg | 01430_00.jpg | Shirt | Standard |
| P03 | 07445_00.jpg | 02783_00.jpg | Shirt | Standard |
| P04 | 07573_00.jpg | 03751_00.jpg | Shirt | Standard |
| P05 | 08909_00.jpg | 06429_00.jpg | Shirt | Standard |
| P06 | 10549_00.jpg | 06802_00.jpg | Shirt | Standard |
| P07 | 00891_00.jpg | 07429_00.jpg | Shirt | Cross-pair |
| P08 | 03615_00.jpg | 08348_00.jpg | Shirt | Cross-pair |
| P09 | 07445_00.jpg | 09933_00.jpg | Shirt | Cross-pair |
| P10 | 07573_00.jpg | 11028_00.jpg | Shirt | Cross-pair |
| P11 | 08909_00.jpg | 11351_00.jpg | Shirt | Cross-pair |
| P12 | 10549_00.jpg | 11791_00.jpg | Shirt | Cross-pair |

**Dataset:** VITON-HD test split (CC BY-NC 4.0)  
**Image format:** JPEG, 768×1024, RGB  
**Location:** `ai-research/dataset/people/` and `ai-research/dataset/clothing/`

---

## 2. Evaluation Criteria

Each model will be evaluated on the following criteria. Each criterion is scored 1–5 (1 = poor, 5 = excellent).

| Criterion | Description | Score (1–5) |
|-----------|-------------|-------------|
| **Realism** | Does the output look like a real photograph? Are lighting, shadows, and skin textures natural? | |
| **Clothing Detail Preservation** | Are patterns, logos, colors, and fabric textures of the clothing preserved accurately? | |
| **Body Alignment** | Is the clothing properly aligned with the person's body? No floating garments, wrong positioning, or distorted anatomy? | |
| **Image Quality** | Is the output sharp and clear? No blurriness, artifacts, or compression issues? | |
| **Processing Time** | How long does inference take per image? (measured in seconds) | |
| **Reliability** | Does the model produce consistent results? No crashes, errors, or failed generations? | |

**Overall Score:** Average of all 6 criteria.

---

## 3. Test Case Definitions

### Test Case TC-01: FASHN VTON v1.5 — Local CPU Test

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-01 |
| **Model** | FASHN VTON v1.5 |
| **License** | Apache-2.0 |
| **Execution Environment** | Local machine — CPU only (no GPU) |
| **Test Pairs** | P01–P12 (all 12 pairs) |
| **Category** | Shirt / tops |
| **Expected Runtime** | Unknown — CPU inference expected to be slow |
| **Memory Required** | ~2GB model weights + system RAM (16GB available) |
| **Prerequisites** | Python, fashn-vton package, ~2GB weights download |
| **Status** | Not tested — CPU-only feasibility not yet confirmed |

**Test Procedure:**
1. Clone fashn-vton-1.5 repository
2. Install with `pip install -e .` (CPU: `onnxruntime` instead of `onnxruntime-gpu`)
3. Download weights (~2GB) via `scripts/download_weights.py`
4. Run inference on each of the 12 test pairs
5. Record processing time, output quality, and any errors
6. Save outputs to `ai-research/testing/results/fashn-vton-1.5/`

**Feasibility Assessment:**
- The model can technically run on CPU (weights converted to float32)
- No dedicated GPU on our machine → inference will be slow
- 16GB RAM may be sufficient for CPU inference but unconfirmed
- **Cannot confirm feasibility without actual testing** (installation and download required, which is deferred pending approval)

---

### Test Case TC-02: FASHN VTON v1.5 — Free Cloud GPU Test

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-02 |
| **Model** | FASHN VTON v1.5 |
| **License** | Apache-2.0 |
| **Execution Environment** | Free cloud GPU (Google Colab or Kaggle) |
| **GPU** | T4 (16GB VRAM) |
| **Test Pairs** | P01–P12 (all 12 pairs) |
| **Category** | Shirt / tops |
| **Expected Runtime** | ~5 seconds per image (reported on H100; T4 will be slower) |
| **Memory Required** | ~8GB VRAM (reported) — fits within T4 16GB |
| **Prerequisites** | Cloud account, fashn-vton package, ~2GB weights download |
| **Status** | Not tested |

**Test Procedure:**
1. Open Google Colab or Kaggle notebook with free T4 GPU
2. Clone fashn-vton-1.5 repository
3. Install dependencies (`pip install -e .`)
4. Download weights (~2GB)
5. Run inference on each of the 12 test pairs
6. Record processing time, output quality, and any errors
7. Save outputs to `ai-research/testing/results/fashn-vton-1.5-cloud/`

**Free Tier Limits:**
- Google Colab: 12–30 GPU hours/week, 12-hour session limit
- Kaggle: 30 GPU hours/week guaranteed, 12-hour session limit, phone verification required

---

### Test Case TC-03: IDM-VTON — Free Cloud GPU Test

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-03 |
| **Model** | IDM-VTON |
| **License** | CC BY-NC-SA 4.0 (non-commercial only) |
| **Execution Environment** | Free cloud GPU (Google Colab or Kaggle) |
| **GPU** | T4 (16GB VRAM) |
| **Test Pairs** | P01–P12 (all 12 pairs) |
| **Category** | Shirt / tops |
| **Expected Runtime** | ~13–17 seconds per image (reported on A100/R4090); T4 likely slower or may fail |
| **Memory Required** | >18GB VRAM (author statement) — **exceeds T4 16GB VRAM** |
| **Prerequisites** | Cloud account, conda, PyTorch 2.0.1 + CUDA 11.8, model weights |
| **Status** | Likely not feasible on T4 — VRAM requirement exceeds available GPU memory |

**Test Procedure (if attempted):**
1. Open Google Colab or Kaggle notebook with free T4 GPU
2. Clone IDM-VTON repository
3. Create conda environment with PyTorch 2.0.1 + CUDA 11.8
4. Download model weights
5. Run inference on test pairs
6. Record processing time, output quality, VRAM usage, and any OOM errors

**Feasibility Assessment:**
- IDM-VTON requires >18GB VRAM per author statement
- T4 GPU has only 16GB VRAM → **likely will fail with out-of-memory errors**
- Community workaround: 8GB VRAM with 4-bit precision + CPU offloading (unofficial, not tested)
- **Likely not testable on free cloud GPU tiers** due to VRAM limitation

---

### Test Case TC-04: CatVTON — Free Cloud GPU Test

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-04 |
| **Model** | CatVTON |
| **License** | CC BY-NC-SA 4.0 (non-commercial only) |
| **Execution Environment** | Free cloud GPU (Google Colab or Kaggle) |
| **GPU** | T4 (16GB VRAM) |
| **Test Pairs** | P01–P12 (all 12 pairs) |
| **Category** | Shirt / tops |
| **Expected Runtime** | ~9 seconds per image (reported on A100 at 1024×768); T4 will be slower |
| **Memory Required** | <8GB VRAM claimed at 1024×768 (paper Table 3: 4.00GB) — fits within T4 16GB |
| **Prerequisites** | Cloud account, PyTorch, diffusers, model weights |
| **Status** | Potentially feasible on T4 — VRAM requirement within limits |

**Test Procedure:**
1. Open Google Colab or Kaggle notebook with free T4 GPU
2. Clone CatVTON repository
3. Install dependencies (PyTorch, diffusers)
4. Download model weights (~899M parameters)
5. Run inference on each of the 12 test pairs
6. Record processing time, output quality, and any errors
7. Save outputs to `ai-research/testing/results/catvton/`

**Feasibility Assessment:**
- CatVTON claims <8GB VRAM at 1024×768 resolution
- T4 GPU has 16GB VRAM → should fit
- Built on SD 1.5 inpainting, well-supported in diffusers
- **Most likely to be testable on free cloud GPU**

---

### Test Case TC-05: IDM-VTON — Local Machine Test

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-05 |
| **Model** | IDM-VTON |
| **License** | CC BY-NC-SA 4.0 (non-commercial only) |
| **Execution Environment** | Local machine — CPU only (no GPU) |
| **Test Pairs** | P01–P12 |
| **Category** | Shirt / tops |
| **Expected Runtime** | Not feasible — no GPU, model requires CUDA |
| **Memory Required** | >18GB VRAM — not available on local machine |
| **Status** | Not feasible — no dedicated GPU on local machine |

**Feasibility Assessment:**
- IDM-VTON requires CUDA-capable NVIDIA GPU
- Local machine has no dedicated GPU
- **Cannot test locally**

---

### Test Case TC-06: CatVTON — Local Machine Test

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-06 |
| **Model** | CatVTON |
| **License** | CC BY-NC-SA 4.0 (non-commercial only) |
| **Execution Environment** | Local machine — CPU only (no GPU) |
| **Test Pairs** | P01–P12 |
| **Category** | Shirt / tops |
| **Expected Runtime** | Not feasible — no GPU, model requires CUDA |
| **Memory Required** | <8GB VRAM claimed — but still requires CUDA GPU |
| **Status** | Not feasible — no dedicated GPU on local machine |

**Feasibility Assessment:**
- CatVTON requires CUDA-capable NVIDIAGPU
- Local machine has no dedicated GPU
- **Cannot test locally**

---

## 4. Models That Can Actually Be Tested for Free

| Model | License | Local Machine (No GPU) | Free Cloud GPU (T4, 16GB VRAM) | Verdict |
|-------|---------|------------------------|---------------------------------|---------|
| **FASHN VTON v1.5** | Apache-2.0 | ⚠️ Technically possible (CPU, float32, very slow) | ✅ Feasible (~8GB VRAM < 16GB T4) | **Best candidate for free testing** |
| **IDM-VTON** | CC BY-NC-SA 4.0 | ❌ No (requires CUDA GPU) | ❌ No (>18GB VRAM > 16GB T4) | Not testable on available free hardware |
| **CatVTON** | CC BY-NC-SA 4.0 | ❌ No (requires CUDA GPU) | ✅ Feasible (<8GB VRAM < 16GB T4) | **Second candidate for free testing** |

### Recommended Testing Order

1. **FASHN VTON v1.5 on free cloud GPU** (TC-02) — Apache-2.0 license, fits T4 VRAM, fastest path to a working try-on
2. **CatVTON on free cloud GPU** (TC-04) — CC BY-NC-SA 4.0 (non-commercial, OK for personal use), fits T4 VRAM
3. **FASHN VTON v1.5 on local CPU** (TC-01) — If cloud testing is not possible, attempt local CPU as fallback
4. **IDM-VTON** — Not testable on available free hardware (VRAM requirement exceeds T4 16GB)

---

## 5. Output Directory Structure

```
ai-research/testing/
├── test_cases/
│   ├── TC-01-fashn-vton-1.5-local-cpu.md
│   ├── TC-02-fashn-vton-1.5-cloud-gpu.md
│   ├── TC-03-idm-vton-cloud-gpu.md
│   ├── TC-04-catvton-cloud-gpu.md
│   ├── TC-05-idm-vton-local-cpu.md
│   └── TC-06-catvton-local-cpu.md
├── results/
│   ├── fashn-vton-1.5/
│   ├── catvton/
│   └── idm-vton/
└── testing_report.md
```

---

## 6. Important Notes

- **No model has been tested yet.** This document only defines test cases and feasibility.
- **Actual testing requires installation and inference**, which is deferred pending your approval for Module 3 execution.
- **Do not claim a model works** unless actual inference has been performed and outputs are saved in `ai-research/testing/results/`.
- All models evaluated are free to use for personal/non-commercial purposes.
- IDM-VTON and CatVTON are CC BY-NC-SA 4.0 — acceptable for personal use, not for commercial products.
