# 🎨 Custom LoRA Path Guide

## Table of Contents
- [What is LoRA?](#what-is-lora)
- [How Custom LoRA Works](#how-custom-lora-works)
- [Using LoRA in Home Deck AI](#using-lora-in-home-deck-ai)
- [Example Use Cases](#example-use-cases)
- [Finding LoRA Models](#finding-lora-models)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## What is LoRA?

**LoRA** (Low-Rank Adaptation) is a technique for fine-tuning AI models to add specific styles, subjects, or capabilities **without retraining the entire base model**.

### Key Benefits:
- ✅ **Small file size** (~10-500 MB vs. several GB for full models)
- ✅ **Easy to use** - Just plug and play
- ✅ **Stackable** - Can combine multiple LoRAs
- ✅ **Specialized** - Trained for specific styles or purposes
- ✅ **Community-driven** - Thousands available on HuggingFace

Think of LoRA as a "style plugin" or "add-on module" that enhances the base AI model with specialized capabilities.

---

## How Custom LoRA Works

In Home Deck AI, LoRAs modify the **Realistic Vision V6.0** base model to:

1. **Add new artistic styles** (e.g., cyberpunk, art nouveau, retro-futuristic)
2. **Enhance specific materials** (e.g., marble, wood, glass textures)
3. **Introduce unique aesthetics** (e.g., anime-style, watercolor, sketch-like)
4. **Improve specific elements** (e.g., lighting, furniture, architectural details)

### Technical Flow:
```
Base Model (Realistic Vision V6.0)
    ↓
+ LoRA Weights (Specialized Style)
    ↓
= Enhanced Model with New Capabilities
```

---

## Using LoRA in Home Deck AI

### Step-by-Step Guide:

#### 1. **Find a LoRA Model**
Visit [HuggingFace](https://huggingface.co/models?pipeline_tag=text-to-image&sort=trending) and search for:
- "interior design lora"
- "architecture lora sd1.5"
- "style lora stable diffusion 1.5"

> **Important:** Make sure the LoRA is compatible with **Stable Diffusion 1.5**

#### 2. **Get the Model Path**
Copy the model identifier in format: `username/model-name`

Example: `artificialguybr/StudioGhibli-LoRA-SD1.5`

#### 3. **Enter in the App**
1. Open Home Deck AI at `http://127.0.0.1:7860`
2. Expand **"⚙️ Advanced Settings"**
3. Paste the model path in **"🎯 Custom LoRA Path"** field
4. Generate your design as normal

#### 4. **First Use**
- The LoRA will download automatically (~100-500 MB)
- Subsequent uses will be instant (cached locally)

---

## Example Use Cases

### 1. **Turbo Mode (Built-in)**
```
LoRA Path: latent-consistency/lcm-lora-sdv1-5
Purpose: Ultra-fast generation (4-8 steps)
Use Case: Quick previews and iterations
```

### 2. **Studio Ghibli Style Interiors**
```
LoRA Path: artificialguybr/StudioGhibli-LoRA-SD1.5
Purpose: Anime-inspired, whimsical interiors
Use Case: Unique playrooms, creative spaces
```

### 3. **Architectural Detail Enhancement**
```
LoRA Path: <architecture-specific-lora>
Purpose: Enhanced architectural elements
Use Case: Professional presentations
```

### 4. **Retro/Vintage Styles**
```
LoRA Path: <vintage-lora>
Purpose: 1950s-1980s aesthetic
Use Case: Retro-themed restaurants, bars
```

### 5. **Minimalist Enhancement**
```
LoRA Path: <minimalist-lora>
Purpose: Ultra-clean, Japanese-inspired minimalism
Use Case: Modern apartments, zen spaces
```

---

## Finding LoRA Models

### Recommended Sources:

#### 1. **HuggingFace Hub** ⭐
- URL: https://huggingface.co/models
- Filter: `text-to-image` pipeline
- Search: "lora sd1.5", "interior design"

#### 2. **Civitai**
- URL: https://civitai.com/
- Filter: LoRA, SD 1.5
- Category: Architecture, Interior Design

### Compatibility Checklist:
- ✅ Must be **Stable Diffusion 1.5** compatible
- ✅ Should be in **HuggingFace format** for direct loading
- ✅ Check reviews and example images
- ⚠️ Avoid SDXL-only LoRAs (incompatible)

---

## Best Practices

### For Beginners:
- ❌ **Don't use LoRA initially** - The 10 preset styles are sufficient
- ✅ Master the basic prompt builder first
- ✅ Experiment with one LoRA at a time
- ✅ Start with popular, well-reviewed LoRAs

### For Advanced Users:
- ✅ **Adjust prompts** when using LoRAs (read the LoRA documentation)
- ✅ **Lower guidance scale** if output is too strong (edit `interior_designer.py`)
- ✅ **Combine with custom prompts** for unique results
- ✅ **Document your favorites** for future use

### Prompt Tips with LoRA:
```
Good Prompt with LoRA:
"Modern living room, Studio Ghibli style, whimsical, warm colors, 8k"

Bad Prompt with LoRA:
"Modern living room, photorealistic, ultra detailed, 8k"
(Conflicts with the anime LoRA style)
```

---

## Troubleshooting

### Common Issues:

#### **Issue 1: LoRA Not Loading**
```
Error: "Failed to load LoRA"
```
**Solutions:**
- Verify the path format: `username/model-name`
- Check internet connection (first download)
- Ensure SD 1.5 compatibility
- Try a different LoRA to test

---

#### **Issue 2: Output Doesn't Look Different**
**Solutions:**
- Adjust your prompt to match the LoRA style
- Increase LoRA weight in code (default is 1.0)
- Check if LoRA is actually compatible

---

#### **Issue 3: Download is Slow**
**Solutions:**
- LoRAs can be 100-500 MB - be patient on first use
- Check your internet speed
- Files are cached locally after first download

---

#### **Issue 4: Results Too Strong/Weak**
**Solution:** Edit `interior_designer.py` to adjust LoRA weight:
```python
def load_custom_lora(self, lora_path, weight=1.0):  # Change weight value
    print(f"Loading LoRA: {lora_path}")
    self.pipe.load_lora_weights(lora_path)
```
- **Default:** 1.0 (100% strength)
- **Subtle:** 0.5-0.7
- **Strong:** 1.2-1.5

---

## Advanced Configuration

### Multiple LoRAs (Code Modification Required)

Currently, the app supports **one LoRA at a time**. To use multiple LoRAs, you need to modify `interior_designer.py`:

```python
# Example: Load multiple LoRAs
self.pipe.load_lora_weights("lora1/path", adapter_name="lora1")
self.pipe.load_lora_weights("lora2/path", adapter_name="lora2")
self.pipe.set_adapters(["lora1", "lora2"], adapter_weights=[0.7, 0.5])
```

---

## Who Should Use Custom LoRA?

### ❌ **Skip LoRA if you are:**
- Just starting with the app
- Happy with the 10 preset styles
- Creating general interior designs
- Looking for simplicity

### ✅ **Use LoRA if you are:**
- An advanced user wanting unique styles
- Working on brand-specific projects
- Experimenting with artistic interpretations
- Need specialized aesthetics not in presets

---

## Popular LoRA Categories for Interior Design

| Category | Example Use | Compatibility |
|----------|-------------|---------------|
| **Architectural** | Enhance structural details | SD 1.5 |
| **Material-Specific** | Marble, wood, glass | SD 1.5 |
| **Artistic Styles** | Watercolor, sketch, anime | SD 1.5 |
| **Era-Specific** | Art Deco, Victorian, Mid-Century | SD 1.5 |
| **Lighting** | Golden hour, neon, moody | SD 1.5 |

---

## Summary

- **LoRA** = Style plugin for the AI model
- **Optional** = Not required for basic use
- **Powerful** = Unlocks unique, specialized styles
- **Easy to use** = Just paste HuggingFace path
- **Compatible** = Must be SD 1.5 format

**Bottom Line:** Custom LoRA Path is an advanced feature for users who want to go beyond the 10 built-in preset styles and create truly unique interior designs! 🎨

---

## Need Help?

- Check the [HuggingFace Documentation](https://huggingface.co/docs/diffusers/using-diffusers/loading_adapters)
- Review LoRA model pages for specific prompt recommendations
- Join the Stable Diffusion community for LoRA suggestions

Happy designing! 🏠✨
