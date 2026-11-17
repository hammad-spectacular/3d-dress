# AI Virtual Try-On — Dataset Documentation

**Project:** AI Virtual Try-On (Member 3 — AI & Computer Vision Developer)  
**Module:** 2 — Dataset Preparation  
**Workspace:** `ai-research/dataset/`  
**Project use:** Personal use and experimentation only (non-commercial)  
**Budget:** Zero — no purchases, no subscriptions, no API credits  
**Machine:** 16 GB RAM, 256 GB SSD, no dedicated GPU assumed  

---

## 1. Folder Structure

```
ai-research/dataset/
├── people/          # Person (model) images — target bodies for try-on
├── clothing/        # Clothing (garment) images — items to try on
├── test_pairs/      # Defined person↔clothing pairs for validation
└── dataset_documentation.md   # This file
```

- `dataset/people/` — Place person images here. These are the people onto whom clothing will be tried on.
- `dataset/clothing/` — Place clothing images here. These are the garments (shirts, dresses, trousers, jackets).
- `dataset/test_pairs/` — Place pair definitions and reference outputs here.

> **Status (as of Module 2 completion):** Images have been downloaded from VITON-HD test split and placed in the respective folders. See Section 10 for actual dataset status.

---

## 2. Recommended Free Datasets (Non-Commercial / Personal Use OK)

Because this project is **personal and non-commercial**, datasets with **Non-Commercial (NC)** licenses are acceptable. All datasets below permit personal experimentation and research.

### 2.1 VITON-HD

| Field | Detail |
|-------|--------|
| **Source** | https://github.com/shadow2496/VITON-HD |
| **Paper** | VITON-HD: High-Resolution Virtual Try-On via Misalignment-Aware Normalization (CVPR 2021) |
| **License** | CC BY-NC 4.0 (Creative Commons Attribution-NonCommercial 4.0) |
| **Commercial use** | Not allowed — personal/research use only |
| **Attribution required** | Yes — cite the paper |
| **Content** | 11,647 train + 2,032 test pairs; frontal-view woman + top-clothing pairs |
| **Resolution** | 1024 × 768 |
| **Categories** | Tops / shirts (upper body) |
| **Format** | Paired person + garment images |
| **Download** | Preprocessed dataset via repository link; test images via Google Drive folder linked in README |
| **Size** | ~4.4 GB (full), smaller for test split only |

**Restrictions:** Non-commercial only. Must attribute by citing the paper. No commercial products or paid services using this data.

**Suitability for this project:** Excellent for shirts/tops. 2,032 test pairs available — more than enough to select 20–30 person images and 20–30 clothing images.

---

### 2.2 Dress Code (DressCode)

| Field | Detail |
|-------|--------|
| **Source** | https://github.com/aimagelab/dress-code |
| **Paper** | Dress Code: High-Resolution Multi-Category Virtual Try-On (ECCV 2022) |
| **License** | Non-commercial academic license (YOOX NET-A-PORTER terms) |
| **Commercial use** | Not allowed |
| **Attribution required** | Yes — cite the paper |
| **Content** | 53,792 garments, 107,584 images, 3 categories |
| **Resolution** | 1024 × 768 |
| **Categories** | Upper body (shirts, tops, sweatshirts), Lower body (trousers, skirts, shorts, leggings), Dresses |
| **Format** | Paired model + garment images, plus keypoints, label maps, skeletons, DensePose |
| **Download** | Via dataset request form — requires institutional email (.edu/.ac) and signed release agreement |
| **Size** | Large (~50k+ pairs) |

**Restrictions:** 
- **Not released to private companies.**
- Requires **institutional/academic email** (gmail.com, qq.com, etc. are rejected).
- Signed release agreement form is mandatory; typed signatures not accepted.
- Requests manually validated weekly.

**Suitability for this project:** Excellent category coverage (shirts, dresses, trousers). However, access is restricted — you need an academic/institutional email. If you don't have one, this dataset may not be accessible.

---

### 2.3 FIT (FitVTO-100k)

| Field | Detail |
|-------|--------|
| **Source** | https://huggingface.co/datasets/Yuanhao-Harry-Wang/fitvto-100k |
| **Paper** | FIT: A Large-Scale Dataset for Fit-Aware Virtual Try-On |
| **License** | CC BY-NC-ND 4.0 (Attribution-NonCommercial-NoDerivatives 4.0) |
| **Commercial use** | Not allowed |
| **Attribution required** | Yes |
| **Content** | 100,000 training + 5,000 evaluation triplets |
| **Resolution** | 768 × 1024 PNG |
| **Categories** | Tops and garments (various) |
| **Format** | Triplets: person image + layflat garment image + garment-agnostic person image + body/garment measurements |
| **Download** | Hugging Face datasets server |
| **Size** | 212 GB (full) |

**Restrictions:** Non-commercial, no derivatives (ND means you cannot create adapted/derivative versions of the dataset itself, though using it for personal experimentation is permitted).

**Suitability for this project:** Very large (212 GB) — may exceed your 256 GB SSD if downloaded in full. Use only the eval split (5,000 samples) if you choose this dataset.

---

### 2.4 OpenVTON

| Field | Detail |
|-------|--------|
| **Source** | https://huggingface.co/datasets/RenxingIntelligence/OpenVTON |
| **Paper** | OpenVTON-Bench: A Large-Scale High-Resolution Benchmark for Controllable Virtual Try-On Evaluation |
| **License** | CC BY-NC 4.0 |
| **Commercial use** | Not allowed |
| **Attribution required** | Yes |
| **Content** | 99,925 garment-person pairs with masking images and garment captions |
| **Resolution** | High-resolution |
| **Categories** | 14 coarse labels (various garments) |
| **Format** | Source (garment), mask (masked person), target (person wearing garment), caption, category |
| **Download** | Hugging Face datasets server |
| **Size** | Large |

**Restrictions:** Non-commercial research only. Contains images of people — do not use for biometric identification, face recognition, surveillance, or attempts to recover personal identity.

**Suitability for this project:** Good category variety (14 labels). Includes pre-made masks which simplify try-on.

---

### 2.5 OmniView

| Field | Detail |
|-------|--------|
| **Source** | https://huggingface.co/datasets/zwpro/OmniView |
| **Paper** | BooM-VVT: Boosting Mask-Free Video Virtual Try-On with Image-Level Pseudo Data |
| **License** | Images from IGPair and public sources; all images and brands remain property of respective owners |
| **Commercial use** | Not explicitly licensed for commercial use — treat as non-commercial |
| **Attribution required** | Yes — credit IGPair and respective owners |
| **Content** | 8,597 garment-model groups; 35,904 model images; 15,879 flat-garment images |
| **Categories** | Upper body, lower body, outerwear, full body |
| **Format** | Garment images (front/back flat), model images (multi-view), metadata JSONL |
| **Download** | Hugging Face datasets server |
| **Size** | Moderate |

**Restrictions:** Garment types include outerwear (jackets). All brands/images remain property of owners — use for personal experimentation only.

**Suitability for this project:** Good for jackets/outerwear category which other datasets lack.

---

### 2.6 StreetTryOn

| Field | Detail |
|-------|--------|
| **Source** | https://github.com/cuiaiyu/street-tryon-benchmark |
| **License** | Inherits DeepFashion2 + VITON-HD licenses — no commercial usage |
| **Content** | 12,364 train + 2,089 validation in-the-wild person images |
| **Format** | Unpaired person images (from DeepFashion2) |
| **Download** | Requires DeepFashion2 access password + annotation download |

**Restrictions:** No commercial usage. Requires DeepFashion2 access (zip password).

---

## 3. Recommended Dataset Selection for This Project

Given your constraints (personal use, zero budget, 256 GB SSD, 16 GB RAM, no GPU), I recommend:

| Priority | Dataset | Reason | Categories Covered |
|----------|---------|--------|-------------------|
| 1 | **VITON-HD** | CC BY-NC 4.0, directly downloadable, no email gate, ~4.4 GB full / smaller test split | Shirts / tops |
| 2 | **OmniView** | Includes jackets/outerwear, moderate size, from public sources | Jackets / outerwear |
| 3 | **Dress Code** | If you have an institutional email — best category coverage | Dresses, trousers, shirts |
| 4 | **OpenVTON** | 14 categories, pre-made masks | Various |

**Minimum viable selection:** VITON-HD (shirts) + OmniView (jackets) + one more source for dresses/trousers (Dress Code if eligible, otherwise OpenVTON or a manually curated set).

---

## 4. Target Image Counts

| Category | Person Images | Clothing Images | Source |
|----------|--------------|-----------------|--------|
| Shirts / tops | 8–10 | 8–10 | VITON-HD |
| Dresses | 4–6 | 4–6 | Dress Code / OpenVTON |
| Trousers / lower body | 4–6 | 4–6 | Dress Code / OpenVTON |
| Jackets / outerwear | 4–6 | 4–6 | OmniView |
| **Total** | **20–28** | **20–28** | |

Target: **20–30 person images** and **20–30 clothing images**, covering shirts, dresses, trousers, and jackets.

---

## 5. How to Download (Manual Steps)

I cannot download binary image files for you. Please perform these steps yourself:

### VITON-HD
1. Go to https://github.com/shadow2496/VITON-HD
2. Follow the "Dataset" section in the README to download the preprocessed dataset (Google Drive link)
3. Extract the `test` split (2,032 pairs) to keep download size manageable
4. Copy person images → `ai-research/dataset/people/`
5. Copy garment images → `ai-research/dataset/clothing/`

### Dress Code (if you have institutional email)
1. Go to https://github.com/aimagelab/dress-code
2. Complete the dataset request form with your institutional email
3. Sign and submit the release agreement
4. Wait for approval (validated weekly)
5. Download approved category splits (upper_body, lower_body, dresses)
6. Copy images to respective folders

### OmniView
1. Go to https://huggingface.co/datasets/zwpro/OmniView
2. Download the garment-model data release
3. Extract model images → `ai-research/dataset/people/`
4. Extract flat-garment images → `ai-research/dataset/clothing/`

### OpenVTON
1. Go to https://huggingface.co/datasets/RenxingIntelligence/OpenVTON
2. Download via Hugging Face datasets server (use only a subset to save space)
3. Copy source/garment images → `ai-research/dataset/clothing/`
4. Copy target/person images → `ai-research/dataset/people/`

---

## 6. Test Pair Plan

Create person↔clothing pairs for validation. Each pair = one person image + one clothing image of a compatible category.

### Pairing Scheme (24 pairs planned)

| Pair ID | Person Image | Clothing Image | Category | Source |
|---------|-------------|----------------|----------|--------|
| P01 | person_01.jpg | shirt_01.jpg | Shirt / top | VITON-HD |
| P02 | person_02.jpg | shirt_02.jpg | Shirt / top | VITON-HD |
| P03 | person_03.jpg | shirt_03.jpg | Shirt / top | VITON-HD |
| P04 | person_04.jpg | shirt_04.jpg | Shirt / top | VITON-HD |
| P05 | person_05.jpg | shirt_05.jpg | Shirt / top | VITON-HD |
| P06 | person_06.jpg | shirt_06.jpg | Shirt / top | VITON-HD |
| P07 | person_07.jpg | shirt_07.jpg | Shirt / top | VITON-HD |
| P08 | person_08.jpg | shirt_08.jpg | Shirt / top | VITON-HD |
| P09 | person_09.jpg | dress_01.jpg | Dress | Dress Code / OpenVTON |
| P10 | person_10.jpg | dress_02.jpg | Dress | Dress Code / OpenVTON |
| P11 | person_11.jpg | dress_03.jpg | Dress | Dress Code / OpenVTON |
| P12 | person_12.jpg | dress_04.jpg | Dress | Dress Code / OpenVTON |
| P13 | person_13.jpg | trousers_01.jpg | Trousers | Dress Code / OpenVTON |
| P14 | person_14.jpg | trousers_02.jpg | Trousers | Dress Code / OpenVTON |
| P15 | person_15.jpg | trousers_03.jpg | Trousers | Dress Code / OpenVTON |
| P16 | person_16.jpg | trousers_04.jpg | Trousers | Dress Code / OpenVTON |
| P17 | person_17.jpg | jacket_01.jpg | Jacket / outerwear | OmniView |
| P18 | person_18.jpg | jacket_02.jpg | Jacket / outerwear | OmniView |
| P19 | person_19.jpg | jacket_03.jpg | Jacket / outerwear | OmniView |
| P20 | person_20.jpg | jacket_04.jpg | Jacket / outerwear | OmniView |
| P21 | person_21.jpg | shirt_09.jpg | Shirt / top (cross-pair) | VITON-HD |
| P22 | person_22.jpg | dress_05.jpg | Dress (cross-pair) | Dress Code / OpenVTON |
| P23 | person_23.jpg | trousers_05.jpg | Trousers (cross-pair) | Dress Code / OpenVTON |
| P24 | person_24.jpg | jacket_05.jpg | Jacket (cross-pair) | OmniView |

**Cross-pairs** (P21–P24) intentionally mix different person↔clothing combinations to test generalization.

Store pair metadata in `ai-research/dataset/test_pairs/test_pairs.json` (template below).

---

## 7. test_pairs.json Template

Create this file at `ai-research/dataset/test_pairs/test_pairs.json`:

```json
{
  "project": "AI Virtual Try-On",
  "module": "Dataset Preparation (Module 2)",
  "use_case": "Personal and non-commercial experimentation only",
  "total_pairs": 24,
  "categories": ["shirt", "dress", "trousers", "jacket"],
  "pairs": [
    {
      "pair_id": "P01",
      "category": "shirt",
      "person_image": "dataset/people/person_01.jpg",
      "clothing_image": "dataset/clothing/shirt_01.jpg",
      "source_dataset": "VITON-HD",
      "license": "CC BY-NC 4.0"
    }
    // ... add P02-P24 here
  ],
  "notes": "Replace filenames with actual downloaded image names. Cross-pairs (P21-P24) test generalization across different person-clothing combinations."
}
```

---

## 8. License and Restriction Summary

| Dataset | License | Commercial? | Attribution? | Access Restrictions |
|---------|---------|-------------|--------------|-------------------|
| VITON-HD | CC BY-NC 4.0 | ❌ No | Yes (cite paper) | None (direct download) |
| Dress Code | Non-commercial academic | ❌ No | Yes | Institutional email + signed agreement |
| FIT (FitVTO-100k) | CC BY-NC-ND 4.0 | ❌ No | Yes | None (Hugging Face) |
| OpenVTON | CC BY-NC 4.0 | ❌ No | Yes | None (Hugging Face) |
| OmniView | Respective owners' rights | ❌ Treat as no | Yes | None (Hugging Face) |
| StreetTryOn | DeepFashion2 + VITON-HD | ❌ No | Yes | DeepFashion2 access password |

**Important:** All datasets above are **non-commercial only**. Since your project is personal and experimental, this is acceptable. **Do not** use any of these datasets or models trained on them for commercial purposes.

**Do not:**
- Upload private photographs publicly
- Use images with unknown/unclear permissions
- Use any dataset commercially
- Exceed your 256 GB SSD (be selective — download only needed splits)

---

## 9. Next Steps (Pending Your Approval)

Images have been downloaded and placed. Test pairs have been created. Report back when ready to proceed to Module 3 (prototype development).

---

## 10. Actual Dataset Status (as of Module 2 Completion)

### 10.1 Images Downloaded and Placed

| Folder | Files | Source |
|--------|-------|--------|
| `dataset/people/` | 6 person images + 1 README.txt | VITON-HD test split (`3d clothing\test\test\image\`) |
| `dataset/clothing/` | 12 clothing images + 1 README.txt | VITON-HD test split (`3d clothing\test\test\cloth\`) |
| `dataset/test_pairs/` | test_pairs.json + 1 README.txt | Created from actual filenames |

### 10.2 Image Validation Results

All images validated using PIL/Pillow — no corruption, no duplicates, all readable.

**People images (6 total):**

| Filename | Format | Dimensions | Mode | Size |
|----------|--------|------------|------|------|
| 00891_00.jpg | JPEG | 768 × 1024 | RGB | 105 KB |
| 03615_00.jpg | JPEG | 768 × 1024 | RGB | 142 KB |
| 07445_00.jpg | JPEG | 768 × 1024 | RGB | 128 KB |
| 07573_00.jpg | JPEG | 768 × 1024 | RGB | 107 KB |
| 08909_00.jpg | JPEG | 768 × 1024 | RGB | 181 KB |
| 10549_00.jpg | JPEG | 768 × 1024 | RGB | 133 KB |

**Clothing images (12 total):**

| Filename | Format | Dimensions | Mode | Size |
|----------|--------|------------|------|------|
| 01260_00.jpg | JPEG | 768 × 1024 | RGB | 178 KB |
| 01430_00.jpg | JPEG | 768 × 1024 | RGB | 88 KB |
| 02783_00.jpg | JPEG | 768 × 1024 | RGB | 295 KB |
| 03751_00.jpg | JPEG | 768 × 1024 | RGB | 212 KB |
| 06429_00.jpg | JPEG | 768 × 1024 | RGB | 147 KB |
| 06802_00.jpg | JPEG | 768 × 1024 | RGB | 91 KB |
| 07429_00.jpg | JPEG | 768 × 1024 | RGB | 105 KB |
| 08348_00.jpg | JPEG | 768 × 1024 | RGB | 211 KB |
| 09933_00.jpg | JPEG | 768 × 1024 | RGB | 87 KB |
| 11028_00.jpg | JPEG | 768 × 1024 | RGB | 126 KB |
| 11351_00.jpg | JPEG | 768 × 1024 | RGB | 69 KB |
| 11791_00.jpg | JPEG | 768 × 1024 | RGB | 114 KB |

### 10.3 Actual Counts vs Target

| Category | Target | Actual | Status |
|----------|--------|--------|--------|
| Person images | 20–30 | 6 | ⚠️ Below target |
| Clothing images | 20–30 | 12 | ⚠️ Below target |
| Shirts / tops | 8–10 | 12 | ✅ Exceeds target |
| Dresses | 4–6 | 0 | ❌ Not available |
| Trousers / lower body | 4–6 | 0 | ❌ Not available |
| Jackets / outerwear | 4–6 | 0 | ❌ Not available |
| **Total pairs** | 24 | 12 | ⚠️ Below target |

### 10.4 Test Pairs Created (12 total)

| Pair ID | Person | Clothing | Category | Pair Type |
|---------|--------|----------|----------|-----------|
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

All pairs recorded in `dataset/test_pairs/test_pairs.json`.

### 10.5 Limitations

1. **Only VITON-HD test split available.** Could not obtain Dress Code (requires institutional email), OpenVTON, or OmniView because no additional downloads were permitted.
2. **Only shirts/tops available.** VITON-HD contains only upper-body garments. No dresses, trousers, or jackets in the downloaded data.
3. **Below target counts.** Only 6 person images and 12 clothing images (target was 20–30 each).
4. **All from one dataset.** No cross-dataset variety; all images share the same source characteristics (frontal-view women, upper-body garments, 768×1024 resolution).
5. **No masks or annotations included.** Only raw person and clothing images were copied; cloth-mask, image-parse, and openpose files from the source were not included.

### 10.6 License

All images are from VITON-HD, licensed under **CC BY-NC 4.0** (Creative Commons Attribution-NonCommercial 4.0).
- ✅ Permitted: Personal use, research, experimentation, academic publication
- ❌ Not permitted: Commercial use, commercial products, paid services
- Required: Attribution by citing the VITON-HD paper (Choi et al., CVPR 2021)

Since this project is **personal and non-commercial**, this license is acceptable.

### 10.7 Recommendation for Module 3

With 6 person images and 12 shirt images, the prototype can be developed and tested using the 12 defined pairs. All pairs are shirt-category try-ons. If dresses, trousers, or jackets are needed later, additional datasets would need to be downloaded (subject to your approval).

