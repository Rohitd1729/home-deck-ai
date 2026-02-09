"""
Singleton Model Manager for Interior Designer
Handles lazy loading and caching of the AI model
"""
import threading
from interior_designer import InteriorDesigner

class ModelManager:
    """Thread-safe singleton for managing the InteriorDesigner model"""
    
    _instance = None
    _lock = threading.Lock()
    _model = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_model(self, device="cuda"):
        """Get or initialize the model (lazy loading)"""
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    print(f"Initializing Interior Designer model on {device}...")
                    self._model = InteriorDesigner(device=device)
                    # Enable turbo mode by default
                    self._model.enable_turbo(True)
                    self._initialized = True
                    print("Model initialized successfully with Turbo Mode enabled!")
        return self._model
    
    def is_ready(self):
        """Check if model is loaded"""
        return self._initialized
    
    def get_status(self):
        """Get model status information"""
        return {
            "model_loaded": self._initialized,
            "turbo_mode": self._model.is_turbo if self._model else False,
            "device": self._model.device if self._model else "not loaded"
        }
