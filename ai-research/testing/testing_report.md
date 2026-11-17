# AI Virtual Try-On — Module 3: Testing Report

**Project:** AI Virtual Try-On (Member 3 — AI & Computer Vision Developer)  
**Module:** 3 — AI Model Testing  
**Workspace:** `ai-research/testing/`  
**Project use:** Personal use and experimentation only (non-commercial)  
**Machine:** 16 GB RAM, 256 GB SSD, no dedicated GPU assumed  

---

## 1. Executive Summary

| Field | Value |
|-------|-------|
| **Test Date** | |
| **Tester** | |
| **Machine** | 16 GB RAM, 256 GB SSD, no dedicated GPU |
| **Test Pairs Used** | 12 pairs (P01–P12) from `ai-research/dataset/test_pairs/test_pairs.json` |
| **Dataset** | VITON-HD test split (CC BY-NC 4.0) |
| **Models Tested** | |
| **Models Not Tested** | |
| **Best Performing Model** | |
| **Recommended Model for Prototype** | |

---

## 2. Model Testing Summary

| Model | License | Test Environment | Tested? | Overall Score (1–5) | Processing Time | VRAM Required | Commercial Use |
|-------|---------|-----------------|---------|---------------------|-----------------|---------------|----------------|
| FASHN VTON v1.5 | Apache-2.0 | | | | | | ✅ Yes |
| IDM-VTON | CC BY-NC-SA 4.0 | | | | | >18GB | ❌ No |
| CatVTON | CC BY-NC-SA 4.0 | | | | | <8GB | ❌ No |

---

## 3. Detailed Results by Model

### 3.1 FASHN VTON v1.5

| Field | Value |
|-------|-------|
| **Test Case** | TC-01 (local CPU) / TC-02 (cloud GPU) |
| **Environment** | |
| **Tested?** | Yes / No |
| **Pairs Completed** | X / 12 |
| **Pairs Failed** | X / 12 |
| **Average Processing Time** | X seconds per image |
| **Overall Score** | X / 5 |

#### Per-Pair Results

| Pair ID | Person | Clothing | Realism | Detail | Alignment | Quality | Speed | Reliability | Overall | Notes |
|---------|--------|----------|---------|--------|-----------|---------|-------|-------------|---------|-------|
| P01 | 00891_00.jpg | 01260_00.jpg | | | | | | | | |
| P02 | 03615_00.jpg | 01430_00.jpg | | | | | | | | |
| P03 | 07445_00.jpg | 02783_00.jpg | | | | | | | | |
| P04 | 07573_00.jpg | 03751_00.jpg | | | | | | | | |
| P05 | 08909_00.jpg | 06429_00.jpg | | | | | | | | |
| P06 | 10549_00.jpg | 06802_00.jpg | | | | | | | | |
| P07 | 00891_00.jpg | 07429_00.jpg | | | | | | | | |
| P08 | 03615_00.jpg | 08348_00.jpg | | | | | | | | |
| P09 | 07445_00.jpg | 09933_00.jpg | | | | | | | | |
| P10 | 07573_00.jpg | 11028_00.jpg | | | | | | | | |
| P11 | 08909_00.jpg | 11351_00.jpg | | | | | | | | |
| P12 | 10549_00.jpg | 11791_00.jpg | | | | | | | | |

#### Output Files

| Pair ID | Output File Path |
|---------|-----------------|
| P01 | `ai-research/testing/results/fashn-vton-1.5/P01_output.png` |
| ... | |

#### Notes

---

### 3.2 IDM-VTON

| Field | Value |
|-------|-------|
| **Test Case** | TC-03 (cloud GPU) / TC-05 (local CPU — skipped) |
| **Environment** | |
| **Tested?** | Yes / No / Skipped |
| **Reason if not tested** | |
| **Pairs Completed** | X / 12 |
| **Pairs Failed** | X / 12 |
| **Average Processing Time** | X seconds per image |
| **Overall Score** | X / 5 |
| **VRAM Issues** | Yes / No (describe) |

#### Per-Pair Results

| Pair ID | Realism | Detail | Alignment | Quality | Speed | Reliability | Overall | Notes |
|---------|---------|--------|-----------|---------|-------|-------------|---------|-------|
| P01 | | | | | | | | |
| ... | | | | | | | | |

#### Output Files

| Pair ID | Output File Path |
|---------|-----------------|
| ... | |

#### Notes

---

### 3.3 CatVTON

| Field | Value |
|-------|-------|
| **Test Case** | TC-04 (cloud GPU) / TC-06 (local CPU — skipped) |
| **Environment** | |
| **Tested?** | Yes / No / Skipped |
| **Reason if not tested** | |
| **Pairs Completed** | X / 12 |
| **Pairs Failed** | X / 12 |
| **Average Processing Time** | X seconds per image |
| **Overall Score** | X / 5 |
| **VRAM Issues** | Yes / No (describe) |

#### Per-Pair Results

| Pair ID | Realism | Detail | Alignment | Quality | Speed | Reliability | Overall | Notes |
|---------|---------|--------|-----------|---------|-------|-------------|---------|-------|
| P01 | | | | | | | | |
| ... | | | | | | | | |

#### Output Files

| Pair ID | Output File Path |
|---------|-----------------|
| ... | |

#### Notes

---

## 4. Model Comparison

| Criterion | FASHN VTON v1.5 | IDM-VTON | CatVTON |
|-----------|-----------------|----------|---------|
| License | Apache-2.0 | CC BY-NC-SA 4.0 | CC BY-NC-SA 4.0 |
| Commercial Use | ✅ Yes | ❌ No | ❌ No |
| Local Machine (No GPU) | ⚠️ CPU possible, slow | ❌ No | ❌ No |
| Free Cloud GPU (T4 16GB) | ✅ Feasible | ❌ VRAM exceeded | ✅ Feasible |
| Processing Time | X s | X s | X s |
| Realism Score | X / 5 | X / 5 | X / 5 |
| Detail Preservation Score | X / 5 | X / 5 | X / 5 |
| Body Alignment Score | X / 5 | X / 5 | X / 5 |
| Image Quality Score | X / 5 | X / 5 | X / 5 |
| Reliability Score | X / 5 | X / 5 | X / 5 |
| Overall Score | X / 5 | X / 5 | X / 5 |

---

## 5. Models That Can Be Tested for Free

| Model | Can Test Locally? | Can Test on Free Cloud GPU? | License Restriction | Verdict |
|-------|-------------------|----------------------------|---------------------|---------|
| FASHN VTON v1.5 | ⚠️ CPU (slow) | ✅ Yes | None (Apache-2.0) | **Recommended** |
| IDM-VTON | ❌ No | ❌ No (>18GB VRAM) | Non-commercial only | Not testable |
| CatVTON | ❌ No | ✅ Yes | Non-commercial only | **Alternative** |

---

## 6. Recommendation for Prototype (Milestone 4)

| Field | Value |
|-------|-------|
| **Recommended Model** | |
| **Reason** | |
| **Test Environment** | |
| **Expected Processing Time** | |
| **License Compatibility** | |

---

## 7. Issues and Limitations

| Issue | Description | Impact | Mitigation |
|-------|-------------|--------|------------|
| No dedicated GPU | Local machine cannot run IDM-VTON or CatVTON | Limits local testing | Use free cloud GPU |
| Limited dataset | Only 6 person + 12 clothing images, shirts only | Limited test coverage | Accept for initial prototype |
| CPU inference slow | FASHN VTON v1.5 on CPU will be slow | Long processing times | Use cloud GPU |
| T4 VRAM limit | IDM-VTON needs >18GB VRAM, T4 has 16GB | Cannot test IDM-VTON | Skip IDM-VTON |

---

## 8. Sign-off

**Important:** Do not claim a model has been tested unless actual inference has been performed and outputs are saved in `ai-research/testing/results/`.

| Role | Name | Signature | Date |
|------|------|-----------|------|
| AI & CV Developer (Member 3) | | | |

---

## 8. Pipeline Testing Results (No GPU Required)

**Test Date:** November 17, 2026  
**Test Script:** `ai-research/testing/test_pipeline.py`  
**GPU Required:** No  
**Model Weights Required:** No  

### 8.1 Test Results Summary

| Metric | Value |
|--------|-------|
| Total test scenarios | 24 |
| Passed | 24 |
| Failed | 0 |
| GPU required | No |
| Model weights required | No |

### 8.2 Test Coverage

| Test Area | Scenarios | Status |
|-----------|-----------|--------|
| Image validation (valid images) | 3 | ✅ Passed |
| Image validation (file not found) | 1 | ✅ Passed |
| Image validation (corrupted file) | 1 | ✅ Passed |
| Image validation (unsupported format) | 1 | ✅ Passed |
| Image validation (too small) | 1 | ✅ Passed |
| Preprocessing (RGB conversion) | 1 | ✅ Passed |
| Preprocessing (resize large image) | 1 | ✅ Passed |
| Preprocessing (aspect ratio) | 1 | ✅ Passed |
| Pipeline (no model adapter) | 1 | ✅ Passed |
| Pipeline (request/result structure) | 2 | ✅ Passed |
| API interface structure | 5 | ✅ Passed |
| Kaggle notebook structure | 4 | ✅ Passed |

### 8.3 What Is Functional (No GPU)

| Component | Status | Notes |
|-----------|--------|-------|
| Image validation | ✅ Functional | Validates format, size, corruption, dimensions |
| Image preprocessing | ✅ Functional | RGB conversion, resize, aspect ratio preservation |
| Pipeline orchestration | ✅ Functional | Validate → preprocess → infer → postprocess flow |
| Error handling | ✅ Functional | ValidationError, PreprocessingError, InferenceError, PostprocessingError |
| API interface definition | ✅ Defined | REST endpoints documented in api_interface.md |
| Kaggle notebook | ✅ Defined | Ready to execute on Kaggle T4 GPU |

### 8.4 What Requires GPU Access

| Component | Status | Required For |
|-----------|--------|--------------|
| FASHN VTON v1.5 inference | ⏸️ Blocked | Model weights (~2 GB) + GPU (8GB VRAM recommended) |
| IDM-VTON inference | ⏸️ Blocked | Model weights + GPU (>18GB VRAM) |
| CatVTON inference | ⏸️ Blocked | Model weights + GPU (<8GB VRAM claimed) |

---

## 9. Next Steps (Pending Approval)

1. Obtain Hugging Face access token or Kaggle GPU access (phone verification pending)
2. Run Kaggle notebook (`ai-research/prototype/kaggle_fashn_vton.ipynb`) for actual inference
3. Generate first try-on image using FASHN VTON v1.5 on cloud GPU
4. Proceed to Milestone 4: First Successful AI Try-On
5. Build the working prototype application

