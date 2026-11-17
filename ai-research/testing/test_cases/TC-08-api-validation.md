# Test Case TC-08: API Interface Validation (No GPU Required)

**Test Case ID:** TC-08  
**Module:** Task 3 — Backend Integration  
**Location:** `ai-research/integration/api_interface.md`  
**Status:** Ready to execute  

## Purpose
Validate the backend API interface definition for correctness and completeness.

## API Endpoints to Validate

| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/v1/tryon/health` | GET | Health check, model status | Defined |
| `/api/v1/tryon/generate` | POST | Start try-on generation | Defined |
| `/api/v1/tryon/status/{job_id}` | GET | Check generation status | Defined |
| `/api/v1/tryon/result/{id}.png` | GET | Download result image | Defined |
| `/api/v1/tryon/job/{job_id}` | DELETE | Cancel generation | Defined |

## Request/Response Validation

### Generate Request Parameters
| Parameter | Type | Required | Default | Validated |
|-----------|------|----------|---------|-----------|
| person_image | file | Yes | — | File format, size, dimensions |
| garment_image | file | Yes | — | File format, size, dimensions |
| category | string | No | "tops" | tops/bottoms/one-pieces |
| num_samples | integer | No | 1 | 1-4 |
| num_timesteps | integer | No | 30 | 20-50 |
| guidance_scale | float | No | 1.5 | 1.0-3.0 |
| seed | integer | No | 42 | Any integer |

## Error Response Validation

| Error Code | HTTP Status | Scenario |
|------------|-------------|----------|
| validation_failed | 400 | Invalid input image or parameter |
| model_not_loaded | 503 | Model weights unavailable |
| inference_failed | 500 | Model crashed during generation |
| job_not_found | 404 | Invalid job ID |
| internal_error | 500 | Unexpected server error |

## Integration Readiness Checklist

- [ ] Health endpoint returns model name, version, loaded status, device
- [ ] Generate endpoint accepts multipart/form-data image upload
- [ ] Generate returns job_id for async polling
- [ ] Status endpoint returns progress (0-100) and status
- [ ] Result endpoint serves PNG image binary
- [ ] All error responses follow consistent JSON format
- [ ] No API keys or secrets in client-facing responses
