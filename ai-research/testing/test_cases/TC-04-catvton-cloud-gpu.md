# Test Case TC-04: CatVTON — Free Cloud GPU Test

**Test Case ID:** TC-04  
**Model:** CatVTON  
**License:** CC BY-NC-SA 4.0 (non-commercial only)  
**Execution Environment:** Free cloud GPU (Google Colab or Kaggle)  
**GPU:** T4 (16GB VRAM)  
**Test Pairs:** P01–P12 (all 12 pairs)  
**Category:** Shirt / tops  
**Expected Runtime:** ~9 seconds per image (reported on A100 at 1024×768); T4 will be slower  
**Memory Required:** <8GB VRAM claimed at 1024×768 (paper Table 3: 4.00GB) — fits within T4 16GB  
**Prerequisites:** Cloud account, PyTorch, diffusers, model weights  
**Status:** Potentially feasible on T4 — VRAM requirement within limits

## Test Procedure

1. Open Google Colab or Kaggle notebook with free T4 GPU
2. Clone https://github.com/Zheng-Chong/CatVTON.git
3. Install dependencies (PyTorch, diffusers)
4. Download model weights (~899M parameters)
5. For each pair P01–P12:
   - Run inference
   - Record processing time
   - Save output image
6. Evaluate each output using the 6 criteria
7. Save all outputs to `ai-research/testing/results/catvton/`

## Feasibility Assessment

- CatVTON claims <8GB VRAM at 1024×768 resolution
- T4 GPU has 16GB VRAM → should fit
- Built on SD 1.5 inpainting, well-supported in diffusers
- **Most likely to be testable on free cloud GPU**

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
