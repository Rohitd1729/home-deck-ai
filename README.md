# 🏠 Home Deck AI Pro

A professional-grade **Interior Design AI** tool built for architects, designers, and enthusiasts. This application uses state-of-the-art **Stable Diffusion (Realistic Vision V6.0)** combined with **ControlNet** to generate photorealistic interior designs while strictly preserving the room's geometry and structure.

---

## 🚀 **NEW: Flask REST API for ERP Integration**

The project now includes a **Flask REST API** for easy integration with React-based ERP systems and other applications!

### Quick API Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start API server:**
   ```bash
   python api_server.py
   ```

3. **Test the API:**
   ```bash
   curl http://localhost:5000/api/health
   ```

4. **Generate design from React:**
   ```javascript
   const formData = new FormData();
   formData.append('image', imageFile);
   
   const response = await fetch('http://localhost:5000/api/generate', {
     method: 'POST',
     body: formData
   });
   
   const result = await response.json();
   ```

**📚 Documentation:**
- [QUICKSTART.md](QUICKSTART.md) - Installation & setup guide
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Complete API reference
- [REACT_INTEGRATION_GUIDE.md](REACT_INTEGRATION_GUIDE.md) - React/ERP integration examples

---

## ✨ Key Features

*   **📏 Structural Accuracy**: Uses **MLSD (Mobile Line Segment Detection)** ControlNet to lock walls, ceilings, and edges. No warped rooms.
*   **📐 3D Depth Awareness**: Uses **Midas/DPT** Depth estimation to understand scene volume.
*   **🚀 Turbo Mode**: Integrated **LCM-LoRA** (Latent Consistency Model) for ultra-fast generation (4-8 steps, <5 seconds on GPU).
*   **💎 Photorealism**: Built on **Realistic Vision V6.0** for commercial-grade rendering quality.
*   **🔌 REST API**: Flask API for seamless integration with web applications and ERP systems.
*   **⚛️ React Ready**: Complete integration guide and examples for React applications.

---

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

---

## 🚀 Usage

### Option 1: REST API (Recommended for ERP Integration)

**Start the API server:**
```bash
python api_server.py
```

**API Endpoints:**
- `POST /api/generate` - Generate interior design from image
- `GET /api/health` - Check server health
- `GET /api/images/<filename>` - Retrieve generated images

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for details.

### Option 2: Interactive Web App (Gradio)

The standalone Gradio interface for local use:

1.  Run the launcher:
    ```bash
    python app.py
    ```

2.  Open your browser at **http://127.0.0.1:7860**.

3.  **Workflow**:
    *   Upload an image of an empty room or existing interior.
    *   Enter a **Prompt** (e.g., "Modern living room, leather sofa, cinematic lighting, 8k").
    *   *(Optional)* Check **Turbo Mode** for speed.
    *   Click **Generate**.

### Option 3: Batch Processing

To process a folder of images automatically:

1.  Place images in `inputs/`.
2.  Run:
    ```bash
    python main.py
    ```
3.  Results saved to `outputs/`.

---

## 🧠 Technical Details

*   **Base Model**: `SG161222/Realistic_Vision_V6.0_B1_noVAE` (SD 1.5)
*   **ControlNets**:
    *   `lllyasviel/control_v11p_sd15_mlsd` (Lines/Structure)
    *   `lllyasviel/control_v11f1p_sd15_depth` (Depth/Volume)
*   **Accelerator**: `latent-consistency/lcm-lora-sdv1-5` (Turbo Mode)
*   **Optimization**: `xformers` (Memory Efficient Attention) + `DPMSolverMultistepScheduler`.

---

## 🔌 API Integration Examples

### React Component
```jsx
const handleGenerate = async (imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  
  const response = await fetch('http://localhost:5000/api/generate', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  setGeneratedImage(`http://localhost:5000${result.result_url}`);
};
```

### Python Client
```python
import requests

with open('room.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5000/api/generate', files=files)
    result = response.json()
    print(result['result_url'])
```

See [REACT_INTEGRATION_GUIDE.md](REACT_INTEGRATION_GUIDE.md) for complete examples.

---

## 📁 Project Structure

```
home-deck-ai/
├── api/                   # Flask API package
│   ├── routes.py          # API endpoints
│   ├── model_manager.py   # Model lifecycle management
│   └── utils.py           # Helper functions
├── api_server.py          # Flask server entry point
├── app.py                 # Gradio web interface
├── main.py                # Batch processing script
├── interior_designer.py   # Core AI logic
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── API_DOCUMENTATION.md   # API reference
├── REACT_INTEGRATION_GUIDE.md  # React examples
└── QUICKSTART.md          # Quick start guide
```

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)

---

## 🆘 Support

- **API Issues**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md#troubleshooting)
- **React Integration**: See [REACT_INTEGRATION_GUIDE.md](REACT_INTEGRATION_GUIDE.md#troubleshooting)
- **General Setup**: See [QUICKSTART.md](QUICKSTART.md#troubleshooting)
