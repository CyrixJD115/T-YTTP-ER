#!/usr/bin/env python3
"""
T(YTTP)ER Application Launcher
==============================

This script sets up and launches the T(YTTP)ER application with:
- Python version validation
- Virtual environment creation
- Dependency installation
- Application execution

Features:
- Clear progress reporting
- Error handling with descriptive messages
- Cross-platform support (Windows, macOS, Linux)
- Dependency version pinning
- Virtual environment management
"""

import sys
import os
import platform
import subprocess
import shutil
from pathlib import Path
import time

# Application information
APP_NAME = "T(YTTP)ER"
APP_VERSION = "1.0.0"
REPO_URL = "https://github.com/yourusername/tyttper"

# Required packages with version specifications
REQUIREMENTS = [
    "PySide6>=6.7.0",
    "youtube-transcript-api>=0.6.2",
    "python-docx>=1.1.0",
    "requests>=2.31.0",
]

def print_header():
    """Display application header with version information."""
    print(f"\n{'-'*60}")
    print(f"{APP_NAME} v{APP_VERSION} - Enhanced YouTube Transcript Processor")
    print(f"{'-'*60}\n")

def validate_python():
    """Ensure Python 3.7+ is used with descriptive error messages."""
    print("[1/4] Checking Python version...")
    if sys.version_info < (3, 7):
        print("\n[ERROR] Python 3.7+ is required.")
        print(f"Current version: {platform.python_version()}")
        print("Please upgrade Python from https://python.org/downloads")
        sys.exit(1)
    print(f"✓ Python {platform.python_version()} detected\n")

def create_venv():
    """Create a virtual environment with progress indicators."""
    print("[2/4] Setting up virtual environment...")
    venv_dir = Path("venv")
    
    if venv_dir.exists():
        print("✓ Virtual environment already exists")
        return False  # No need to install dependencies again
    
    try:
        print("- Creating isolated Python environment...")
        result = subprocess.run(
            [sys.executable, "-m", "venv", "venv"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            print(f"\n[ERROR] Failed to create virtual environment:")
            print(result.stderr)
            sys.exit(1)
            
        print("✓ Virtual environment created successfully\n")
        return True  # New environment, need to install dependencies
        
    except Exception as e:
        print(f"\n[ERROR] Virtual environment setup failed: {e}")
        sys.exit(1)

def install_dependencies(is_new_venv):
    """Install required packages with progress visualization."""
    if not is_new_venv:
        print("[3/4] Skipping dependency installation (existing environment)")
        return
    
    print("[3/4] Installing dependencies...")
    
    is_windows = platform.system() == "Windows"
    venv_bin = "Scripts" if is_windows else "bin"
    pip_exe = "pip.exe" if is_windows else "pip"
    pip_path = Path("venv") / venv_bin / pip_exe
    
    if not pip_path.exists():
        print(f"\n[ERROR] Pip not found at: {pip_path}")
        sys.exit(1)
    
    try:
        print("- Installing required packages...")
        cmd = [str(pip_path), "install"] + REQUIREMENTS
        
        # Execute installation
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            print(f"\n[ERROR] Dependency installation failed:")
            print(result.stderr)
            sys.exit(1)
        
        print("✓ Dependencies installed successfully\n")
        
    except Exception as e:
        print(f"\n[ERROR] Installation process failed: {e}")
        sys.exit(1)

def launch_app():
    """Launch the main application with proper environment."""
    print("[4/4] Launching application...")
    is_windows = platform.system() == "Windows"
    venv_bin = "Scripts" if is_windows else "bin"
    python_exe = "python.exe" if is_windows else "python"
    python_path = Path("venv") / venv_bin / python_exe
    
    if not python_path.exists():
        print(f"\n[ERROR] Python interpreter not found at: {python_path}")
        print("Possible solutions:")
        print("1. Delete the 'venv' directory and rerun this script")
        print("2. Ensure virtual environment was created properly")
        print("3. Check Python installation")
        sys.exit(1)
    
    try:
        print("\nStarting T(YTTP)ER GUI...")
        print("=" * 60)
        subprocess.run([str(python_path), "main.py"], check=True)
    except KeyboardInterrupt:
        print("\nApplication closed by user")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Application crashed with code {e.returncode}")
    except Exception as e:
        print(f"\n[ERROR] Failed to launch application: {e}")
    finally:
        print("\n" + "=" * 60)
        print("Thank you for using T(YTTP)ER!")
        print(f"Report issues at: {REPO_URL}\n")

def main():
    """Main application workflow."""
    print_header()
    validate_python()
    is_new_venv = create_venv()
    install_dependencies(is_new_venv)
    launch_app()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user. Exiting...")
        sys.exit(1)