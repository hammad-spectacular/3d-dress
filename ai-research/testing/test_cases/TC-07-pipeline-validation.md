# Test Case TC-07: Pipeline Validation (No GPU Required)

**Test Case ID:** TC-07  
**Module:** Task 5 — Testing Without GPU  
**Location:** `ai-research/integration/ai_pipeline.py`  
**Status:** Ready to execute  

## Purpose
Validate the model-independent pipeline logic without requiring GPU or model weights:
- Image validation (format, size, corruption)
- Preprocessing (resize, RGB conversion)
- Error handling (missing files, invalid formats, oversized images)
- Pipeline orchestration (validate → preprocess → infer → postprocess)
- API interface structure

## Test Scenarios

### TC-07.1: Valid Image Validation
| Input | Expected Result |
|-------|----------------|
| Valid JPG image (768×1024) | ImageInfo returned with correct metadata |
| Valid PNG image | ImageInfo returned |
| Valid WEBP image | ImageInfo returned |

### TC-07.2: Invalid Image — File Not Found
| Input | Expected Result |
|-------|----------------|
| Non-existent path | ValidationError raised |

### TC-07.3: Invalid Image — Corrupted File
| Input | Expected Result |
|-------|----------------|
| Corrupted JPG (random bytes) | ValidationError raised |

### TC-07.4: Invalid Image — Unsupported Format
| Input | Expected Result |
|-------|----------------|
| .txt file with image extension | ValidationError raised |

### TC-07.5: Invalid Image — Too Small
| Input | Expected Result |
|-------|----------------|
| 32×32 image | ValidationError raised (min 64×64) |

### TC-07.6: Invalid Image — Too Large
| Input | Expected Result |
|-------|----------------|
| 5000×5000 image | ValidationError raised (max 4096×4096) |

### TC-07.7: Preprocessing — RGB Conversion
| Input | Expected Result |
|-------|----------------|
| Grayscale image | Converted to RGB, 3 channels |
| RGBA image | Converted to RGB, alpha removed |

### TC-07.8: Preprocessing — Resize
| Input | Expected Result |
|-------|----------------|
| 1536×2048 image | Resized to fit within 768×1024, aspect ratio preserved |
| 768×1024 image | No change |

### TC-07.9: Pipeline — No Model Adapter
| Input | Expected Result |
|-------|----------------|
| Pipeline.run() with no adapter | InferenceError raised ("No model adapter configured") |

### TC-07.10: Pipeline — Model Not Loaded
| Input | Expected Result |
|-------|----------------|
| Pipeline.run() with adapter but not loaded | InferenceError raised ("not loaded") |

### TC-07.11: API Interface Structure
| Check | Expected Result |
|-------|-----------------|
| Health check endpoint defined | GET /api/v1/tryon/health |
| Generate endpoint defined | POST /api/v1/tryon/generate |
| Status endpoint defined | GET /api/v1/tryon/status/{job_id} |
| Result endpoint defined | GET /api/v1/tryon/result/{id}.png |
| Error response format defined | JSON with error, message, optional field/details |

### TC-07.12: Kaggle Notebook Structure
| Check | Expected Result |
|-------|-----------------|
| .ipynb file valid JSON | Parses without error |
| HF_TOKEN from environment | Uses os.environ.get("HF_TOKEN") |
| No hardcoded credentials | No token visible in source |
| 12 test pairs defined | Matches test_pairs.json |

## Execution
Run: `python ai-research/testing/test_pipeline.py`

## Expected Output
All 12 test scenarios pass without GPU or model weights.
