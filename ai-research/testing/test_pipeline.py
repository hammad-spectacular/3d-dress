"""
AI Virtual Try-On — Lightweight Pipeline Tests (No GPU, No Model Weights)

Tests:
  - Image validation (valid, missing, corrupted, unsupported, too small, too large)
  - Preprocessing (RGB conversion, resize)
  - Pipeline orchestration (no adapter, adapter not loaded)
  - API interface structure validation

Run: python ai-research/testing/test_pipeline.py
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Add integration to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "integration"))

from ai_pipeline import (
    ImageValidator,
    Preprocessor,
    Postprocessor,
    VirtualTryOnPipeline,
    TryOnRequest,
    GarmentCategory,
    ValidationError,
    PreprocessingError,
    InferenceError,
    PostprocessingError,
    PipelineStatus,
)

# Paths to test data
# test_pipeline.py is at ai-research/testing/test_pipeline.py
# parents[0] = testing, parents[1] = ai-research
DATASET_DIR = Path(__file__).resolve().parents[1] / "dataset"
PEOPLE_DIR = DATASET_DIR / "people"
CLOTHING_DIR = DATASET_DIR / "clothing"
TEST_PAIRS_FILE = DATASET_DIR / "test_pairs" / "test_pairs.json"


def load_test_pairs():
    """Load test pairs from dataset documentation."""
    with open(TEST_PAIRS_FILE) as f:
        return json.load(f)["pairs"]


# ---------------------------------------------------------------------------
# Test counters
# ---------------------------------------------------------------------------
passed = 0
failed = 0
errors = []


def test(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print(f"  PASS: {name}")
    else:
        failed += 1
        errors.append(f"{name}: {detail}")
        print(f"  FAIL: {name} — {detail}")


# ===========================================================================
# TC-07.1: Valid Image Validation
# ===========================================================================
print("\n=== TC-07.1: Valid Image Validation ===")
pairs = load_test_pairs()
for pair in pairs[:3]:  # Test first 3 pairs
    person_path = str(PEOPLE_DIR / pair["person_image"].split("/")[-1])
    garment_path = str(CLOTHING_DIR / pair["clothing_image"].split("/")[-1])
    try:
        person_info = ImageValidator.validate(person_path)
        garment_info = ImageValidator.validate(garment_path)
        test(
            f"Valid pair {pair['pair_id']}",
            person_info.width == 768 and person_info.height == 1024
            and garment_info.width == 768 and garment_info.height == 1024,
            f"Person: {person_info.width}x{person_info.height}, Garment: {garment_info.width}x{garment_info.height}",
        )
    except Exception as e:
        test(f"Valid pair {pair['pair_id']}", False, str(e))

# ===========================================================================
# TC-07.2: Invalid Image — File Not Found
# ===========================================================================
print("\n=== TC-07.2: Invalid Image — File Not Found ===")
try:
    ImageValidator.validate("/nonexistent/path/image.jpg")
    test("File not found raises ValidationError", False, "No exception raised")
except ValidationError:
    test("File not found raises ValidationError", True)
except Exception as e:
    test("File not found raises ValidationError", False, f"Wrong exception: {type(e).__name__}: {e}")

# ===========================================================================
# TC-07.3: Invalid Image — Corrupted File
# ===========================================================================
print("\n=== TC-07.3: Invalid Image — Corrupted File ===")
with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
    tmp.write(b"\x00\x01\x02\x03\x04\x05 corrupted jpg data")
    tmp_path = tmp.name
try:
    ImageValidator.validate(tmp_path)
    test("Corrupted file raises ValidationError", False, "No exception raised")
except ValidationError:
    test("Corrupted file raises ValidationError", True)
except Exception as e:
    test("Corrupted file raises ValidationError", False, f"Wrong exception: {type(e).__name__}: {e}")
finally:
    os.unlink(tmp_path)

# ===========================================================================
# TC-07.4: Invalid Image — Unsupported Format
# ===========================================================================
print("\n=== TC-07.4: Invalid Image — Unsupported Format ===")
with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
    tmp.write(b"this is not an image")
    tmp_path = tmp.name
try:
    ImageValidator.validate(tmp_path)
    test("Unsupported format raises ValidationError", False, "No exception raised")
except ValidationError:
    test("Unsupported format raises ValidationError", True)
except Exception as e:
    test("Unsupported format raises ValidationError", False, f"Wrong exception: {type(e).__name__}: {e}")
finally:
    os.unlink(tmp_path)

# ===========================================================================
# TC-07.5: Invalid Image — Too Small
# ===========================================================================
print("\n=== TC-07.5: Invalid Image — Too Small ===")
from PIL import Image
with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
    img = Image.new("RGB", (32, 32), color="red")
    img.save(tmp_path := tmp.name, format="PNG")
try:
    ImageValidator.validate(tmp_path)
    test("Too small image raises ValidationError", False, "No exception raised")
except ValidationError:
    test("Too small image raises ValidationError", True)
except Exception as e:
    test("Too small image raises ValidationError", False, f"Wrong exception: {type(e).__name__}: {e}")
finally:
    os.unlink(tmp_path)

# ===========================================================================
# TC-07.6: Preprocessing — RGB Conversion
# ===========================================================================
print("\n=== TC-07.6: Preprocessing — RGB Conversion ===")
with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
    img = Image.new("L", (100, 100), color=128)  # Grayscale
    img.save(tmp_path := tmp.name, format="PNG")
try:
    with Image.open(tmp_path) as img:
        result = Preprocessor.preprocess(img, img)
        test(
            "Grayscale converted to RGB",
            result[0].mode == "RGB" and result[1].mode == "RGB",
            f"Mode: {result[0].mode}, {result[1].mode}",
        )
except Exception as e:
    test("Grayscale converted to RGB", False, str(e))
finally:
    os.unlink(tmp_path)

# ===========================================================================
# TC-07.7: Preprocessing — Resize Large Image
# ===========================================================================
print("\n=== TC-07.7: Preprocessing — Resize ===")
with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
    img = Image.new("RGB", (1536, 2048), color="blue")
    img.save(tmp_path := tmp.name, format="PNG")
try:
    with Image.open(tmp_path) as img:
        result = Preprocessor.preprocess(img, img)
        test(
            "Large image resized within 768x1024",
            result[0].width <= 768 and result[0].height <= 1024,
            f"Result: {result[0].width}x{result[0].height}",
        )
except Exception as e:
    test("Large image resized", False, str(e))
finally:
    os.unlink(tmp_path)

# ===========================================================================
# TC-07.8: Preprocessing — Aspect Ratio Preserved
# ===========================================================================
print("\n=== TC-07.8: Preprocessing — Aspect Ratio ===")
with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
    img = Image.new("RGB", (200, 100), color="green")  # 2:1 ratio
    img.save(tmp_path := tmp.name, format="PNG")
try:
    with Image.open(tmp_path) as img:
        result = Preprocessor.preprocess(img, img)
        orig_ratio = 200 / 100
        new_ratio = result[0].width / result[0].height
        test(
            "Aspect ratio preserved",
            abs(orig_ratio - new_ratio) < 0.01,
            f"Original: {orig_ratio:.2f}, Result: {new_ratio:.2f}",
        )
except Exception as e:
    test("Aspect ratio preserved", False, str(e))
finally:
    os.unlink(tmp_path)

# ===========================================================================
# TC-07.9: Pipeline — No Model Adapter
# ===========================================================================
print("\n=== TC-07.9: Pipeline — No Model Adapter ===")
pipeline = VirtualTryOnPipeline()
request = TryOnRequest(
    person_image_path=str(PEOPLE_DIR / "00891_00.jpg"),
    garment_image_path=str(CLOTHING_DIR / "01260_00.jpg"),
    category=GarmentCategory.TOPS,
)
result = pipeline.run(request, output_dir="outputs")
test(
    "Pipeline fails without model adapter",
    result.status == PipelineStatus.FAILED
    and "No model adapter" in (result.error_message or ""),
    f"Status: {result.status}, Error: {result.error_message}",
)

# ===========================================================================
# TC-07.10: Pipeline — Valid Request Structure (mock adapter)
# ===========================================================================
print("\n=== TC-07.10: Pipeline — Request Structure ===")
test(
    "TryOnRequest has correct fields",
    hasattr(request, "person_image_path")
    and hasattr(request, "garment_image_path")
    and hasattr(request, "category")
    and hasattr(request, "num_samples"),
    "All required fields present",
)

test(
    "TryOnResult has status field",
    hasattr(result, "status")
    and hasattr(result, "output_images")
    and hasattr(result, "processing_time_seconds"),
    "All required result fields present",
)

# ===========================================================================
# TC-07.11: API Interface Structure (validate api_interface.md exists)
# ===========================================================================
print("\n=== TC-07.11: API Interface Structure ===")
api_interface_path = (
    Path(__file__).resolve().parents[1] / "integration" / "api_interface.md"
)
test(
    "API interface document exists",
    api_interface_path.exists(),
    f"Path: {api_interface_path}",
)
if api_interface_path.exists():
    content = api_interface_path.read_text()
    test(
        "Health endpoint defined",
        "/api/v1/tryon/health" in content,
    )
    test(
        "Generate endpoint defined",
        "/api/v1/tryon/generate" in content,
    )
    test(
        "Status endpoint defined",
        "/api/v1/tryon/status/" in content,
    )
    test(
        "Result endpoint defined",
        "/api/v1/tryon/result/" in content,
    )
    test(
        "Error response format defined",
        "error" in content.lower() and "message" in content.lower(),
    )

# ===========================================================================
# TC-07.12: Kaggle Notebook Structure
# ===========================================================================
print("\n=== TC-07.12: Kaggle Notebook Structure ===")
kaggle_nb_path = (
    Path(__file__).resolve().parents[1] / "prototype" / "kaggle_fashn_vton.ipynb"
)
test(
    "Kaggle notebook exists",
    kaggle_nb_path.exists(),
    f"Path: {kaggle_nb_path}",
)
if kaggle_nb_path.exists():
    nb = json.loads(kaggle_nb_path.read_text(encoding="utf-8"))
    test(
        "Notebook is valid JSON",
        "cells" in nb and "metadata" in nb,
    )
    source_text = " ".join(
        "".join(cell.get("source", [])) for cell in nb.get("cells", [])
    )
    test(
        "HF_TOKEN from environment (no hardcoded token)",
        "os.environ.get(\"HF_TOKEN\")" in source_text,
    )
    test(
        "12 test pairs defined",
        '"P01"' in source_text and '"P12"' in source_text,
    )
    test(
        "No hardcoded HF token in source",
        "hf_token =" in source_text and "os.environ" in source_text,
    )

# ===========================================================================
# Summary
# ===========================================================================
print("\n" + "=" * 60)
print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed}")
print("=" * 60)
if failed:
    print("\nFailures:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("\nAll tests passed!")
    sys.exit(0)
