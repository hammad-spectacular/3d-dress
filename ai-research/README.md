# AI Virtual Try-On — AI Research Workspace

This folder is the independent workspace for all AI & Computer Vision development work (Member 3 role). It is kept separate from the rest of the project so that AI experimentation, dataset handling, and prototype work do not interfere with the core application code.

> **Machine constraints:** 16 GB RAM, 256 GB SSD, no dedicated GPU assumed.
> - No large AI libraries (PyTorch, TensorFlow, etc.) are installed yet.
> - No models are downloaded yet.
> - No application building has started yet.

## Folder Structure

| Folder | Purpose |
|--------|---------|
| `research/` | Literature review, algorithm notes, papers, and experimental designs for virtual try-on techniques (e.g., warping, try-on networks, pose estimation, segmentation). |
| `dataset/people/` | Source images/video of people (models) used for training and evaluation. Do not commit large media files to git. |
| `dataset/clothing/` | Source images of clothing items (tops, bottoms, dresses, etc.) used as the "garment" input for try-on. Do not commit large media files to git. |
| `dataset/test_pairs/` | Paired (person + clothing) test samples used to validate try-on quality during development. |
| `testing/test_cases/` | Test scripts, unit tests, and validation cases for CV components (detection, segmentation, warping, fitting). |
| `testing/results/` | Output images, logs, and metrics from test runs. Used to compare before/after changes. |
| `prototype/` | Early-stage AI prototypes and proof-of-concept scripts (e.g., single-image try-on, pose transfer). |
| `integration/` | Code and notes for connecting the AI try-on module with the rest of the application (frontend/backend APIs, image I/O, model serving). |
| `future_research/` | Ideas, roadmap items, and advanced features to explore later (e.g., multi-garment try-on, video try-on, real-time inference optimization). |
| `README.md` | This file. |

## Usage Notes

1. **Do not modify or delete files outside this folder.**
2. **Do not install large AI libraries or download models yet.** Wait for approval before adding dependencies.
3. **Do not start building the full application yet.** This workspace is for research and prototyping only at this stage.
4. Large dataset files and model weights should be tracked outside of git (e.g., via `.gitignore`, LFS, or external storage) given the 256 GB SSD limit.

## Next Steps (pending approval)

- Review and approve this workspace structure.
- Install AI libraries (e.g., PyTorch CPU build) if needed.
- Begin dataset curation and prototype development.
