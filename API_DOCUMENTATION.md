# API Documentation - Home Deck AI

## Overview

Flask REST API for generating interior designs using AI with Turbo Mode enabled by default for fast generation (~5 seconds on GPU).

**Base URL:** `http://localhost:5000/api`

---

## Endpoints

### 1. Health Check

Check if the API server and AI model are ready.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "turbo_mode": true,
  "device": "cuda"
}
```

**Example:**
```bash
curl http://localhost:5000/api/health
```

---

### 2. Generate Interior Design

Upload an image and generate a photorealistic interior design.

**Endpoint:** `POST /api/generate`

**Content-Type:** `multipart/form-data`

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image` | File | Yes | - | Image file (PNG, JPG, JPEG). Max 16MB |
| `prompt` | String | No | "Modern minimal interior design..." | Design style prompt |
| `negative_prompt` | String | No | "low quality, blurry..." | What to avoid |

**Response Success (200):**
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

**Response Error (400/500):**
```json
{
  "success": false,
  "error": "Error message"
}
```

**Example (cURL):**
```bash
curl -X POST http://localhost:5000/api/generate \
  -F "image=@room.jpg" \
  -F "prompt=Modern living room, minimalist design, 8k" \
  -F "negative_prompt=low quality, blurry"
```

**Example (JavaScript/Fetch):**
```javascript
const formData = new FormData();
formData.append('image', imageFile);
formData.append('prompt', 'Scandinavian living room, wooden furniture, natural light');

const response = await fetch('http://localhost:5000/api/generate', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result.result_url); // "/api/images/design_xyz.png"
```

---

### 3. Serve Generated Images

Retrieve generated images by filename.

**Endpoint:** `GET /api/images/<filename>`

**Response:** Image file (PNG)

**Example:**
```bash
curl http://localhost:5000/api/images/design_a1b2c3d4.png -o result.png
```

In browser: `http://localhost:5000/api/images/design_a1b2c3d4.png`

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (missing image, invalid format) |
| 404 | Not Found (endpoint or image not found) |
| 413 | File Too Large (max 16MB) |
| 500 | Internal Server Error |

---

## File Formats

**Allowed Image Formats:** PNG, JPG, JPEG  
**Max File Size:** 16MB  
**Recommended Resolution:** 512px - 1024px (larger images take longer)

---

## Rate Limiting

Currently no rate limiting. For production, consider implementing:
- Token bucket algorithm
- Per-IP rate limits
- API key-based quotas

---

## Authentication (Optional)

To enable API key authentication:

1. Set `API_KEY` in `.env`:
   ```
   API_KEY=your-secret-key-here
   ```

2. Include in request headers:
   ```
   X-API-Key: your-secret-key-here
   ```

---

## Performance

- **First Request:** ~20-30 seconds (model loading)
- **Subsequent Requests (Turbo):** ~5 seconds on GPU
- **CPU Mode:** ~60-120 seconds per request

---

## Troubleshooting

### "Model not loaded" error
- Wait for server to fully start (model loads on first request)
- Check GPU availability if using CUDA
- Try CPU mode: Set `DEVICE=cpu` in `.env`

### CORS errors
- Update `CORS_ORIGINS` in `.env` with your React app URL
- Restart Flask server after config changes

### Out of memory
- Reduce image resolution before uploading
- Use CPU mode instead of GPU
- Close other GPU-intensive applications
