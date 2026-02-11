# FastAPI Implementation Guide - Home Deck AI Backend

## 📋 Table of Contents
- [What is FastAPI?](#what-is-fastapi)
- [Why FastAPI for This Project?](#why-fastapi-for-this-project)
- [Architecture Overview](#architecture-overview)
- [Server Setup Decision](#server-setup-decision)
- [Implementation Steps](#implementation-steps)
- [API Endpoints Design](#api-endpoints-design)
- [Code Examples](#code-examples)
- [Frontend Integration](#frontend-integration)
- [Testing Strategy](#testing-strategy)
- [Deployment Guide](#deployment-guide)

---

## What is FastAPI?

**FastAPI** is a modern, fast (high-performance) Python web framework for building APIs.

### Key Features:
- ✅ **Fast**: High performance, on par with NodeJS and Go
- ✅ **Easy**: Simple to learn and use
- ✅ **Auto Documentation**: Generates interactive API docs automatically
- ✅ **Type Hints**: Uses Python type hints for validation
- ✅ **Async Support**: Handles concurrent requests efficiently

### Think of it as:
```
Flask/Django (old school) → FastAPI (modern, faster, better)
```

---

## Why FastAPI for This Project?

### Your Current Situation:
- ✅ You have a **Gradio web app** (works locally)
- ❌ Client wants it in their **React ERP system**
- ❌ Gradio UI can't be embedded in React

### Solution:
**Convert to FastAPI** = Create a REST API that React can call

```
Before (Gradio):
User → Gradio Web UI → AI Model → Result

After (FastAPI):
React Frontend → FastAPI Backend → AI Model → JSON Response → React
```

---

## Architecture Overview

### High-Level Flow

```
┌─────────────────────────────────────┐
│   CLIENT'S REACT ERP SYSTEM        │
│                                     │
│   User uploads image                │
│   Selects "Modern Minimalist"       │
│   Clicks "Generate"                 │
│                                     │
│   ↓ Makes HTTP POST Request         │
└─────────────────────────────────────┘
            ↓
            ↓ HTTP/REST API
            ↓
┌─────────────────────────────────────┐
│   YOUR FASTAPI BACKEND              │
│   (Port 8000)                       │
│                                     │
│   Endpoints:                        │
│   • POST /generate-design           │
│   • GET /styles                     │
│   • GET /room-types                 │
│   • GET /health                     │
│                                     │
│   ↓ Calls AI Model                  │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│   INTERIOR DESIGNER AI              │
│   (Your existing code)              │
│   • Stable Diffusion                │
│   • ControlNet                      │
│   • CUDA/GPU                        │
└─────────────────────────────────────┘
```

---

## Server Setup Decision

### Option 1: Separate Backend Server ⭐ **RECOMMENDED**

```
┌─────────────────┐         ┌─────────────────┐
│  Frontend       │  HTTP   │  Backend        │
│  Server         │◄───────►│  Server         │
│                 │         │                 │
│  React App      │         │  FastAPI        │
│  Port 3000      │         │  Port 8000      │
│  No GPU needed  │         │  NEEDS GPU      │
└─────────────────┘         └─────────────────┘
```

**Why Separate?**
- ✅ React doesn't need GPU, FastAPI does
- ✅ Can scale independently
- ✅ Cleaner separation
- ✅ Cost-effective (only GPU server for AI)

**Setup:**
- Server 1: Any web server (Nginx + React build)
- Server 2: GPU server (Python + FastAPI + CUDA)

---

### Option 2: Same Server, Different Ports

```
┌─────────────────────────────────────┐
│        Single GPU Server            │
│                                     │
│  ┌──────────┐    ┌──────────┐     │
│  │  React   │    │ FastAPI  │     │
│  │ Port 3000│    │Port 8000 │     │
│  └──────────┘    └──────────┘     │
└─────────────────────────────────────┘
```

**Good for:**
- ✅ Development/testing
- ✅ Simpler initial setup

**Bad for:**
- ❌ Wastes GPU on React
- ❌ All eggs in one basket

---

## Implementation Steps

### Step 1: Create FastAPI Backend File

**File:** `api.py`

**What it needs:**
1. Import FastAPI
2. Create app instance
3. Add CORS (so React can access)
4. Define endpoints (routes)
5. Reuse your existing `interior_designer.py`

---

### Step 2: Install Dependencies

```bash
pip install fastapi uvicorn python-multipart aiofiles
```

**What each does:**
- `fastapi`: The framework
- `uvicorn`: Server to run FastAPI
- `python-multipart`: Handle file uploads
- `aiofiles`: Async file operations

---

### Step 3: Configure CORS

CORS = Cross-Origin Resource Sharing

**Why needed?** React (port 3000) calling API (port 8000) = different origins

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React URL
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Step 4: Create Endpoints

**Basic structure:**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/styles")
def get_styles():
    return {"styles": ["Modern", "Industrial", ...]}

@app.post("/generate-design")
def generate(image: UploadFile, style: str):
    # Your AI code here
    return {"image_url": "generated.png"}
```

---

## API Endpoints Design

### 1. Health Check

```
GET /health
```

**Purpose:** Check if API and model are loaded

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda"
}
```

**Frontend use:** Check before allowing user to upload image

---

### 2. Get Styles

```
GET /styles
```

**Purpose:** Get list of all design styles

**Response:**
```json
{
  "styles": [
    {
      "name": "Modern Minimalist",
      "prompt": "Modern minimalist interior..."
    },
    {
      "name": "Scandinavian",
      "prompt": "Scandinavian interior..."
    }
  ]
}
```

**Frontend use:** Populate dropdown menu

---

### 3. Get Room Types

```
GET /room-types
```

**Purpose:** Get list of all room types

**Response:**
```json
{
  "room_types": [
    "Living Room",
    "Bedroom",
    "Kitchen",
    ...
  ]
}
```

**Frontend use:** Populate room type selector

---

### 4. Generate Design (Main Endpoint)

```
POST /generate-design
```

**Input (Form Data):**
```
image: File
style: string
room_type: string
quality_level: string
turbo_mode: boolean
```

**Response:**
```json
{
  "status": "success",
  "generated_image_url": "/outputs/image_123.png",
  "prompt_used": "Modern minimalist...",
  "request_id": "abc123"
}
```

**How it works:**
1. Receive image from React
2. Save temporarily
3. Call your `InteriorDesigner` class
4. Generate design
5. Return image URL

---

## Code Examples

### Minimal FastAPI Backend

```python
# api.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from interior_designer import InteriorDesigner

app = FastAPI()

# CORS - Update with your React URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI model
designer = None

def get_designer():
    global designer
    if designer is None:
        designer = InteriorDesigner(device="cuda")
    return designer

@app.get("/health")
def health_check():
    model = get_designer()
    return {"status": "healthy", "model_loaded": True}

@app.get("/styles")
def get_styles():
    styles = [
        "Modern Minimalist",
        "Scandinavian",
        "Industrial",
        # ... rest of styles
    ]
    return {"styles": styles}

@app.post("/generate-design")
async def generate_design(
    image: UploadFile = File(...),
    style: str = Form(...),
    room_type: str = Form(...)
):
    # Save uploaded image
    image_path = f"uploads/{image.filename}"
    with open(image_path, "wb") as f:
        f.write(await image.read())
    
    # Build prompt
    prompt = f"{room_type}, {style} style, 8k, photorealistic"
    
    # Generate design
    model = get_designer()
    result, _, _ = model.generate_design(
        image_path,
        prompt=prompt,
        negative_prompt="low quality, blur"
    )
    
    # Save result
    output_path = "outputs/generated_123.png"
    result.save(output_path)
    
    return {
        "status": "success",
        "generated_image_url": f"/outputs/generated_123.png"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Run the Server

```bash
python api.py
```

API runs on: `http://localhost:8000`

Auto docs at: `http://localhost:8000/docs` ← **Interactive testing interface!**

---

## Frontend Integration

### How Frontend Intern Will Use Your API

```javascript
// React component example
const InteriorDesignTool = () => {
  const [imageFile, setImageFile] = useState(null);
  const [style, setStyle] = useState('Modern Minimalist');
  const [generatedImage, setGeneratedImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateDesign = async () => {
    setLoading(true);
    
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('style', style);
    formData.append('room_type', 'Living Room');
    
    try {
      const response = await fetch('http://localhost:8000/generate-design', {
        method: 'POST',
        body: formData,
      });
      
      const result = await response.json();
      
      if (result.status === 'success') {
        // Display generated image
        setGeneratedImage(`http://localhost:8000${result.generated_image_url}`);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={(e) => setImageFile(e.target.files[0])} />
      <select value={style} onChange={(e) => setStyle(e.target.value)}>
        <option>Modern Minimalist</option>
        <option>Scandinavian</option>
        {/* ... */}
      </select>
      <button onClick={generateDesign} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Design'}
      </button>
      {generatedImage && <img src={generatedImage} alt="Generated" />}
    </div>
  );
};
```

**YOUR JOB:** Provide API endpoints that work  
**FRONTEND INTERN'S JOB:** Build React UI that calls your endpoints

---

## Testing Strategy

### 1. Test with Interactive Docs

FastAPI auto-generates docs at `/docs`

1. Go to `http://localhost:8000/docs`
2. Click on endpoint
3. Click "Try it out"
4. Upload image, fill parameters
5. Click "Execute"
6. See response

**No code needed to test!**

---

### 2. Test with cURL

```bash
# Health check
curl http://localhost:8000/health

# Get styles
curl http://localhost:8000/styles

# Generate design
curl -X POST http://localhost:8000/generate-design \
  -F "image=@room.jpg" \
  -F "style=Modern Minimalist" \
  -F "room_type=Living Room"
```

---

### 3. Test with Postman

1. Download Postman
2. Create new request
3. Set to POST
4. URL: `http://localhost:8000/generate-design`
5. Body → form-data
6. Add: `image` (file), `style` (text), etc.
7. Send

---

## Deployment Guide

### Development (Your Computer)

```bash
# Terminal 1: Run FastAPI
python api.py

# Terminal 2: Run React (frontend intern's job)
cd react-app
npm start
```

---

### Production (Separate Servers)

**Backend Server (GPU required):**
```bash
# Install dependencies
pip install -r requirements.txt
pip install fastapi uvicorn[standard]

# Run FastAPI (production mode)
uvicorn api:app --host 0.0.0.0 --port 8000
```

**Frontend Server:**
```bash
# Build React app
npm run build

# Serve with Nginx or similar
```

---

## Your Responsibilities vs Frontend Intern

### ✅ YOUR JOB (Backend):
1. Create `api.py` with endpoints
2. Handle image uploads
3. Run AI model when endpoint is called
4. Return generated images
5. Write API documentation
6. Test endpoints work correctly

### ✅ FRONTEND INTERN'S JOB:
1. Build React UI (buttons, dropdowns, upload)
2. Make HTTP calls to your API
3. Display generated images
4. Handle loading states
5. Integrate into existing ERP

---

## Quick Start Checklist

When you're ready to implement:

- [ ] Create `api.py` file
- [ ] Install FastAPI: `pip install fastapi uvicorn python-multipart`
- [ ] Add CORS middleware
- [ ] Create `/health` endpoint
- [ ] Create `/styles` endpoint
- [ ] Create `/generate-design` endpoint
- [ ] Test with `/docs` interactive interface
- [ ] Share API documentation with frontend intern
- [ ] Test integration with React frontend

---

## Common Questions

**Q: Do I need to learn React?**  
A: No! You only need to create the API. Frontend intern handles React.

**Q: How do React and FastAPI talk?**  
A: React makes HTTP requests to your FastAPI endpoints (like visiting a website).

**Q: Where does the AI model run?**  
A: On your FastAPI server when an endpoint is called.

**Q: What if I don't have a GPU server?**  
A: Test locally first. For production, client needs to provide GPU server.

**Q: How do I know if it's working?**  
A: Go to `http://localhost:8000/docs` - you'll see interactive API docs!

---

## Next Steps

1. **Review this guide** - Make sure you understand the architecture
2. **Decide on server setup** - Same or separate? (Recommend separate)
3. **Implement `api.py`** - When ready, I'll help you write it
4. **Test endpoints** - Use `/docs` interface
5. **Coordinate with frontend** - Share API docs
6. **Deploy** - Set up on GPU server

---

## Summary

**What is FastAPI?** A modern Python framework for building APIs

**Why use it?** To connect your AI model to the React frontend

**Your role:** Create API endpoints that React can call

**Frontend's role:** Build UI that calls your API

**Server setup:** Separate backend (with GPU) + frontend (no GPU) = Best approach

**Testing:** Use auto-generated docs at `/docs`

**Timeline:** 3-5 days of work

---

**You're in great shape!** The hard part (AI model) is done. Now just wrap it in FastAPI so React can use it. 🚀
