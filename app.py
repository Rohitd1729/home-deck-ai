import gradio as gr
import numpy as np
from PIL import Image
from interior_designer import InteriorDesigner

# Initialize generic
designer = None

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

# Measurement logic remains same
points = []
def on_select(evt: gr.SelectData, image):
    global points
    points.append((evt.index[0], evt.index[1]))
    vis = Image.fromarray(image).copy()
    vis_arr = np.array(vis)
    import cv2
    for p in points:
        cv2.circle(vis_arr, p, 5, (255,0,0), -1)
    if len(points) >= 2:
        cv2.line(vis_arr, points[-2], points[-1], (0,255,0), 2)
    return vis_arr

def calibrate(dist):
    global points
    if len(points)<2: return "Need 2 points"
    model, _ = get_designer()
    if model:
        model.calibrate_scale(points[-2], points[-1], float(dist))
        return f"Calibrated: {model.scale_factor:.3f} m/px"
    return "Error"

def measure():
    global points
    if len(points)<2: return "Need 2 points"
    model, _ = get_designer()
    if model:
        d = model.measure_distance(points[-2], points[-1])
        return f"Distance: {d:.2f} m"
    return "Error"

def clear():
    global points
    points = []
    return None

with gr.Blocks(title="Home Deck AI Pro") as app:
    gr.Markdown("# 🏠 Standard + Turbo Interior Design AI")
    
    with gr.Row():
        with gr.Column():
            input_img = gr.Image(label="Input", type="numpy")
            prompt = gr.Textbox(label="Prompt", value="Best quality, modern minimalist interior, photorealistic, 8k")
            neg = gr.Textbox(label="Negative", value="low quality, blur, distortion")
            
            with gr.Accordion("Advanced Settings", open=True):
                turbo = gr.Checkbox(label="⚡ Turbo Mode (Fast Generation)", value=False)
                lora_path = gr.Textbox(label="Custom LoRA Path (HuggingFace ID)", placeholder="e.g., latent-consistency/lcm-lora-sdv1-5")
                
            gen_btn = gr.Button("Generate", variant="primary")
        
        with gr.Column():
            out_img = gr.Image(label="Result", type="pil")
            status = gr.Textbox(label="Status")

    gen_btn.click(generate, inputs=[input_img, prompt, neg, turbo, lora_path], outputs=[out_img, status])
    
    # Measurement UI
    gr.Markdown("## 📏 Measurements")
    input_img.select(on_select, [input_img], [input_img])
    
    with gr.Row():
        dist_in = gr.Number(label="Ref Distance (m)", value=3.0)
        cal_btn = gr.Button("Calibrate")
        meas_btn = gr.Button("Measure")
        clr_btn = gr.Button("Clear")
        res = gr.Textbox(label="Result")
        
    cal_btn.click(calibrate, [dist_in], [res])
    meas_btn.click(measure, [], [res])
    clr_btn.click(clear, [], [input_img])

if __name__ == "__main__":
    app.launch()
