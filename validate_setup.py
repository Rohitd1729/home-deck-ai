"""
Simple validation script to check Flask API setup
"""
import os
import sys

def check_files():
    """Check if all required files exist"""
    required_files = [
        'api_server.py',
        'config.py',
        'interior_designer.py',
        'requirements.txt',
        'api/__init__.py',
        'api/routes.py',
        'api/model_manager.py',
        'api/utils.py',
    ]
    
    print("Checking required files...")
    all_exist = True
    for file in required_files:
        exists = os.path.exists(file)
        status = "✅" if exists else "❌"
        print(f"  {status} {file}")
        if not exists:
            all_exist = False
    
    return all_exist

def check_imports():
    """Check if all imports work"""
    print("\nChecking imports...")
    try:
        import flask
        print("  ✅ flask")
    except ImportError:
        print("  ❌ flask - Run: pip install flask")
        return False
    
    try:
        import flask_cors
        print("  ✅ flask_cors")
    except ImportError:
        print("  ❌ flask_cors - Run: pip install flask-cors")
        return False
    
    try:
        from config import Config
        print("  ✅ config")
    except Exception as e:
        print(f"  ❌ config - Error: {e}")
        return False
    
    return True

def check_structure():
    """Check directory structure"""
    print("\nChecking directory structure...")
    Config.init_app()
    
    if os.path.exists('uploads'):
        print("  ✅ uploads/ directory")
    else:
        print("  ❌ uploads/ directory missing")
        
    if os.path.exists('outputs'):
        print("  ✅ outputs/ directory")
    else:
        print("  ❌ outputs/ directory missing")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 Flask API Setup Validator")
    print("=" * 60)
    
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(__file__))
    
    from config import Config
    
    files_ok = check_files()
    imports_ok = check_imports()
    structure_ok = check_structure()
    
    print("\n" + "=" * 60)
    if files_ok and imports_ok and structure_ok:
        print("✅ All checks passed! Ready to run API server.")
        print("\nTo start the server:")
        print("  python api_server.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
    print("=" * 60)
