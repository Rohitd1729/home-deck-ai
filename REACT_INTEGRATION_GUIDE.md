# React Integration Guide - Home Deck AI

## Quick Start for React/ERP Integration

This guide shows how to integrate the Home Deck AI API into your React-based ERP system.

---

## Setup

### 1. Configure CORS

Update `.env` in the Flask project with your React app URL:

```env
CORS_ORIGINS=http://localhost:3000,http://your-erp-url.com
```

Restart the Flask server after changes.

### 2. Install Dependencies in React

```bash
npm install axios
# or
yarn add axios
```

---

## Basic React Component

### Simple Upload Component

```jsx
import React, { useState } from 'react';
import axios from 'axios';

const InteriorDesignGenerator = () => {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_URL = 'http://localhost:5000/api';

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const handleGenerate = async () => {
    if (!image) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', image);
    formData.append('prompt', 'Modern minimal interior design, high quality, 8k, photorealistic');
    formData.append('negative_prompt', 'low quality, blurry, distorted');

    try {
      const response = await axios.post(`${API_URL}/generate`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        setResult({
          image: `${API_URL}${response.data.result_url}`,
          processingTime: response.data.processing_time,
        });
      } else {
        setError(response.data.error);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate design');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="interior-design-generator">
      <h2>AI Interior Design Generator</h2>
      
      <div className="upload-section">
        <input
          type="file"
          accept="image/png,image/jpeg,image/jpg"
          onChange={handleImageChange}
          disabled={loading}
        />
      </div>

      {preview && (
        <div className="preview">
          <h3>Original Image</h3>
          <img src={preview} alt="Preview" style={{ maxWidth: '400px' }} />
        </div>
      )}

      <button onClick={handleGenerate} disabled={loading || !image}>
        {loading ? 'Generating...' : 'Generate Design'}
      </button>

      {error && <div className="error">{error}</div>}

      {result && (
        <div className="result">
          <h3>Generated Design</h3>
          <img src={result.image} alt="Generated" style={{ maxWidth: '400px' }} />
          <p>Processing time: {result.processingTime}s</p>
        </div>
      )}
    </div>
  );
};

export default InteriorDesignGenerator;
```

---

## Advanced Integration with Custom Prompts

```jsx
import React, { useState } from 'react';
import axios from 'axios';

const AdvancedInteriorDesign = () => {
  const [formData, setFormData] = useState({
    image: null,
    prompt: 'Modern minimal interior design, high quality, 8k, photorealistic',
    negativePrompt: 'low quality, blurry, distorted, messy',
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const API_URL = 'http://localhost:5000/api';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const data = new FormData();
    data.append('image', formData.image);
    data.append('prompt', formData.prompt);
    data.append('negative_prompt', formData.negativePrompt);

    try {
      const response = await axios.post(`${API_URL}/generate`, data);
      setResult(response.data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        onChange={(e) => setFormData({ ...formData, image: e.target.files[0] })}
        required
      />
      
      <textarea
        placeholder="Design prompt..."
        value={formData.prompt}
        onChange={(e) => setFormData({ ...formData, prompt: e.target.value })}
      />

      <textarea
        placeholder="What to avoid..."
        value={formData.negativePrompt}
        onChange={(e) => setFormData({ ...formData, negativePrompt: e.target.value })}
      />

      <button type="submit" disabled={loading}>
        {loading ? 'Generating...' : 'Generate'}
      </button>

      {result?.success && (
        <div>
          <img src={`${API_URL}${result.result_url}`} alt="Result" />
        </div>
      )}
    </form>
  );
};
```

---

## TypeScript Type Definitions

```typescript
// types/interior-design.ts

export interface GenerateRequest {
  image: File;
  prompt?: string;
  negative_prompt?: string;
}

export interface GenerateResponse {
  success: boolean;
  result_url?: string;
  structure_map_url?: string;
  depth_map_url?: string;
  processing_time?: number;
  turbo_mode?: boolean;
  error?: string;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
  turbo_mode: boolean;
  device: string;
}
```

---

## API Service Module

```javascript
// services/interiorDesignApi.js

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

class InteriorDesignAPI {
  async checkHealth() {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  }

  async generateDesign(image, prompt, negativePrompt) {
    const formData = new FormData();
    formData.append('image', image);
    if (prompt) formData.append('prompt', prompt);
    if (negativePrompt) formData.append('negative_prompt', negativePrompt);

    const response = await axios.post(`${API_BASE_URL}/generate`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000, // 2 minutes timeout
    });

    return response.data;
  }

  getImageUrl(path) {
    return `${API_BASE_URL}${path}`;
  }
}

export default new InteriorDesignAPI();
```

**Usage:**

```jsx
import interiorDesignAPI from './services/interiorDesignApi';

// In your component
const handleGenerate = async () => {
  try {
    const result = await interiorDesignAPI.generateDesign(
      imageFile,
      'Modern living room',
      'low quality'
    );
    
    const imageUrl = interiorDesignAPI.getImageUrl(result.result_url);
    setGeneratedImage(imageUrl);
  } catch (error) {
    console.error(error);
  }
};
```

---

## Environment Variables

Add to your React `.env` file:

```env
REACT_APP_API_URL=http://localhost:5000/api
```

For production:
```env
REACT_APP_API_URL=https://your-api-domain.com/api
```

---

## Error Handling Best Practices

```jsx
const handleGenerate = async () => {
  try {
    setLoading(true);
    setError(null);
    
    const result = await interiorDesignAPI.generateDesign(image, prompt);
    
    if (!result.success) {
      throw new Error(result.error);
    }
    
    setResult(result);
  } catch (error) {
    if (error.response) {
      // Server responded with error
      setError(error.response.data.error || 'Server error');
    } else if (error.request) {
      // Request made but no response
      setError('No response from server. Is the API running?');
    } else {
      // Other errors
      setError(error.message);
    }
  } finally {
    setLoading(false);
  }
};
```

---

## Loading States

```jsx
{loading && (
  <div className="loading">
    <div className="spinner" />
    <p>Generating design... This may take a few seconds.</p>
  </div>
)}
```

---

## Integration with ERP Workflow

### Example: Property Management Module

```jsx
const PropertyDesignModule = ({ propertyId }) => {
  const [designs, setDesigns] = useState([]);

  const handleGenerateDesign = async (roomImage) => {
    const result = await interiorDesignAPI.generateDesign(roomImage);
    
    // Save to your ERP database
    await saveToDatabase({
      propertyId,
      designUrl: result.result_url,
      createdAt: new Date(),
    });
    
    setDesigns([...designs, result]);
  };

  return (
    <div>
      <h3>Property {propertyId} - Room Designs</h3>
      {/* Your ERP UI */}
    </div>
  );
};
```

---

## Testing the Integration

1. **Start Flask API:**
   ```bash
   cd home-deck-ai-main
   python api_server.py
   ```

2. **Start React App:**
   ```bash
   cd your-erp-system
   npm start
   ```

3. **Test Upload:**
   - Upload a room image
   - Click generate
   - Wait ~5 seconds (first time may take longer)
   - View result

---

## Troubleshooting

### CORS Issues
- Check Flask `.env` has your React URL
- Restart Flask server
- Check browser console for specific CORS errors

### Timeout Errors
- Increase axios timeout to 120000ms (2 minutes)
- First request takes longer (model loading)

### File Upload Fails
- Check file size < 16MB
- Ensure format is PNG/JPG/JPEG
- Verify FormData is properly constructed
