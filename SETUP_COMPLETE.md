# 🎉 Flask API Setup Complete!

## ✅ What's Been Created

Your Home Deck AI project has been successfully converted into a Flask REST API for integration with your React-based ERP system!

### New Files Created

1. **API Core:**
   - `api_server.py` - Flask application entry point
   - `config.py` - Centralized configuration
   - `api/routes.py` - API endpoints (POST /api/generate)
   - `api/model_manager.py` - Singleton model handler
   - `api/utils.py` - Helper functions

2. **Documentation:**
   - `API_DOCUMENTATION.md` - Complete API reference
   - `REACT_INTEGRATION_GUIDE.md` - React integration examples
   - `QUICKSTART.md` - Quick start guide
   - `README.md` - Updated with API information

3. **Utilities:**
   - `test_api.py` - API testing script
   - `validate_setup.py` - Setup validation
   - `.env.example` - Environment template

4. **Auto-created Directories:**
   - `uploads/` - Temporary file storage
   - `outputs/` - Generated results

---

## 🚀 How to Use

### Step 1: Start the API Server

```bash
cd c:\Users\rohit\Downloads\home-deck-ai-main\home-deck-ai-main
python api_server.py
```

You should see:
```
============================================================
🏠 Home Deck AI - Flask API Server
============================================================
✓ Turbo Mode: ENABLED (Fast generation)
✓ Device: cuda
✓ CORS Origins: http://localhost:3000
============================================================
Starting server on http://127.0.0.1:5000
============================================================
```

---

### Step 2: Test the API

**Health Check:**
```bash
curl http://localhost:5000/api/health
```

**Generate Design:**
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "image=@your_room_image.jpg"
```

---

### Step 3: Integrate with Your React ERP

**Basic React Example:**

```jsx
import React, { useState } from 'react';

const InteriorDesignUploader = () => {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    const formData = new FormData();
    formData.append('image', image);
    
    setLoading(true);
    const response = await fetch('http://localhost:5000/api/generate', {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    if (data.success) {
      setResult(`http://localhost:5000${data.result_url}`);
    }
    setLoading(false);
  };

  return (
    <div>
      <input 
        type="file" 
        onChange={(e) => setImage(e.target.files[0])} 
        accept="image/*"
      />
      <button onClick={handleGenerate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Design'}
      </button>
      {result && <img src={result} alt="Generated Design" />}
    </div>
  );
};
```

---

## 🔧 Configuration

### For Your React ERP

Update the CORS origins:

1. Create `.env` file (copy from `.env.example`)
2. Set your React URL:
   ```
   CORS_ORIGINS=http://localhost:3000,https://your-erp-url.com
   ```
3. Restart Flask server

---

## 📋 API Endpoint Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Check API status |
| `/api/generate` | POST | Generate interior design |
| `/api/images/<filename>` | GET | Retrieve generated images |

### POST /api/generate Parameters

- **image** (required): Image file (PNG/JPG/JPEG, max 16MB)
- **prompt** (optional): Design prompt
  - Default: "Modern minimal interior design, high quality, 8k, photorealistic..."
- **negative_prompt** (optional): What to avoid
  - Default: "low quality, blurry, distorted..."

### Response Example

```json
{
  "success": true,
  "result_url": "/api/images/design_a1b2c3d4.png",
  "structure_map_url": "/api/images/structure_a1b2c3d4.png",
  "depth_map_url": "/api/images/depth_a1b2c3d4.png",
  "processing_time": 4.5,
  "turbo_mode": true
}
```

---

## 📚 Complete Documentation

- **Quick Start**: See `QUICKSTART.md`
- **API Reference**: See `API_DOCUMENTATION.md`
- **React Integration**: See `REACT_INTEGRATION_GUIDE.md`

---

## ⚡ Performance

- **Turbo Mode**: ENABLED by default
- **First Request**: ~20-30 seconds (model loading)
- **Subsequent Requests**: ~5 seconds on GPU
- **CPU Mode**: ~60-120 seconds

---

## 🔒 Security (Optional)

To enable API key authentication:

1. Add to `.env`:
   ```
   API_KEY=your-secret-key-here
   ```

2. Include in React requests:
   ```javascript
   headers: {
     'X-API-Key': 'your-secret-key-here'
   }
   ```

---

## 🆘 Troubleshooting

### Server won't start
- Check Python version (3.10+)
- Install dependencies: `pip install -r requirements.txt`
- Check if port 5000 is available

### CORS errors in React
- Update `CORS_ORIGINS` in `.env`
- Restart Flask server
- Clear browser cache

### Out of memory
- Use CPU mode: Set `DEVICE=cpu` in `.env`
- Reduce image size before upload
- Close other GPU applications

### Slow generation
- First request loads model (~30s)
- Subsequent requests are fast (~5s)
- Turbo mode is enabled by default

---

## 🎯 Next Steps

1. ✅ **API is ready** - Server tested and validated
2. 🔌 **Integrate with React** - Use examples in `REACT_INTEGRATION_GUIDE.md`
3. 🎨 **Customize prompts** - Adjust default prompts in `api/routes.py`
4. 🚀 **Deploy to production** - See deployment section in `QUICKSTART.md`
5. 🔐 **Add authentication** - Enable API key if needed

---

## 📞 Support

For detailed information:
- API issues → `API_DOCUMENTATION.md`
- React integration → `REACT_INTEGRATION_GUIDE.md`
- General setup → `QUICKSTART.md`

---

**Congratulations! Your AI Interior Design API is ready for ERP integration! 🎉**
