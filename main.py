import os
import cv2
import numpy as np
from PIL import Image
from interior_designer import InteriorDesigner

def main():
    # Setup directories
    INPUT_DIR = "inputs"
    OUTPUT_DIR = "outputs"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Initialize the Professional Designer
    # This loads MLSD (Structure) + Depth (Volume) + Metrics (Measurements)
    try:
        designer = InteriorDesigner(device="cuda")
    except Exception as e:
        print(f"Error loading models: {e}")
        # Fallback to cpu if needed or handle gracefully
        # designer = InteriorDesigner(device="cpu")
        return

    # Process all images in inputs
    images = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not images:
        print("No images found in inputs/ folder.")
        return

    # Define the Design Prompt (Modern Professional Style)
    prompt = "Modern minimal interior design, high quality, 8k, photorealistic, neutral colors, cozy lighting, expansive windows"
    negative_prompt = "low quality, blurry, distorted, messy, clutter"

    for img_name in images:
        img_path = os.path.join(INPUT_DIR, img_name)
        print(f"\nProcessing {img_name}...")
        
        try:
            # 1. Generate Design
            result_img, mlsd_map, depth_map = designer.generate_design(
                img_path, 
                prompt=prompt, 
                negative_prompt=negative_prompt
            )
            
            # 2. Save Results
            base_name = os.path.splitext(img_name)[0]
            result_img.save(os.path.join(OUTPUT_DIR, f"{base_name}_design.png"))
            mlsd_map.save(os.path.join(OUTPUT_DIR, f"{base_name}_structure_map.png"))
            depth_map.save(os.path.join(OUTPUT_DIR, f"{base_name}_depth_map.png"))
            
            print(f"Saved design and maps to {OUTPUT_DIR}/")

            # 3. Simulate Measurement (Demo)
            # In a real app, user would click points. Here we simulate a calibration.
            # Assume we know the height of the room is 3.0 meters.
            # We would pick points (x1,y1) (x2,y2) spanning floor to ceiling.
            # For automation, we skip specific point picking but show the API usage:
            
            # Example usage of measurement API:
            # designer.calibrate_scale((100, 100), (100, 400), 3.0) 
            # dist = designer.measure_distance((200, 200), (300, 200))
            # print(f"Distance between sofa edges: {dist:.2f} meters")
            
        except Exception as e:
            print(f"Failed to process {img_name}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
