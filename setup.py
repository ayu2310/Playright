#!/usr/bin/env python3
"""
Setup script for Browser Workflow Automation Agent
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install Python dependencies"""
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    return True

def install_playwright():
    """Install Playwright browsers"""
    if not run_command("playwright install", "Installing Playwright browsers"):
        return False
    return True

def setup_environment():
    """Set up environment file"""
    print("🔧 Setting up environment...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_example.exists():
        print("❌ .env.example file not found")
        return False
    
    if env_file.exists():
        print("⚠️  .env file already exists. Skipping...")
        return True
    
    try:
        shutil.copy(env_example, env_file)
        print("✅ Environment file created (.env)")
        print("📝 Please edit .env and add your Gemini API key")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = ["workflows", "results", "schedules"]
    
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
            print(f"✅ Created directory: {directory}/")
        except Exception as e:
            print(f"❌ Failed to create directory {directory}: {e}")
            return False
    
    return True

def make_executable():
    """Make CLI script executable"""
    print("🔧 Making CLI script executable...")
    
    cli_file = Path("cli.py")
    if cli_file.exists():
        try:
            cli_file.chmod(0o755)
            print("✅ CLI script is now executable")
            return True
        except Exception as e:
            print(f"⚠️  Could not make CLI executable: {e}")
            return True  # Not critical
    else:
        print("❌ cli.py not found")
        return False

def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    # Test imports
    try:
        import playwright
        import selenium
        import google.generativeai
        import schedule
        import fastapi
        print("✅ All dependencies imported successfully")
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    
    # Test CLI help
    if not run_command("python cli.py --help", "Testing CLI"):
        return False
    
    return True

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("🎉 Installation completed successfully!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your Gemini API key")
    print("2. Get a Gemini API key from: https://makersuite.google.com/app/apikey")
    print("\n🚀 Quick start:")
    print("   python cli.py execute \"Go to google.com and search for 'python automation'\"")
    print("\n🌐 Start web interface:")
    print("   python web_interface.py")
    print("\n📖 For more examples, see README.md")
    print("="*60)

def main():
    """Main setup function"""
    print("🚀 Browser Workflow Automation Agent Setup")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Install Playwright
    if not install_playwright():
        print("❌ Failed to install Playwright")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("❌ Failed to setup environment")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)
    
    # Make CLI executable
    make_executable()
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed")
        sys.exit(1)
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()