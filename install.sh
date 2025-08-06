#!/bin/bash

echo "🚀 Browser Workflow Automation Agent - Installation Script"
echo "=========================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $python_version detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install

# Create environment file
echo "⚙️  Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Environment file created (.env)"
    echo "📝 Please edit .env and add your Gemini API key"
else
    echo "⚠️  .env file already exists"
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p workflows results schedules

# Make CLI executable
echo "🔧 Making CLI executable..."
chmod +x cli.py

# Test installation
echo "🧪 Testing installation..."
python test_system.py

echo ""
echo "🎉 Installation completed successfully!"
echo "=========================================================="
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file and add your Gemini API key"
echo "2. Get a Gemini API key from: https://makersuite.google.com/app/apikey"
echo ""
echo "🚀 Quick start:"
echo "   source venv/bin/activate"
echo "   python cli.py execute \"Go to google.com and search for 'python automation'\""
echo ""
echo "🌐 Start web interface:"
echo "   source venv/bin/activate"
echo "   python web_interface.py"
echo ""
echo "📖 For more examples, see README.md"
echo "=========================================================="