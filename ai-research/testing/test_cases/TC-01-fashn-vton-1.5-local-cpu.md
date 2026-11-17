# Test Case TC-01: FASHN VTON v1.5 — Local CPU Test

**Test Case ID:** TC-01  
**Model:** FASHN VTON v1.5  
**License:** Apache-2.0  
**Execution Environment:** Local machine — CPU only (no GPU)  
**Machine:** 16 GB RAM, 256 GB SSD, no dedicated GPU  
**Test Pairs:** P01–P12 (all 12 pairs from `ai-research/dataset/test_pairs/test_pairs.json`)  
**Category:** Shirt / tops  
**Expected Runtime:** Unknown — CPU inference expected to be slow  
**Memory Required:** ~2GB model weights + system RAM  
**Prerequisites:** Python, fashn-vton package, ~2GB weights download  
**Status:** Not tested

## Test Procedure

1. Clone https://github.com/fashn-AI/fashn-vton-1.5.git
2. Install: `pip install -e .` (CPU: `pip uninstall onnxruntime-gpu && pip install onnxruntime`)
3. Download weights: `python scripts/download_weights.py --weights-dir ./weights` (~2GB)
4. For each pair P01–P12:
   - Run: `python examples/basic_inference.py --weights-dir ./weights --person-image <person> --garment-image <garment> --category tops --output-dir ./outputs/`
   - Record processing time
   - Save output image
5. Evaluate each output using the 6 criteria in the test case definitions
6. Save all outputs to `ai-research/testing/results/fashn-vton-1.5/`

## Feasibility Assessment

- Model can technically run on CPU (weights converted to float32)
- No dedicated GPU → inference will be slow
- 16GB RAM may be sufficient but unconfirmed
- **Cannot confirm without actual testing**

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
