"""
Test script for the Interior Design API
Usage: python test_api.py
"""
import requests
import os

API_URL = "http://localhost:5000/api"

def test_health():
    """Test health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def test_generate(image_path):
    """Test generate endpoint with a sample image"""
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found!")
        print("Please provide a valid image path")
        return False
    
    print(f"Testing generate endpoint with {image_path}...")
    print("This may take 20-30 seconds on first request (model loading)...")
    
    with open(image_path, 'rb') as f:
        files = {'image': f}
        data = {
            'prompt': 'Modern minimal living room, 8k, photorealistic',
            'negative_prompt': 'low quality, blurry'
        }
        
        response = requests.post(
            f"{API_URL}/generate",
            files=files,
            data=data,
            timeout=120  # 2 minute timeout
        )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {result}\n")
    
    if result.get('success'):
        print(f"✅ Success! Generated in {result['processing_time']}s")
        print(f"View result at: http://localhost:5000{result['result_url']}")
        return True
    else:
        print(f"❌ Failed: {result.get('error')}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🏠 Home Deck AI - API Test Script")
    print("=" * 60)
    
    # Test health
    if not test_health():
        print("❌ Health check failed. Is the server running?")
        print("Start server with: python api_server.py")
        exit(1)
    
    # Test generate
    print("To test image generation, provide an image path:")
    image_path = input("Enter path to test image (or press Enter to skip): ").strip()
    
    if image_path:
        test_generate(image_path)
    else:
        print("Skipping generation test")
        print("\nTo test later, use:")
        print('  python -c "from test_api import test_generate; test_generate(\'path/to/image.jpg\')"')
    
    print("\n" + "=" * 60)
    print("✅ API test completed!")
    print("=" * 60)
