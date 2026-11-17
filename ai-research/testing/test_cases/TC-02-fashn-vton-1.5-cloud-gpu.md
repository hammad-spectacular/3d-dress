# Test Case TC-02: FASHN VTON v1.5 — Free Cloud GPU Test

**Test Case ID:** TC-02  
**Model:** FASHN VTON v1.5  
**License:** Apache-2.0  
**Execution Environment:** Free cloud GPU (Google Colab or Kaggle)  
**GPU:** T4 (16GB VRAM)  
**Test Pairs:** P01–P12 (all 12 pairs)  
**Category:** Shirt / tops  
**Expected Runtime:** ~5 seconds per image (reported on H100; T4 will be slower)  
**Memory Required:** ~8GB VRAM (reported) — fits within T4 16GB  
**Prerequisites:** Cloud account, fashn-vton package, ~2GB weights download  
**Status:** Not tested

## Test Procedure

1. Open Google Colab (colab.research.google.com) or Kaggle (kaggle.com/code) with free T4 GPU
2. Clone https://github.com/fashn-AI/fashn-vton-1.5.git
3. Install: `pip install -e .`
4. Download weights: `python scripts/download_weights.py --weights-dir ./weights` (~2GB)
5. For each pair P01–P12:
   - Run inference
   - Record processing time
   - Save output image
6. Evaluate each output using the 6 criteria
7. Save all outputs to `ai-research/testing/results/fashn-vton-1.5-cloud/`

## Free Tier Limits

- **Google Colab:** 12–30 GPU hours/week, 12-hour session limit, no credit card
- **Kaggle:** 30 GPU hours/week guaranteed, 12-hour session limit, phone verification required

## Feasibility Assessment

- ~8GB VRAM requirement < 16GB T4 VRAM → should fit
- Apache-2.0 license → no restrictions for personal use
- **Most viable path to a working try-on**

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
