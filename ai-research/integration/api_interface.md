# AI Virtual Try-On — Backend Integration Interface

**Project:** AI Virtual Try-On (Member 3 — AI & Computer Vision Developer)  
**Module:** Task 3 — Backend Integration  
**Location:** `ai-research/integration/api_interface.md`  
**Status:** Ready for integration  

---

## Overview

This document defines the clean interface between the AI Virtual Try-On module
and the rest of the application (frontend + backend developed by other team members).

The AI module is **independent** — it exposes a simple REST-like API that other
teams can call without needing to understand PyTorch, model weights, or GPU
management.

---

## Design Principles

1. **Independence:** AI module can be developed, tested, and deployed separately.
2. **Simplicity:** JSON over HTTP, image upload via multipart/form-data.
3. **Asynchronous:** Try-on generation can take seconds to minutes — status polling supported.
4. **Error handling:** Consistent error responses with HTTP status codes and messages.
5. **No secrets in client:** API keys / HF tokens live server-side only.

---

## Base URL

```
http://<ai-server-host>:<port>/api/v1/tryon
```

---

## Endpoints

### 1. Health Check

```
GET /api/v1/tryon/health
```

Check if the AI service is running and whether the model is loaded.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "model": {
    "name": "FASHN VTON v1.5",
    "version": "1.5.0",
    "loaded": true,
    "device": "cuda",
    "supported_categories": ["tops", "bottoms", "one-pieces"]
  },
  "gpu_available": true,
  "version": "1.0.0"
}
```

**Response (503 Service Unavailable — model not loaded):**
```json
{
  "status": "unhealthy",
  "model": {
    "name": "FASHN VTON v1.5",
    "version": "1.5.0",
    "loaded": false,
    "device": null,
    "supported_categories": ["tops", "bottoms", "one-pieces"]
  },
  "gpu_available": false,
  "error": "Model weights not found on server",
  "version": "1.0.0"
}
```

---

### 2. Start Try-On Generation

```
POST /api/v1/tryon/generate
```

**Content-Type:** `multipart/form-data`

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `person_image` | file | Yes | Photo of the person (JPG, PNG, WEBP) |
| `garment_image` | file | Yes | Photo of the clothing (JPG, PNG, WEBP) |
| `category` | string | No | `"tops"`, `"bottoms"`, `"one-pieces"`. Default: `"tops"` |
| `num_samples` | integer | No | Number of outputs (1-4). Default: `1` |
| `num_timesteps` | integer | No | Diffusion steps (20-50). Default: `30` |
| `guidance_scale` | float | No | CFG strength (1.0-3.0). Default: `1.5` |
| `seed` | integer | No | Random seed for reproducibility. Default: `42` |

**Response (202 Accepted — generation started):**
```json
{
  "job_id": "tryon_abc123def456",
  "status": "queued",
  "message": "Try-on generation started",
  "estimated_seconds": 30
}
```

**Response (400 Bad Request — validation error):**
```json
{
  "error": "validation_failed",
  "message": "Person image is corrupted or unsupported format",
  "field": "person_image"
}
```

**Response (503 Service Unavailable — model not loaded):**
```json
{
  "error": "model_not_loaded",
  "message": "AI model weights are not available on this server",
  "details": "Download weights and restart the AI service"
}
```

---

### 3. Check Generation Status

```
GET /api/v1/tryon/status/{job_id}
```

**Response (200 OK — processing):**
```json
{
  "job_id": "tryon_abc123def456",
  "status": "processing",
  "progress": 45,
  "message": "Running inference (15/30 steps)"
}
```

**Response (200 OK — completed):**
```json
{
  "job_id": "tryon_abc123def456",
  "status": "completed",
  "progress": 100,
  "output_images": [
    "/api/v1/tryon/result/tryon_abc123def456_00.png"
  ],
  "processing_time_seconds": 23.4,
  "model": "FASHN VTON v1.5"
}
```

**Response (200 OK — failed):**
```json
{
  "job_id": "tryon_abc123def456",
  "status": "failed",
  "progress": 0,
  "error": "inference_failed",
  "message": "Model ran out of memory during sampling"
}
```

**Response (404 Not Found — invalid job_id):**
```json
{
  "error": "job_not_found",
  "message": "No try-on job found with ID: tryon_abc123def456"
}
```

---

### 4. Retrieve Generated Image

```
GET /api/v1/tryon/result/{job_id}_{index}.png
```

Where `{index}` is the sample number (00, 01, 02, 03).

**Response (200 OK):** Image binary (PNG)

**Response (404 Not Found):** Image not ready or job not found.

---

### 5. Cancel Generation

```
DELETE /api/v1/tryon/job/{job_id}
```

**Response (200 OK):**
```json
{
  "job_id": "tryon_abc123def456",
  "status": "cancelled"
}
```

---

## Error Response Format

All errors follow this structure:

```json
{
  "error": "<error_code>",
  "message": "<human_readable_message>",
  "field": "<optional_field_name>",
  "details": "<optional_technical_details>"
}
```

**Common error codes:**

| Code | HTTP Status | Meaning |
|------|-------------|---------|
| `validation_failed` | 400 | Input image or parameter invalid |
| `model_not_loaded` | 503 | AI model weights not available |
| `inference_failed` | 500 | Model crashed during generation |
| `job_not_found` | 404 | Invalid job ID |
| `internal_error` | 500 | Unexpected server error |

---

## Input / Output Formats

### Input Images
- **Formats:** JPEG, PNG, WEBP, BMP
- **Max size:** 50 MB per image
- **Min dimensions:** 64×64 pixels
- **Max dimensions:** 4096×4096 pixels
- **Color mode:** Auto-converted to RGB server-side

### Output Images
- **Format:** PNG
- **Naming:** `{job_id}_{index:02d}.png`
- **Dimensions:** Same aspect ratio as input, resized to fit 768×1024

---

## Integration Example (Python)

```python
import requests

# 1. Start generation
with open("person.jpg", "rb") as p, open("shirt.jpg", "rb") as g:
    response = requests.post(
        "http://ai-server:8000/api/v1/tryon/generate",
        files={"person_image": p, "garment_image": g},
        data={"category": "tops", "num_samples": 1}
    )
job = response.json()
job_id = job["job_id"]

# 2. Poll status
import time
while True:
    status = requests.get(f"http://ai-server:8000/api/v1/tryon/status/{job_id}").json()
    if status["status"] == "completed":
        break
    if status["status"] == "failed":
        raise RuntimeError(status["message"])
    time.sleep(2)

# 3. Download result
result_url = f"http://ai-server:8000{status['output_images'][0]}"
img_data = requests.get(result_url).content
with open("result.png", "wb") as f:
    f.write(img_data)
```

---

## Deployment Requirements

| Requirement | Specification |
|-------------|---------------|
| Python | 3.10+ |
| PyTorch | 2.0+ (CPU or CUDA) |
| GPU | Optional (CPU works but slow) |
| VRAM (GPU) | 8 GB+ recommended for FASHN VTON v1.5 |
| Disk space | 3 GB+ (model weights + runtime) |
| Memory | 8 GB+ RAM |

---

## Integration Checklist for Other Teams

- [ ] AI service health endpoint reachable
- [ ] Image upload (multipart/form-data) working
- [ ] Job ID returned and status polling functional
- [ ] Result image downloadable via `/result/` endpoint
- [ ] Error responses handled gracefully in frontend
- [ ] Loading/progress UI implemented for inference wait time

---

## Future Extensions

- Batch try-on (multiple garments in one request)
- Webhook notifications on completion
- Result image expiration/cleanup policy
- Rate limiting per user/IP
- Analytics: success rate, average processing time
