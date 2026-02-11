import torch
import numpy as np
import cv2
from PIL import Image
from diffusers import (
    StableDiffusionControlNetImg2ImgPipeline,
    ControlNetModel,
    UniPCMultistepScheduler,
    LCMScheduler
)
from controlnet_aux import MLSDdetector, MidasDetector
from transformers import pipeline

class InteriorDesigner:
    def __init__(self, device="cuda", base_model="SG161222/Realistic_Vision_V6.0_B1_noVAE"):
        self.device = device
        self.base_model = base_model
        
        # Pipelines
        self.pipe = None
        self.depth_estimator = None
        self.mlsd_detector = None
        self.midas_detector = None
        
        # Metrics
        self.scale_factor = 1.0 
        self.depth_map_metric = None

        # State
        self.is_turbo = False
        
        # Load models on init
        self._load_models()

    def _load_models(self):
        print(f"Loading Professional Interior Design Model: {self.base_model}...")
        
        # 1. ControlNets for Structural Accuracy
        # We stick to SD1.5 ControlNets as we are using Realistic Vision (SD1.5 base)
        controlnet_mlsd = ControlNetModel.from_pretrained(
            "lllyasviel/control_v11p_sd15_mlsd", 
            torch_dtype=torch.float16
        )
        controlnet_depth = ControlNetModel.from_pretrained(
            "lllyasviel/control_v11f1p_sd15_depth", 
            torch_dtype=torch.float16
        )

        # 2. Main Stable Diffusion Pipeline
        self.pipe = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
            self.base_model,
            controlnet=[controlnet_mlsd, controlnet_depth],
            torch_dtype=torch.float16,
            safety_checker=None
        ).to(self.device)
        
        # Default Scheduler (Fast & High Quality)
        # DPMSolver++ 2M Karras is technically the best speed/quality trade-off right now
        from diffusers import DPMSolverMultistepScheduler
        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config, 
            use_karras_sigmas=True,
            algorithm_type="dpmsolver++"
        )
        
        # Optimization
        if self.device == "cuda":
            self.pipe.enable_model_cpu_offload() 
            # Try enabling xformers for massive speedup if installed
            try:
                self.pipe.enable_xformers_memory_efficient_attention()
                print("✅ Xformers enabled (Fast!)")
            except Exception:
                print("⚠️ Xformers not found, using standard attention")
                self.pipe.enable_attention_slicing()

        # 3. Aux Detectors
        self.mlsd_detector = MLSDdetector.from_pretrained("lllyasviel/ControlNet")
        self.midas_detector = MidasDetector.from_pretrained("lllyasviel/ControlNet")

        # 4. Metric Depth Estimator
        self.depth_estimator = pipeline(
            "depth-estimation", 
            model="Intel/dpt-large", 
            device=0 if self.device == "cuda" else -1
        )
        
        print("Models Loaded Successfully.")

    def enable_turbo(self, enable=True):
        """Enables LCM-LoRA for 4-8 step generation (Super Fast)."""
        if enable and not self.is_turbo:
            print("Enabling Turbo Mode (LCM-LoRA)...")
            # Load LCM LoRA
            self.pipe.load_lora_weights("latent-consistency/lcm-lora-sdv1-5")
            self.pipe.scheduler = LCMScheduler.from_config(self.pipe.scheduler.config)
            self.is_turbo = True
        elif not enable and self.is_turbo:
            print("Disabling Turbo Mode...")
            self.pipe.unload_lora_weights()
            self.pipe.scheduler = UniPCMultistepScheduler.from_config(self.pipe.scheduler.config)
            self.is_turbo = False

    def load_custom_lora(self, lora_path, weight=1.0):
        """Loads a custom style LoRA."""
        print(f"Loading LoRA: {lora_path}")
        self.pipe.load_lora_weights(lora_path)
        # self.pipe.fuse_lora(lora_scale=weight) # Optional: fuse if needed
        
    def preprocess_image(self, image_path, max_size=1024):
        image = Image.open(image_path).convert("RGB")
        w, h = image.size
        scale = max_size / max(w, h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        new_w = new_w - (new_w % 8)
        new_h = new_h - (new_h % 8)
        return image.resize((new_w, new_h), Image.LANCZOS)

    def generate_design(self, image_path, prompt, negative_prompt="", strength=0.75, seed=-1, guidance_scale=7.5):
        original_image = self.preprocess_image(image_path)
        
        # 1. Prepare Control Images
        mlsd_image = self.mlsd_detector(original_image)
        depth_image = self.midas_detector(original_image)
        
        # FIX: Ensure control images match the exact size of the processed input image
        # This prevents the "tensor size mismatch" (96 vs 64) error
        if mlsd_image.size != original_image.size:
            mlsd_image = mlsd_image.resize(original_image.size, Image.NEAREST)
        if depth_image.size != original_image.size:
            depth_image = depth_image.resize(original_image.size, Image.NEAREST)
        
        # 2. Metric Depth
        self._analyze_depth_for_measurement(original_image)

        # 3. Settings based on Mode
        num_steps = 15 # Reduced from 20 for faster generation (still good quality)
        if self.is_turbo:
            num_steps = 6 # LCM is fast!
            guidance_scale = 1.0 # LCM needs low guidance
            strength = 0.65 # Lower strength for LCM usually

        # 4. Generate
        generator = torch.Generator(device=self.device)
        if seed != -1:
            generator.manual_seed(seed)
        else:
            generator.seed()

        print(f"Generating (Turbo={self.is_turbo}, Steps={num_steps})...")
        images = self.pipe(
            prompt,
            negative_prompt=negative_prompt,
            image=original_image,
            control_image=[mlsd_image, depth_image],
            controlnet_conditioning_scale=[1.0, 0.8], 
            strength=strength,
            guidance_scale=guidance_scale,
            num_inference_steps=num_steps,
            cross_attention_kwargs={"scale": 1.0}, # For LoRA scale if loaded
            generator=generator
        ).images

        return images[0], mlsd_image, depth_image

    def _analyze_depth_for_measurement(self, image):
        result = self.depth_estimator(image)
        self.depth_map_metric = np.array(result["depth"])
        
    def calibrate_scale(self, point1, point2, real_distance_meters):
        if self.depth_map_metric is None:
            raise ValueError("No image processed yet.")
        x1, y1 = point1
        x2, y2 = point2
        h, w = self.depth_map_metric.shape
        x1, x2 = min(x1, w-1), min(x2, w-1)
        y1, y2 = min(y1, h-1), min(y2, h-1)
        
        pixel_dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        if pixel_dist == 0: return
        self.scale_factor = real_distance_meters / pixel_dist

    def measure_distance(self, point1, point2):
        if self.depth_map_metric is None: return 0.0
        x1, y1 = point1
        x2, y2 = point2
        pixel_dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        return pixel_dist * self.scale_factor
