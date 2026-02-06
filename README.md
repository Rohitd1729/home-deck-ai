# 🏠 Home Deck AI Pro

A professional-grade **Interior Design AI** tool built for architects, designers, and enthusiasts. This application uses state-of-the-art **Stable Diffusion (Realistic Vision V6.0)** combined with **ControlNet** to generate photorealistic interior designs while strictly preserving the room's geometry and structure.

![Demo](https://via.placeholder.com/800x400?text=Home+Deck+AI+Demo)

## ✨ Key Features

*   **📏 Structural Accuracy**: Uses **MLSD (Mobile Line Segment Detection)** ControlNet to lock walls, ceilings, and edges. No warped rooms.
*   **📐 3D Depth Awareness**: Uses **Midas/DPT** Depth estimation to understand scene volume.
*   **🚀 Turbo Mode**: Integrated **LCM-LoRA** (Latent Consistency Model) for ultra-fast generation (4-8 steps, <5 seconds on GPU).
*   **💎 Photorealism**: Built on **Realistic Vision V6.0** for commercial-grade rendering quality.
*   **📏 Measurements Tool**: Interactive tool to calibrate and measure real-world distances directly on the image.
*   **🎨 Custom Styles**: Support for external LoRA models to fine-tune specific styles (e.g., "Minimalist", "Industrial").

## 🛠️ Installation

### Prerequisites
*   Python 3.10+
*   NVIDIA GPU with 6GB+ VRAM (Recommended)
    *   *Note: Works on CPU but slower.*

### Setup
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Rohitd1729/home-deck-ai.git
    cd home-deck-ai
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *If you have an NVIDIA GPU, ensure PyTorch is installed with CUDA support:*
    ```bash
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
    ```

## 🚀 Usage

### Interactive Web App (Gradio)
The easiest way to use the tool.
1.  Run the launcher:
    ```bash
    .\run_app.bat
    ```
    *Or manually:* `python app.py`

2.  Open your browser at **http://127.0.0.1:7860**.

3.  **Workflow**:
    *   Upload an image of an empty room or existing interior.
    *   Enter a **Prompt** (e.g., "Modern living room, leather sofa, cinematc lighting, 8k").
    *   *(Optional)* Check **Turbo Mode** for speed.
    *   Click **Generate**.

### Batch Processing
To process a folder of images automatically:
1.  Place images in `inputs/`.
2.  Run:
    ```bash
    python main.py
    ```
3.  Results saved to `outputs/`.

## 🧠 Technical Details

*   **Base Model**: `SG161222/Realistic_Vision_V6.0_B1_noVAE` (SD 1.5)
*   **ControlNets**:
    *   `lllyasviel/control_v11p_sd15_mlsd` (Lines/Structure)
    *   `lllyasviel/control_v11f1p_sd15_depth` (Depth/Volume)
*   **Accelerator**: `latent-consistency/lcm-lora-sdv1-5` (Turbo Mode)
*   **Optimization**: `xformers` (Memory Efficient Attention) + `DPMSolverMultistepScheduler`.

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)
