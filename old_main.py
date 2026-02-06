import os
import torch
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from diffusers import StableDiffusionControlNetImg2ImgPipeline, ControlNetModel
from transformers import pipeline

# Configuration
INPUT_DIR = "inputs"
OUTPUT_DIR = "outputs"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {DEVICE}")

def load_models():
    """Loads and returns the necessary models."""
    print("Loading models... this may take a while.")
    
    # Load ControlNet
    controlnet = ControlNetModel.from_pretrained(
        "lllyasviel/sd-controlnet-depth",
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32
    )

    # Load Stable Diffusion with ControlNet
    pipe = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        controlnet=controlnet,
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
        safety_checker=None
    ).to(DEVICE)
    
    pipe.enable_attention_slicing()
    # pipe.enable_model_cpu_offload() # Enable this if you hit OOM errors on 6GB RAM
    
    # Load Depth Estimator
    depth_estimator = pipeline(
        "depth-estimation",
        model="Intel/dpt-hybrid-midas",
        device=0 if DEVICE == "cuda" else -1
    )
    
    # Load Segmentation Model
    segmenter = pipeline(
        "image-segmentation",
        model="facebook/detr-resnet-50-panoptic",
        device=0 if DEVICE == "cuda" else -1
    )
    
    return pipe, depth_estimator, segmenter

def process_image(image_path, pipe, depth_estimator, segmenter, prompt, negative_prompt, output_name):
    """Processes a single image."""
    print(f"Processing {image_path}...")
    
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found.")
        return

    # 1. Load and prep image
    init_image = Image.open(image_path)
    init_image = ImageOps.exif_transpose(init_image).convert("RGB")
    
    # Resize to max 512 layout
    w, h = init_image.size
    scale = 512 / min(w, h)
    new_size = (int(w * scale), int(h * scale))
    init_image = init_image.resize(new_size)
    
    # 2. Generate Depth Map
    print("Generating depth map...")
    depth_output = depth_estimator(init_image)
    depth_map = depth_output["depth"]
    depth_map = np.array(depth_map)
    depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())
    depth_map = (depth_map * 255).astype("uint8")
    depth_image = Image.fromarray(depth_map).convert("RGB").resize(init_image.size)

    # 3. Generate Generation Loop (Using Depth only for now as per original main flow logic)
    # The original script had segmentation but didn't strictly use it in the main pipe calls shown efficiently, 
    # except one complex call at the end. We'll stick to the main depth-conditioned generation for now.
    
    print("Running Stable Diffusion...")
    result = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=init_image,
        control_image=depth_image,
        strength=0.85,
        guidance_scale=8.5,
        controlnet_conditioning_scale=1.0,
        num_inference_steps=50
    ).images[0]
    
    output_path = os.path.join(OUTPUT_DIR, output_name)
    result.save(output_path)
    print(f"Saved result to {output_path}")
    return result

def main():
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pipe, depth_estimator, segmenter = load_models()

    # Example Prompt
    prompt = """
    Opulent luxury living room lounge,
    rich jewel-toned velvet sofas in deep emerald green and sapphire blue,
    brushed brass metal accents on tables and lighting fixtures,
    dark walnut wood paneling on walls, large ornate crystal chandelier,
    thick plush silk rug, curated art pieces, glamorous atmosphere,
    cinematic lighting, highly detailed textures, 8k
    """

    negative_prompt = """
    distorted room, warped walls, extra furniture,
    duplicate objects, low quality
    """
    
    # Find images in input dir
    images = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not images:
        print(f"No images found in {INPUT_DIR}. Please add an image.")
        return

    for img_name in images:
        process_image(
            os.path.join(INPUT_DIR, img_name),
            pipe, depth_estimator, segmenter,
            prompt, negative_prompt,
            f"processed_{img_name}"
        )

if __name__ == "__main__":
    main()
