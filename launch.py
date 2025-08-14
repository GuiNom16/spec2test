#!/usr/bin/env python3
"""
Launch script for Spec2Test Lite
Checks dependencies and starts the Streamlit app
"""

import sys
import subprocess
import importlib.util

def check_dependency(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False

def install_dependency(package_name):
    """Install a missing dependency"""
    print(f"Installing {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def check_ollama():
    """Check if Ollama is installed and running"""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def main():
    print("🚀 Spec2Test Lite - Launch Check")
    print("=" * 40)
    
    # Check Python dependencies
    dependencies = [
        ("streamlit", "streamlit"),
        ("pandas", "pandas"),
        ("PyMuPDF", "fitz"),
        ("python-docx", "docx")
    ]
    
    missing_deps = []
    for package, import_name in dependencies:
        if not check_dependency(package, import_name):
            missing_deps.append(package)
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Installing missing dependencies...")
        
        for dep in missing_deps:
            if not install_dependency(dep):
                print(f"❌ Failed to install {dep}")
                print("Please install manually: pip install -r requirements.txt")
                return False
        
        print("✅ Dependencies installed successfully!")
    else:
        print("✅ All Python dependencies are installed")
    
    # Check Ollama
    if not check_ollama():
        print("❌ Ollama not found or not running")
        print("Please install Ollama from https://ollama.ai")
        print("Then run: ollama pull llama3")
        return False
    else:
        print("✅ Ollama is running")
    
    print("\n🎉 All checks passed! Starting Spec2Test Lite...")
    print("=" * 40)
    
    # Launch the app
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Spec2Test Lite stopped by user")
    except Exception as e:
        print(f"❌ Error starting app: {e}")

if __name__ == "__main__":
    main() 