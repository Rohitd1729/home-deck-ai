"""
API Routes for Interior Design Generation
"""
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge
import os
import time
from config import Config
from api.model_manager import ModelManager
from api.utils import allowed_file, save_uploaded_file, save_result_image, cleanup_file

# Create Blueprint
api = Blueprint('api', __name__, url_prefix='/api')

# Initialize model manager
model_manager = ModelManager()

@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    status = model_manager.get_status()
    return jsonify({
        'status': 'healthy',
        'model_loaded': status['model_loaded'],
        'turbo_mode': status['turbo_mode'],
        'device': status['device']
    }), 200

@api.route('/generate', methods=['POST'])
def generate_design():
    """
    Generate interior design from uploaded image
    POST /api/generate
    
    Form data:
        - image: Image file (required)
        - prompt: Design prompt (optional, default provided)
        - negative_prompt: Negative prompt (optional, default provided)
    
    Returns:
        JSON with generated image URL or base64
    """
    try:
        # Validate image file
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Invalid file format. Allowed: {", ".join(Config.ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Get optional parameters
        prompt = request.form.get('prompt', 
            'Modern minimal interior design, high quality, 8k, photorealistic, neutral colors, cozy lighting')
        negative_prompt = request.form.get('negative_prompt', 
            'low quality, blurry, distorted, messy, clutter')
        
        # Save uploaded file
        input_path = save_uploaded_file(file)
        if not input_path:
            return jsonify({
                'success': False,
                'error': 'Failed to save uploaded file'
            }), 500
        
        # Get model (lazy loading)
        model = model_manager.get_model(device=Config.DEVICE)
        
        # Generate design
        start_time = time.time()
        result_image, structure_map, depth_map = model.generate_design(
            input_path,
            prompt=prompt,
            negative_prompt=negative_prompt
        )
        processing_time = time.time() - start_time
        
        # Save result images
        result_filename = save_result_image(result_image, prefix="design")
        structure_filename = save_result_image(structure_map, prefix="structure")
        depth_filename = save_result_image(depth_map, prefix="depth")
        
        # Cleanup uploaded file
        cleanup_file(input_path)
        
        # Return response
        response = {
            'success': True,
            'result_url': f'/api/images/{result_filename}',
            'structure_map_url': f'/api/images/{structure_filename}',
            'depth_map_url': f'/api/images/{depth_filename}',
            'processing_time': round(processing_time, 2),
            'turbo_mode': True
        }
        
        return jsonify(response), 200
        
    except RequestEntityTooLarge:
        return jsonify({
            'success': False,
            'error': f'File too large. Maximum size: {Config.MAX_CONTENT_LENGTH // (1024*1024)}MB'
        }), 413
    
    except Exception as e:
        # Cleanup on error
        if 'input_path' in locals():
            cleanup_file(input_path)
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    """Serve generated images"""
    try:
        return send_from_directory(Config.OUTPUT_FOLDER, filename)
    except FileNotFoundError:
        return jsonify({
            'success': False,
            'error': 'Image not found'
        }), 404
