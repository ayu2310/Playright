# 🚀 Browser Workflow Automation Agent

A powerful browser automation agent that uses **Playwright** and **Selenium** with **Gemini AI** integration for intelligent workflow generation and scheduling.

## ✨ Features

- 🤖 **AI-Powered Workflow Generation**: Use natural language to describe what you want to automate
- 🌐 **Multi-Browser Support**: Choose between Playwright and Selenium
- ⏰ **Smart Scheduling**: Schedule workflows to run at specific times or intervals
- 🎯 **Easy-to-Use**: Simple CLI and REST API interfaces
- 📊 **Comprehensive Logging**: Detailed execution results and error tracking
- 💾 **Persistent Storage**: Save and load workflows and schedules
- 📸 **Screenshot Capture**: Automatic screenshot capture during execution

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Chrome browser (for Selenium)
- Gemini API key

### Method 1: Quick Installation (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd browser-automation-agent

# Run the installation script
chmod +x install.sh
./install.sh
```

### Method 2: Manual Installation

```bash
# Clone the repository
git clone <repository-url>
cd browser-automation-agent

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Create environment file
cp .env.example .env

# Create necessary directories
mkdir -p workflows results schedules

# Make CLI executable
chmod +x cli.py

# Test installation
python test_system.py
```

## 🔑 Setting Up Environment Variables

### Step 1: Get a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### Step 2: Configure Environment Variables

```bash
# Edit the .env file
nano .env
# or
vim .env
# or
code .env
```

Update the `.env` file with your API key:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Browser Configuration
HEADLESS_MODE=false
BROWSER_TYPE=chromium  # chromium, firefox, webkit

# Scheduler Configuration
DEFAULT_TIMEZONE=UTC

# Logging Configuration
LOG_LEVEL=INFO
```

**Important**: Replace `your_actual_gemini_api_key_here` with your real Gemini API key.

### Step 3: Verify Configuration

```bash
# Test that the API key is loaded correctly
source venv/bin/activate
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key loaded:', 'GEMINI_API_KEY' in os.environ)"
```

## 🚀 Usage

### Activating the Virtual Environment

**Always activate the virtual environment before using the system:**

```bash
source venv/bin/activate
```

You'll see `(venv)` in your prompt when it's activated.

### Command Line Interface (CLI)

#### 1. Execute a Workflow Immediately

```bash
# Basic execution
python cli.py execute "Go to google.com and search for 'python automation'"

# With specific browser type
python cli.py execute "Go to google.com and search for 'python automation'" --browser-type playwright

# In headless mode
python cli.py execute "Go to google.com and search for 'python automation'" --headless

# Save results to file
python cli.py execute "Go to google.com and search for 'python automation'" --save-results
```

#### 2. Generate a Workflow Without Executing

```bash
# Generate workflow
python cli.py generate "Login to a website with username 'test@example.com' and password 'password123'"

# Generate and save workflow
python cli.py generate "Login to a website" --save-workflow
```

#### 3. Schedule a Workflow

```bash
# Schedule for specific time (one-time)
python cli.py schedule "Check website status" --time "14:30"

# Schedule daily at 9 AM
python cli.py schedule "Check website status" --time "09:00" --repeat

# Schedule with custom job name
python cli.py schedule "Check website status" --time "09:00" --repeat --job-name "daily_check"

# Start scheduler after scheduling
python cli.py schedule "Check website status" --time "09:00" --repeat --start-scheduler
```

#### 4. Schedule Interval Workflows

```bash
# Run every 30 minutes
python cli.py interval "Monitor website uptime" --interval 30

# Run every 2 hours (120 minutes)
python cli.py interval "Monitor website uptime" --interval 120 --job-name "hourly_check"

# Start scheduler after scheduling
python cli.py interval "Monitor website uptime" --interval 30 --start-scheduler
```

#### 5. Manage Scheduled Jobs

```bash
# List all scheduled jobs
python cli.py list-jobs

# Remove a specific job
python cli.py remove-job "daily_check"
```

### Web API Interface

#### 1. Start the Web Server

```bash
# Start the server
python web_interface.py

# The server will start on http://localhost:8000
```

#### 2. Access API Documentation

Open your browser and go to:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

#### 3. Make API Calls

```bash
# Execute a workflow
curl -X POST "http://localhost:8000/execute" \
     -H "Content-Type: application/json" \
     -d '{"user_request": "Go to google.com and search for python automation"}'

# Generate a workflow
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"user_request": "Login to a website"}'

# Schedule a workflow
curl -X POST "http://localhost:8000/schedule" \
     -H "Content-Type: application/json" \
     -d '{"user_request": "Check website status", "schedule_time": "09:00", "repeat": true}'

# List scheduled jobs
curl -X GET "http://localhost:8000/jobs"
```

### Using Saved Workflows

#### 1. Execute a Saved Workflow File

```bash
# Execute from saved workflow file
python cli.py execute-file --filepath "workflows/my_workflow.json"

# Via API
curl -X POST "http://localhost:8000/execute_file" \
     -H "Content-Type: application/json" \
     -d '{"filepath": "workflows/my_workflow.json"}'
```

#### 2. Load and Save Schedules

```bash
# Save current schedule
curl -X POST "http://localhost:8000/schedule/save"

# Load a saved schedule
curl -X POST "http://localhost:8000/schedule/load" \
     -H "Content-Type: application/json" \
     -d '{"filepath": "schedules/my_schedule.json"}'
```

## 📖 Usage Examples

### Basic Workflow Examples

```bash
# Simple navigation
python cli.py execute "Go to example.com and click the login button"

# Form filling
python cli.py execute "Go to a website, fill username 'test@example.com' and password 'password123', then click login"

# Data extraction
python cli.py execute "Go to a news website and extract the headlines from the main page"

# Screenshot capture
python cli.py execute "Go to google.com, search for 'python', and take a screenshot of the results"
```

### Advanced Scheduling Examples

```bash
# Daily monitoring at 9 AM
python cli.py schedule "Check if my website is working" --time "09:00" --repeat --start-scheduler

# Every 30 minutes monitoring
python cli.py interval "Monitor website uptime" --interval 30 --start-scheduler

# One-time execution tomorrow at 2 PM
python cli.py schedule "Send a test email" --time "14:00"

# Multiple scheduled tasks
python cli.py schedule "Backup database" --time "02:00" --repeat --job-name "daily_backup"
python cli.py schedule "Generate reports" --time "08:00" --repeat --job-name "morning_reports"
python cli.py interval "Check system health" --interval 60 --job-name "health_check"
```

### Workflow Management Examples

```bash
# Generate and save a complex workflow
python cli.py generate "Complex multi-step workflow with form filling and data extraction" --save-workflow

# List all scheduled jobs
python cli.py list-jobs

# Remove specific jobs
python cli.py remove-job "daily_backup"
python cli.py remove-job "health_check"

# Check job status via API
curl -X GET "http://localhost:8000/jobs/daily_backup"
```

## 🔧 Configuration

### Environment Variables

The `.env` file contains all configuration options:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Browser Configuration
HEADLESS_MODE=false          # true/false - Run browser in headless mode
BROWSER_TYPE=chromium        # chromium, firefox, webkit

# Scheduler Configuration
DEFAULT_TIMEZONE=UTC         # Timezone for scheduling

# Logging Configuration
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR
```

### Browser Options

- **Playwright** (Recommended): Faster, more reliable, better error handling
- **Selenium**: Traditional approach, good for legacy systems

### File Locations

- **Workflows**: `workflows/` directory
- **Results**: `results/` directory  
- **Schedules**: `schedules/` directory
- **Screenshots**: Saved with timestamps in the current directory

## 📊 Output and Results

### Execution Results

Each workflow execution generates detailed results including:

- Execution status and timing
- Number of steps completed
- Screenshots taken
- Extracted data
- Error messages (if any)

### File Storage

- **Workflows**: Saved as JSON files in `workflows/` directory
- **Results**: Saved as JSON files in `results/` directory
- **Schedules**: Saved as JSON files in `schedules/` directory
- **Screenshots**: Saved as PNG files with timestamps

## 🛡️ Error Handling

The system includes comprehensive error handling:

- **Step-level errors**: Individual step failures don't stop the entire workflow
- **Browser errors**: Automatic browser restart on critical errors
- **Network errors**: Retry mechanisms for network issues
- **Validation**: Workflow validation before execution

## 🔍 Troubleshooting

### Common Issues

#### 1. Gemini API Key Error

```bash
# Check if API key is set
echo $GEMINI_API_KEY

# Verify .env file exists and has correct content
cat .env

# Test API key loading
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.environ.get('GEMINI_API_KEY', 'NOT FOUND')[:10] + '...')"
```

#### 2. Browser Installation Issues

```bash
# Reinstall Playwright browsers
playwright install

# For Selenium, ensure Chrome is installed
# The webdriver-manager will handle ChromeDriver automatically
```

#### 3. Permission Issues

```bash
# Make sure the script is executable
chmod +x cli.py
chmod +x install.sh

# Check virtual environment activation
which python
# Should show: /path/to/your/project/venv/bin/python
```

#### 4. Virtual Environment Issues

```bash
# Deactivate current environment
deactivate

# Remove and recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Debug Mode

Enable debug logging by setting `LOG_LEVEL=DEBUG` in your `.env` file:

```bash
# Edit .env file
nano .env

# Change LOG_LEVEL to DEBUG
LOG_LEVEL=DEBUG
```

### Testing the System

```bash
# Run comprehensive system test
python test_system.py

# Test specific components
python -c "from automation_engine import BrowserAutomationEngine; print('Engine OK')"
python -c "from gemini_integration import GeminiWorkflowGenerator; print('Gemini OK')"
python -c "from workflow_executor import WorkflowExecutor; print('Executor OK')"
```

## 🚀 Advanced Usage

### Running the Scheduler as a Service

```bash
# Start scheduler in background
nohup python -c "
from workflow_scheduler import WorkflowScheduler
scheduler = WorkflowScheduler()
scheduler.start_scheduler()
import time
while True: time.sleep(1)
" > scheduler.log 2>&1 &

# Check scheduler status
ps aux | grep workflow_scheduler
tail -f scheduler.log
```

### Custom Workflow Development

```bash
# Create a custom workflow file
cat > workflows/custom_workflow.json << 'EOF'
{
  "name": "Custom Workflow",
  "description": "A custom workflow",
  "steps": [
    {
      "action": "navigate",
      "url": "https://example.com",
      "description": "Navigate to example.com"
    },
    {
      "action": "click",
      "selector": "button.login",
      "selector_type": "css",
      "description": "Click login button"
    }
  ]
}
EOF

# Execute custom workflow
python cli.py execute-file --filepath "workflows/custom_workflow.json"
```

### Monitoring and Logs

```bash
# View recent execution results
ls -la results/

# Check scheduler logs
tail -f scheduler.log

# Monitor system resources
htop
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Playwright**: Modern browser automation
- **Selenium**: Traditional browser automation
- **Gemini AI**: Intelligent workflow generation
- **FastAPI**: Modern web framework
- **Schedule**: Python job scheduling

## 📞 Support

For issues and questions:

1. Check the troubleshooting section above
2. Review the API documentation at `/docs`
3. Open an issue on GitHub

---

**Happy Automating! 🚀**