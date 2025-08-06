# 🚀 Quick Start Reference

## 📋 Essential Commands

### Setup (One-time)
```bash
# Clone and install
git clone <repository-url>
cd browser-automation-agent
chmod +x install.sh
./install.sh

# Set up API key
nano .env  # Add your Gemini API key
```

### Daily Usage
```bash
# Always activate virtual environment first
source venv/bin/activate

# Execute a workflow
python cli.py execute "Go to google.com and search for 'python automation'"

# Start web interface
python web_interface.py
# Then visit: http://localhost:8000/docs
```

## 🔑 Environment Setup

### 1. Get Gemini API Key
- Visit: https://makersuite.google.com/app/apikey
- Create API key and copy it

### 2. Configure .env File
```bash
nano .env
```

Add your API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
HEADLESS_MODE=false
BROWSER_TYPE=chromium
```

### 3. Verify Setup
```bash
source venv/bin/activate
python test_system.py
```

## 🎯 Common Commands

### Execute Workflows
```bash
# Basic execution
python cli.py execute "Go to example.com and click login"

# With options
python cli.py execute "Search google for python" --headless --save-results

# From saved file
python cli.py execute-file --filepath "workflows/my_workflow.json"
```

### Generate Workflows
```bash
# Generate without executing
python cli.py generate "Login to website with credentials"

# Generate and save
python cli.py generate "Complex workflow" --save-workflow
```

### Schedule Workflows
```bash
# Schedule daily at 9 AM
python cli.py schedule "Check website" --time "09:00" --repeat

# Schedule every 30 minutes
python cli.py interval "Monitor site" --interval 30

# List scheduled jobs
python cli.py list-jobs

# Remove a job
python cli.py remove-job "job_name"
```

### Web API
```bash
# Start server
python web_interface.py

# Test API
curl -X POST "http://localhost:8000/execute" \
     -H "Content-Type: application/json" \
     -d '{"user_request": "Go to google.com"}'
```

## 🔧 Troubleshooting

### Common Issues
```bash
# Check API key
echo $GEMINI_API_KEY

# Reinstall browsers
playwright install

# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Test system
python test_system.py
```

### Debug Mode
```bash
# Enable debug logging
echo "LOG_LEVEL=DEBUG" >> .env
```

## 📁 File Locations

- **Workflows**: `workflows/` directory
- **Results**: `results/` directory
- **Schedules**: `schedules/` directory
- **Screenshots**: Current directory with timestamps

## 🌐 API Endpoints

- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health
- **Execute**: POST http://localhost:8000/execute
- **Generate**: POST http://localhost:8000/generate
- **Schedule**: POST http://localhost:8000/schedule
- **Jobs**: GET http://localhost:8000/jobs

## 📞 Need Help?

1. Check this quick reference
2. Read the full README.md
3. Run `python test_system.py`
4. Check the API docs at http://localhost:8000/docs