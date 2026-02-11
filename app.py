import gradio as gr
import numpy as np
from PIL import Image
from interior_designer import InteriorDesigner

# Initialize generic
designer = None

# ===== CUSTOM PROMPT TEMPLATES =====
DESIGN_STYLES = {
    "Modern Minimalist": {
        "prompt": "Modern minimalist interior, clean lines, neutral color palette, sleek furniture, open space, natural light, contemporary design, professional photography, 8k, high quality",
        "negative": "clutter, ornate details, dark, cramped, low quality, blur"
    },
    "Scandinavian": {
        "prompt": "Scandinavian interior design, light wood, white walls, cozy textiles, minimalist furniture, hygge atmosphere, natural materials, bright and airy, 8k, professional photography",
        "negative": "dark colors, heavy furniture, ornate, clutter, low quality"
    },
    "Industrial": {
        "prompt": "Industrial loft interior, exposed brick walls, concrete floors, metal fixtures, Edison bulbs, leather furniture, urban style, raw materials, dramatic lighting, 8k, photorealistic",
        "negative": "soft colors, traditional, ornate, low quality, blur"
    },
    "Bohemian": {
        "prompt": "Bohemian interior design, vibrant colors, eclectic mix, plants, textured fabrics, macrame, vintage furniture, artistic, cozy atmosphere, natural light, 8k, professional photography",
        "negative": "minimal, sterile, modern, low quality, monochrome"
    },
    "Luxury Modern": {
        "prompt": "Luxury modern interior, marble surfaces, gold accents, designer furniture, crystal chandelier, premium materials, sophisticated, elegant, cinematic lighting, 8k, ultra detailed",
        "negative": "cheap, simple, minimal, low quality, blur, distortion"
    },
    "Mid-Century Modern": {
        "prompt": "Mid-century modern interior, teak wood furniture, geometric patterns, warm tones, retro vibes, iconic designer pieces, clean lines, vintage charm, natural light, 8k, professional photography",
        "negative": "contemporary, industrial, ornate, low quality"
    },
    "Coastal": {
        "prompt": "Coastal interior design, light blue and white palette, natural textures, driftwood, nautical accents, airy and bright, beach house vibes, relaxed atmosphere, 8k, professional photography",
        "negative": "dark, heavy, urban, industrial, low quality"
    },
    "Rustic Farmhouse": {
        "prompt": "Rustic farmhouse interior, reclaimed wood, vintage decor, white shiplap, farmhouse sink, cozy textiles, warm lighting, country charm, natural materials, 8k, professional photography",
        "negative": "modern, sleek, industrial, low quality, urban"
    },
    "Japanese Zen": {
        "prompt": "Japanese zen interior, minimalist design, natural wood, tatami mats, shoji screens, neutral colors, peaceful atmosphere, balance and harmony, natural light, 8k, serene",
        "negative": "clutter, bright colors, ornate, western style, low quality"
    },
    "Art Deco": {
        "prompt": "Art Deco interior, geometric patterns, rich colors, gold accents, luxurious fabrics, glamorous, vintage elegance, bold contrasts, dramatic lighting, 8k, sophisticated",
        "negative": "minimal, rustic, simple, low quality, modern"
    }
}

ROOM_TYPES = {
    "Living Room": "spacious living room, comfortable seating area, coffee table, entertainment center",
    "Bedroom": "cozy bedroom, comfortable bed, nightstands, soft lighting, relaxing atmosphere",
    "Kitchen": "modern kitchen, functional layout, countertops, cabinets, appliances, island",
    "Bathroom": "elegant bathroom, vanity, shower, bathtub, tiles, fixtures",
    "Dining Room": "elegant dining room, dining table, chairs, chandelier, table setting",
    "Home Office": "productive home office, desk, ergonomic chair, shelving, organized workspace",
    "Nursery": "warm nursery, crib, soft colors, playful elements, cozy atmosphere",
    "Entryway": "welcoming entryway, console table, mirror, organized storage, inviting"
}

QUALITY_ENHANCERS = [
    "8k resolution",
    "professional photography",
    "photorealistic",
    "high detail",
    "cinematic lighting",
    "ultra realistic",
    "award winning design",
    "architectural digest"
]

def get_designer():
    global designer
    if designer is None:
        try:
            # Using the new Realistic Vision V6 model
            designer = InteriorDesigner(device="cuda") 
        except Exception as e:
            return None, f"Error initializing: {e}"
    return designer, "Model Loaded"

def toggle_turbo(turbo_on):
    model, msg = get_designer()
    if model:
        model.enable_turbo(turbo_on)
        return f"Turbo Mode: {'ON' if turbo_on else 'OFF'}"
    return "Model not loaded"

def build_custom_prompt(style, room_type, additional_elements, quality_level):
    """Build a custom prompt from selected options"""
    prompt_parts = []
    
    # Add room type
    if room_type and room_type in ROOM_TYPES:
        prompt_parts.append(ROOM_TYPES[room_type])
    
    # Add style base
    if style and style in DESIGN_STYLES:
        style_prompt = DESIGN_STYLES[style]["prompt"]
        # Extract key style elements (first part before photography quality)
        style_elements = style_prompt.split(',')[:6]
        prompt_parts.extend(style_elements)
    
    # Add additional custom elements
    if additional_elements and additional_elements.strip():
        prompt_parts.append(additional_elements.strip())
    
    # Add quality enhancers based on level
    if quality_level == "High":
        prompt_parts.extend(QUALITY_ENHANCERS[:4])
    elif quality_level == "Ultra":
        prompt_parts.extend(QUALITY_ENHANCERS)
    
    return ", ".join(prompt_parts)

def apply_preset_style(style):
    """Apply a preset style and return prompt and negative prompt"""
    if style in DESIGN_STYLES:
        return DESIGN_STYLES[style]["prompt"], DESIGN_STYLES[style]["negative"]
    return "", ""

def generate(image, prompt, neg_prompt, turbo_mode, custom_lora):
    model, msg = get_designer()
    if model is None: return None, msg
    if image is None: return None, "Upload an image."
    
    # Check Turbo
    if model.is_turbo != turbo_mode:
        model.enable_turbo(turbo_mode)
        
    # Check LoRA
    if custom_lora and custom_lora.strip():
        try:
            model.load_custom_lora(custom_lora.strip())
        except Exception as e:
            print(f"Failed to load LoRA: {e}")

    temp_path = "temp_input.png"
    Image.fromarray(image).save(temp_path)
    
    try:
        result, _, _ = model.generate_design(
            temp_path, prompt, neg_prompt
        )
        return result, "Done"
    except Exception as e:
        return None, str(e)



# Custom CSS for Apple-like modern design
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
}

/* Header styling */
h1 {
    font-size: 48px !important;
    font-weight: 700 !important;
    letter-spacing: -1px !important;
    background: linear-gradient(135deg, #1a1a1a 0%, #4a4a4a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px !important;
}

.subtitle {
    font-size: 18px !important;
    font-weight: 400 !important;
    color: #666 !important;
    margin-bottom: 40px !important;
}

/* Clean card design */
.block {
    border-radius: 16px !important;
    border: 1px solid #e5e5e7 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    background: #ffffff !important;
}

/* Tab styling */
.tab-nav button {
    font-weight: 500 !important;
    padding: 12px 24px !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}

.tab-nav button[aria-selected="true"] {
    background: #000000 !important;
    color: #ffffff !important;
}

/* Input fields */
textarea, input {
    border-radius: 12px !important;
    border: 1px solid #d2d2d7 !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
    transition: all 0.2s ease !important;
}

textarea:focus, input:focus {
    border-color: #0071e3 !important;
    box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1) !important;
}

/* Buttons */
button {
    border-radius: 12px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    border: none !important;
    padding: 14px 28px !important;
}

.primary {
    background: linear-gradient(135deg, #0071e3 0%, #005bb5 100%) !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

.primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(0, 113, 227, 0.3) !important;
}

.secondary {
    background: #f5f5f7 !important;
    color: #1d1d1f !important;
}

.secondary:hover {
    background: #e8e8ed !important;
}

/* Labels */
label {
    font-weight: 500 !important;
    color: #1d1d1f !important;
    font-size: 14px !important;
    margin-bottom: 8px !important;
}

/* Radio buttons and dropdowns */
.radio-group label {
    font-weight: 400 !important;
}

/* Image upload area */
.image-container {
    border-radius: 16px !important;
    border: 2px dashed #d2d2d7 !important;
    transition: all 0.2s ease !important;
}

.image-container:hover {
    border-color: #0071e3 !important;
}

/* Accordion */
.accordion {
    border-radius: 12px !important;
    border: 1px solid #e5e5e7 !important;
    margin-top: 12px !important;
}

/* Status messages */
.output-class {
    border-radius: 12px !important;
    background: #f5f5f7 !important;
    padding: 16px !important;
}

/* Clean spacing */
.gap {
    gap: 20px !important;
}

/* Remove excessive shadows */
.shadow {
    box-shadow: none !important;
}

/* Minimize visual noise */
.gr-form {
    border: none !important;
    background: transparent !important;
}
"""

# Create theme
custom_theme = gr.themes.Base(
    primary_hue="blue",
    secondary_hue="gray",
    neutral_hue="gray",
    font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
).set(
    button_primary_background_fill="#0071e3",
    button_primary_background_fill_hover="#005bb5",
    button_primary_text_color="white",
    button_secondary_background_fill="#f5f5f7",
    button_secondary_text_color="#1d1d1f",
    input_border_color="#d2d2d7",
    input_border_color_focus="#0071e3",
)

with gr.Blocks(title="Home Deck AI", theme=custom_theme, css=custom_css) as app:
    
    # Header
    gr.HTML("""
        <div style="text-align: center; margin-bottom: 60px; margin-top: 40px;">
            <h1 style="font-size: 56px; font-weight: 700; letter-spacing: -2px; margin-bottom: 16px; color: #1d1d1f;">
                Home Deck AI
            </h1>
            <p style="font-size: 21px; color: #86868b; font-weight: 400; max-width: 600px; margin: 0 auto;">
                Transform your spaces with AI-powered interior design
            </p>
        </div>
    """)
    
    with gr.Row(equal_height=True):
        # Left Column - Input
        with gr.Column(scale=1):
            input_img = gr.Image(
                label="Upload Image",
                type="numpy",
                height=400
            )
            
            # Tabs for prompt design
            with gr.Tabs():
                with gr.Tab("Preset Styles"):
                    preset_style = gr.Radio(
                        choices=list(DESIGN_STYLES.keys()),
                        value="Modern Minimalist",
                        label="Choose Style",
                        interactive=True
                    )
                    apply_preset_btn = gr.Button("Apply Style", variant="secondary", size="sm")
                
                with gr.Tab("Custom"):
                    room_type = gr.Dropdown(
                        choices=list(ROOM_TYPES.keys()),
                        value="Living Room",
                        label="Room Type"
                    )
                    style_select = gr.Dropdown(
                        choices=list(DESIGN_STYLES.keys()),
                        value="Modern Minimalist",
                        label="Style"
                    )
                    additional_elements = gr.Textbox(
                        label="Additional Elements",
                        placeholder="fireplace, large windows, plants, artwork",
                        lines=2
                    )
                    quality_level = gr.Radio(
                        choices=["Standard", "High", "Ultra"],
                        value="High",
                        label="Quality"
                    )
                    build_prompt_btn = gr.Button("Build Prompt", variant="secondary", size="sm")
                
                with gr.Tab("Advanced"):
                    gr.Markdown("Write your own prompt for complete control")
            
            # Prompt fields
            prompt = gr.Textbox(
                label="Prompt",
                value="Best quality, modern minimalist interior, photorealistic, 8k",
                lines=3
            )
            neg = gr.Textbox(
                label="Negative Prompt",
                value="low quality, blur, distortion",
                lines=2
            )
            
            # Advanced options
            with gr.Accordion("Settings", open=False):
                turbo = gr.Checkbox(label="Turbo Mode", value=False)
                lora_path = gr.Textbox(
                    label="Custom LoRA", 
                    placeholder="username/model-name"
                )
            
            gen_btn = gr.Button("Generate", variant="primary", size="lg")
        
        # Right Column - Output
        with gr.Column(scale=1):
            out_img = gr.Image(
                label="Generated Design",
                type="pil",
                height=400
            )
            status = gr.Textbox(label="Status", interactive=False)

    # Functions
    def on_apply_preset(style):
        prompt_text, neg_text = apply_preset_style(style)
        return prompt_text, neg_text
    
    def on_build_custom(style, room, elements, quality):
        prompt_text = build_custom_prompt(style, room, elements, quality)
        neg_text = DESIGN_STYLES.get(style, {}).get("negative", "low quality, blur, distortion")
        return prompt_text, neg_text
    
    # Event handlers
    apply_preset_btn.click(
        on_apply_preset,
        inputs=[preset_style],
        outputs=[prompt, neg]
    )
    
    build_prompt_btn.click(
        on_build_custom,
        inputs=[style_select, room_type, additional_elements, quality_level],
        outputs=[prompt, neg]
    )
    
    gen_btn.click(
        generate,
        inputs=[input_img, prompt, neg, turbo, lora_path],
        outputs=[out_img, status]
    )
    
    # Tips section
    gr.HTML("""
        <div style="margin-top: 60px; padding: 40px; background: #f5f5f7; border-radius: 16px;">
            <h3 style="font-size: 24px; font-weight: 600; margin-bottom: 20px; color: #1d1d1f;">Tips for Best Results</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; color: #1d1d1f;">
                <div>
                    <h4 style="font-weight: 600; margin-bottom: 8px;">Lighting</h4>
                    <p style="color: #86868b; font-size: 14px; line-height: 1.6;">
                        Try "warm ambient lighting" for cozy spaces or "natural sunlight" for bright interiors
                    </p>
                </div>
                <div>
                    <h4 style="font-weight: 600; margin-bottom: 8px;">Materials</h4>
                    <p style="color: #86868b; font-size: 14px; line-height: 1.6;">
                        Specify materials like "marble countertops" or "wooden floors" for better accuracy
                    </p>
                </div>
                <div>
                    <h4 style="font-weight: 600; margin-bottom: 8px;">Quality</h4>
                    <p style="color: #86868b; font-size: 14px; line-height: 1.6;">
                        Use keywords like "8k, photorealistic" for professional-grade results
                    </p>
                </div>
            </div>
        </div>
    """)

if __name__ == "__main__":
    app.launch()

