"""
Flask API Server for Interior Design Generation
"""
from flask import Flask
from flask_cors import CORS
from config import Config

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    Config.init_app()
    
    # Enable CORS for React integration
    CORS(app, resources={
        r"/api/*": {
            "origins": Config.CORS_ORIGINS,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Register blueprints
    from api.routes import api
    app.register_blueprint(api)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return {"success": False, "error": "Endpoint not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return {"success": False, "error": "Internal server error"}, 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("=" * 60)
    print("🏠 Home Deck AI - Flask API Server")
    print("=" * 60)
    print(f"✓ Turbo Mode: ENABLED (Fast generation)")
    print(f"✓ Device: {Config.DEVICE}")
    print(f"✓ CORS Origins: {', '.join(Config.CORS_ORIGINS)}")
    print("=" * 60)
    print("API Endpoints:")
    print("  • POST /api/generate - Generate interior design")
    print("  • GET  /api/health   - Health check")
    print("  • GET  /api/images/<filename> - Serve generated images")
    print("=" * 60)
    print(f"Starting server on http://127.0.0.1:5000")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    )
