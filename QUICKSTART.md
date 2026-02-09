# 🚀 Quick Start Guide - Flask API

## Installation

### 1. Install Dependencies

```bash
cd c:\Users\rohit\Downloads\home-deck-ai-main\home-deck-ai-main
pip install -r requirements.txt
```

**Note:** If you have an NVIDIA GPU, ensure PyTorch with CUDA support:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### 2. Configure Environment (Optional)

Copy the example environment file:
```bash
copy .env.example .env
```

Edit `.env` to set your React ERP URL:
```
CORS_ORIGINS=http://localhost:3000,http://your-erp-url.com
```

---

## Running the API Server

Start the Flask server:

```bash
python api_server.py
```

**Expected Output:**
```
============================================================
🏠 Home Deck AI - Flask API Server
============================================================
✓ Turbo Mode: ENABLED (Fast generation)
✓ Device: cuda
✓ CORS Origins: http://localhost:3000
============================================================
API Endpoints:
  • POST /api/generate - Generate interior design
  • GET  /api/health   - Health check
  • GET  /api/images/<filename> - Serve generated images
============================================================
Starting server on http://127.0.0.1:5000
============================================================
```

---

## Testing the API

### Test 1: Health Check

```bash
curl http://localhost:5000/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "model_loaded": false,
  "turbo_mode": false,
  "device": "cuda"
}
```

*(Model loads on first image generation request)*

### Test 2: Generate Design

Find a test image or use one of your room photos, then:

```bash
curl -X POST http://localhost:5000/api/generate \
  -F "image=@path/to/your/room.jpg"
```

**Expected Response:**
```json
{
  "success": true,
  "result_url": "/api/images/design_abc123.png",
  "structure_map_url": "/api/images/structure_abc123.png",
  "depth_map_url": "/api/images/depth_abc123.png",
  "processing_time": 4.5,
  "turbo_mode": true
}
```

### Test 3: View Generated Image

Open in browser:
```
http://localhost:5000/api/images/design_abc123.png
```

---

## React Integration

See **[REACT_INTEGRATION_GUIDE.md](REACT_INTEGRATION_GUIDE.md)** for detailed React examples.

**Quick snippet:**

```javascript
const formData = new FormData();
formData.append('image', imageFile);

const response = await fetch('http://localhost:5000/api/generate', {
  method: 'POST',
  body: formData
});

const result = await response.json();
// Use result.result_url to display the generated image
```

---

## API Documentation

See **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** for complete endpoint reference.

---

## Troubleshooting

### GPU Out of Memory
- Close other GPU applications
- Or use CPU mode: Set `DEVICE=cpu` in `.env`

### CORS Errors in React
- Add your React URL to `CORS_ORIGINS` in `.env`
- Restart Flask server

### Slow Generation
- First request loads the model (~20-30 seconds)
- Subsequent requests are fast (~5 seconds with turbo)
- On CPU, expect 60-120 seconds per request

---

## File Structure

```
home-deck-ai-main/
├── api/
│   ├── routes.py          # API endpoints
│   ├── model_manager.py   # Model handling
│   └── utils.py           # Helper functions
├── uploads/               # Temporary uploads (auto-created)
├── outputs/               # Generated results (auto-created)
├── api_server.py          # Server entry point
├── config.py              # Configuration
├── interior_designer.py   # AI core
├── requirements.txt       # Dependencies
└── .env                   # Environment variables (optional)
```

---

## Production Deployment

For production deployment, consider:

1. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 api_server:app
   ```

2. **Environment variables:**
   - Set proper `CORS_ORIGINS`
   - Set `FLASK_DEBUG=False`
   - Use strong `SECRET_KEY`
   - Optional: Set `API_KEY` for authentication

3. **Reverse proxy:**
   - Use Nginx or Apache in front of Flask
   - Handle SSL/TLS certificates

4. **Resource management:**
   - Monitor GPU memory
   - Implement request queuing for concurrent requests
   - Set up file cleanup cron jobs

---

## Next Steps

1. ✅ API is ready for integration
2. 📱 Integrate into your React ERP system
3. 🎨 Customize prompts for your use case
4. 🚀 Deploy to production
