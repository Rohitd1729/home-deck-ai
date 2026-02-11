# Python Libraries Reference - Home Deck AI

**Understanding the Technology Stack**

This document explains each Python library used in the Home Deck AI project and its specific role in making the interior design AI work.

---

## Core AI & Machine Learning Libraries

### 1. **torch ≥ 2.0.0** (PyTorch)

**What it is:** The fundamental deep learning framework that powers everything

**Purpose in our project:**
- Runs the entire AI model (Stable Diffusion)
- Handles GPU computations via CUDA
- Manages neural network operations
- Performs tensor operations (multi-dimensional arrays)

**Specific uses:**
```python
# From interior_designer.py
import torch

# GPU device selection
self.device = "cuda"  # Uses NVIDIA GPU

# Random number generation for image variation
generator = torch.Generator(device=self.device)

# Model precision (FP16 for speed)
torch_dtype=torch.float16
```

**Why version ≥2.0.0:**
- Faster inference with `torch.compile()`
- Better GPU memory management
- Improved performance optimizations

**Without it:** No AI model would run - this is the foundation

---

### 2. **diffusers ≥ 0.21.0**

**What it is:** HuggingFace's library for diffusion models (Stable Diffusion)

**Purpose in our project:**
- Provides the Stable Diffusion pipeline
- Manages ControlNet integration
- Handles image-to-image generation
- Provides different schedulers (DPM, LCM, etc.)

**Specific uses:**
```python
from diffusers import (
    StableDiffusionControlNetImg2ImgPipeline,  # Main pipeline
    ControlNetModel,                            # ControlNet models
    DPMSolverMultistepScheduler,               # Fast scheduler
    LCMScheduler                                # Turbo mode
)

# Create the main AI pipeline
self.pipe = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
    "SG161222/Realistic_Vision_V6.0_B1_noVAE",
    controlnet=[controlnet_mlsd, controlnet_depth]
)
```

**Components we use:**
- **Pipeline**: Orchestrates the entire generation process
- **ControlNet**: Preserves room structure
- **Schedulers**: Control generation speed/quality trade-off

**Without it:** No Stable Diffusion - project wouldn't exist

---

### 3. **transformers ≥ 4.35.0**

**What it is:** HuggingFace's library for transformer models (NLP and vision)

**Purpose in our project:**
- Processes text prompts into embeddings
- Handles CLIP text encoder (converts prompts to AI-understandable format)
- Provides depth estimation model (DPT-Large)

**Specific uses:**
```python
from transformers import pipeline

# Depth estimation for measurements
self.depth_estimator = pipeline(
    "depth-estimation",
    model="Intel/dpt-large"
)
```

**What it does:**
1. **Text Encoding**: Converts "Modern minimalist living room" → numerical embeddings
2. **Depth Estimation**: Analyzes image depth for 3D understanding
3. **Model Loading**: Downloads and manages pre-trained models

**Without it:** 
- Prompts wouldn't work (no text understanding)
- No depth estimation for measurements

---

### 4. **accelerate ≥ 0.24.0**

**What it is:** HuggingFace's library for optimizing model loading and inference

**Purpose in our project:**
- Optimizes GPU memory usage
- Enables model CPU offloading
- Speeds up model loading
- Better device management

**Specific uses:**
```python
# Automatically applied when using diffusers
self.pipe.enable_model_cpu_offload()  # Uses accelerate internally
```

**What it does:**
- Moves model parts between CPU/GPU as needed
- Reduces VRAM usage
- Enables running larger models on smaller GPUs

**Technical benefit:**
- Without: Might need 8-10GB VRAM
- With: Can run on 6GB VRAM

**Without it:** Would need more powerful (expensive) GPU

---

## Image Processing Libraries

### 5. **numpy**

**What it is:** Fundamental library for numerical computations

**Purpose in our project:**
- Array/matrix operations
- Image data manipulation
- Measurement calculations
- Depth map processing

**Specific uses:**
```python
import numpy as np

# Convert PIL image to array for processing
vis_arr = np.array(vis)

# Store depth map data
self.depth_map_metric = np.array(result["depth"])

# Calculate distances
pixel_dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
```

**What it does:**
- Handles all numerical computations
- Converts between image formats
- Performs mathematical operations

**Without it:** No image manipulation, no calculations

---

### 6. **Pillow (PIL)**

**What it is:** Python Imaging Library for image operations

**Purpose in our project:**
- Load and save images
- Resize images
- Convert image formats
- Basic image preprocessing

**Specific uses:**
```python
from PIL import Image

# Load image
image = Image.open(image_path).convert("RGB")

# Resize to proper dimensions
image.resize((new_w, new_h), Image.LANCZOS)

# Save generated result
result_image.save(output_path)
```

**What it does:**
- Opens JPG/PNG files
- Resizes to AI-compatible sizes (divisible by 8)
- Saves generated designs
- Format conversions

**Without it:** Can't load/save images - no input/output

---

### 7. **opencv-python (cv2)**

**What it is:** Computer vision library from OpenCV

**Purpose in our project:**
- Draw measurement points on images
- Draw lines between points
- Image manipulation for UI feedback

**Specific uses:**
```python
import cv2

# Draw measurement points (red circles)
cv2.circle(vis_arr, point, 5, (255,0,0), -1)

# Draw line between points (green)
cv2.line(vis_arr, points[-2], points[-1], (0,255,0), 2)
```

**What it does:**
- Measurement tool visualization
- Drawing shapes on images
- Color manipulations

**Note:** Only used for the measurement feature we removed. Could potentially be removed if measurements aren't needed.

**Without it:** Measurement visualization wouldn't work

---

## AI-Specific Helper Libraries

### 8. **controlnet_aux**

**What it is:** Auxiliary models for ControlNet preprocessing

**Purpose in our project:**
- Detect lines/edges in images (MLSD)
- Estimate depth from single images (MiDaS)
- Preprocess images for ControlNet

**Specific uses:**
```python
from controlnet_aux import MLSDdetector, MidasDetector

# Line detection (preserves walls, edges)
self.mlsd_detector = MLSDdetector.from_pretrained("lllyasviel/ControlNet")
mlsd_image = self.mlsd_detector(original_image)

# Depth estimation (understands 3D space)
self.midas_detector = MidasDetector.from_pretrained("lllyasviel/ControlNet")
depth_image = self.midas_detector(original_image)
```

**What it does:**
1. **MLSD**: Finds straight lines (walls, ceilings, floors)
2. **MiDaS**: Creates depth map (how far/near objects are)

**Why critical:**
- These ensure room structure is preserved
- Without them: AI might warp walls or distort geometry

**Without it:** No structural accuracy - rooms would look distorted

---

### 9. **scipy**

**What it is:** Scientific computing library (builds on numpy)

**Purpose in our project:**
- Advanced mathematical operations
- Used internally by other libraries
- Optimization algorithms

**Indirect usage:**
- Used by `diffusers` for certain operations
- Part of the scientific Python stack
- Dependency for controlnet_aux

**Note:** Not directly called in our code, but required by dependencies

**Without it:** Other libraries would fail to import

---

### 10. **safetensors**

**What it is:** Safe, fast serialization format for AI model weights

**Purpose in our project:**
- Load AI model weights safely
- Faster loading than traditional pickle format
- More secure (prevents code execution attacks)

**Specific uses:**
- Loads Stable Diffusion model weights
- Loads ControlNet weights
- Loads LoRA weights

**Technical details:**
- Modern replacement for `.bin` files
- Memory-mapped loading (faster)
- Safer than pickle (no arbitrary code execution)

**Format comparison:**
- Old: `model.bin` (pickle format)
- New: `model.safetensors` (safer, faster)

**Without it:** Would need to fall back to slower/less secure formats

---

## Dependency Relationships

### How They Work Together

```
Your Code (app.py, interior_designer.py)
    ↓
┌─────────────────────────────────────────┐
│ diffusers (Stable Diffusion Pipeline)  │
│    ↓                                    │
│    Uses: torch, transformers,           │
│          accelerate, safetensors        │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ controlnet_aux (Preprocessing)          │
│    ↓                                    │
│    Uses: torch, numpy, scipy, opencv    │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Image Processing                        │
│    Uses: Pillow, numpy, opencv          │
└─────────────────────────────────────────┘
```

---

## Installation Order & Dependencies

**Automatic dependency resolution:**
```bash
pip install torch  # Installs numpy automatically
pip install diffusers  # Installs transformers, accelerate, safetensors
pip install controlnet_aux  # Installs scipy, opencv
pip install Pillow  # Standalone
```

**Or all at once:**
```bash
pip install -r requirements.txt
```

---

## Library Sizes & Download Times

| Library | Approximate Size | Download Time (Est.) |
|---------|-----------------|----------------------|
| torch | ~2GB | 5-10 minutes |
| diffusers | ~100MB | 1-2 minutes |
| transformers | ~500MB | 2-3 minutes |
| accelerate | ~50MB | <1 minute |
| numpy | ~20MB | <1 minute |
| Pillow | ~5MB | <1 minute |
| opencv-python | ~100MB | 1-2 minutes |
| controlnet_aux | ~50MB | <1 minute |
| scipy | ~50MB | 1-2 minutes |
| safetensors | ~5MB | <1 minute |

**Total installation:** ~15-30 minutes (depending on internet speed)

---

## Version Requirements Explained

### Why minimum versions?

**torch ≥ 2.0.0:**
- Version 2.0 introduced major speed improvements
- Better CUDA support
- Required for modern diffusers features

**diffusers ≥ 0.21.0:**
- ControlNet support added in 0.21.0
- Improved LCM-LoRA support
- Better pipeline management

**transformers ≥ 4.35.0:**
- Better CLIP text encoder
- DPT depth model support
- Performance improvements

**accelerate ≥ 0.24.0:**
- Better CPU offloading
- Improved memory management

**Others (no version specified):**
- Generally backward compatible
- Latest stable version is fine

---

## What Happens Without Each Library?

| Missing Library | Impact |
|----------------|---------|
| **torch** | Complete failure - nothing works |
| **diffusers** | No AI generation possible |
| **transformers** | Prompts don't work, depth fails |
| **accelerate** | Runs but uses more GPU memory |
| **numpy** | Image operations fail |
| **Pillow** | Can't load/save images |
| **opencv-python** | Measurement visualization fails |
| **controlnet_aux** | Room structure not preserved |
| **scipy** | Dependency errors in other libs |
| **safetensors** | Model loading slower/unsafe |

---

## Summary for Your Manager

**Core Stack (3 libraries):**
1. **torch** - Deep learning foundation
2. **diffusers** - Stable Diffusion implementation
3. **transformers** - Text & vision models

**Support Stack (4 libraries):**
4. **accelerate** - Memory optimization
5. **controlnet_aux** - Structure preservation
6. **numpy** - Numerical operations
7. **Pillow** - Image I/O

**Helper Stack (3 libraries):**
8. **opencv-python** - Computer vision utilities
9. **scipy** - Scientific computing
10. **safetensors** - Safe model loading

**All together:** They enable professional-grade AI interior design generation

---

## Quick Reference

**For presentations:**
- "We use PyTorch and Stable Diffusion for AI"
- "ControlNet preserves room structure"
- "10 total libraries, ~3GB download size"
- "Standard industry tools, well-supported"

**For technical discussions:**
- "PyTorch 2.0 with CUDA for GPU acceleration"
- "HuggingFace diffusers with ControlNet integration"
- "Optimized with accelerate and xformers"
- "Modern safetensors format for security"

---

**Document Version:** 1.0  
**Last Updated:** February 11, 2026
