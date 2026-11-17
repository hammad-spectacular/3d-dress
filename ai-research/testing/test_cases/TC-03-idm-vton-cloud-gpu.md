# Test Case TC-03: IDM-VTON — Free Cloud GPU Test

**Test Case ID:** TC-03  
**Model:** IDM-VTON  
**License:** CC BY-NC-SA 4.0 (non-commercial only)  
**Execution Environment:** Free cloud GPU (Google Colab or Kaggle)  
**GPU:** T4 (16GB VRAM)  
**Test Pairs:** P01–P12 (all 12 pairs)  
**Category:** Shirt / tops  
**Expected Runtime:** ~13–17 seconds per image (reported on A100/RTX 4090); T4 likely slower or may fail  
**Memory Required:** >18GB VRAM (author statement) — **exceeds T4 16GB VRAM**  
**Prerequisites:** Cloud account, conda, PyTorch 2.0.1 + CUDA 11.8, model weights  
**Status:** Likely not feasible — VRAM requirement exceeds available GPU memory

## Test Procedure (if attempted)

1. Open Google Colab or Kaggle notebook with free T4 GPU
2. Clone https://github.com/yisol/IDM-VTON.git
3. Create conda environment with PyTorch 2.0.1 + CUDA 11.8
4. Download model weights
5. Run inference on test pairs
6. Record processing time, output quality, VRAM usage, and any OOM errors

## Feasibility Assessment

- IDM-VTON requires >18GB VRAM per author statement (GitHub issue #43)
- T4 GPU has only 16GB VRAM → **likely will fail with out-of-memory errors**
- Community workaround: 8GB VRAM with 4-bit precision + CPU offloading (unofficial, not verified)
- **Likely not testable on free cloud GPU tiers** due to VRAM limitation

## Evaluation Criteria Scores (to be filled after testing)

| Criterion | Score (1–5) | Notes |
|-----------|-------------|-------|
| Realism | | |
| Clothing Detail Preservation | | |
| Body Alignment | | |
| Image Quality | | |
| Processing Time | | |
| Reliability | | |
| **Overall** | | |

**Overall Score:** (sum of 6 criteria) / 6

**Note:** If out-of-memory errors occur, mark Reliability = 1 and note the error.
