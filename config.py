import os
from pathlib import Path

class Config:
    """Flask application configuration"""
    
    # Base directory
    BASE_DIR = Path(__file__).parent.absolute()
    
    # File upload settings
    UPLOAD_FOLDER = BASE_DIR / "uploads"
    OUTPUT_FOLDER = BASE_DIR / "outputs"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    # CORS settings - Update this with your React ERP URL
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # API settings
    API_KEY = os.getenv('API_KEY', None)  # Optional: Set API key for authentication
    
    # Cleanup settings
    CLEANUP_INTERVAL = 3600  # Clean old files every hour (in seconds)
    FILE_RETENTION_TIME = 7200  # Keep files for 2 hours (in seconds)
    
    # Model settings
    DEVICE = os.getenv('DEVICE', 'cuda')  # 'cuda' or 'cpu'
    BASE_MODEL = os.getenv('BASE_MODEL', 'SG161222/Realistic_Vision_V6.0_B1_noVAE')
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    @staticmethod
    def init_app():
        """Initialize application directories"""
        Config.UPLOAD_FOLDER.mkdir(exist_ok=True)
        Config.OUTPUT_FOLDER.mkdir(exist_ok=True)
