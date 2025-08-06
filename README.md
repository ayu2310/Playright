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

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd browser-automation-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key
   ```

5. **Get a Gemini API key**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

## 🚀 Quick Start

### Command Line Interface

1. **Execute a workflow immediately**
   ```bash
   python cli.py execute "Go to google.com and search for 'python automation'"
   ```

2. **Generate a workflow without executing**
   ```bash
   python cli.py generate "Login to a website" --save-workflow
   ```

3. **Schedule a workflow**
   ```bash
   python cli.py schedule "Check website status" --time "09:00" --repeat --start-scheduler
   ```

### Web API

1. **Start the web server**
   ```bash
   python web_interface.py
   ```

2. **Access the API documentation**
   - Open your browser to `http://localhost:8000/docs`
   - Interactive API documentation with Swagger UI

3. **Make API calls**
   ```bash
   # Execute a workflow
   curl -X POST "http://localhost:8000/execute" \
        -H "Content-Type: application/json" \
        -d '{"user_request": "Go to google.com and search for python"}'
   ```

## 📖 Usage Examples

### Basic Workflow Execution

```bash
# Simple navigation and interaction
python cli.py execute "Go to example.com and click the login button"

# Form filling
python cli.py execute "Go to a website, fill username 'test@example.com' and password 'password123', then click login"

# Data extraction
python cli.py execute "Go to a news website and extract the headlines from the main page"
```

### Advanced Scheduling

```bash
# Daily monitoring at 9 AM
python cli.py schedule "Check if my website is working" --time "09:00" --repeat --start-scheduler

# Every 30 minutes monitoring
python cli.py interval "Monitor website uptime" --interval 30 --start-scheduler

# One-time execution tomorrow at 2 PM
python cli.py schedule "Send a test email" --time "14:00"
```

### Workflow Management

```bash
# List all scheduled jobs
python cli.py list-jobs

# Remove a scheduled job
python cli.py remove-job "my_monitoring_job"

# Generate and save a workflow for later use
python cli.py generate "Complex multi-step workflow" --save-workflow
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Browser Configuration
HEADLESS_MODE=false
BROWSER_TYPE=chromium  # chromium, firefox, webkit

# Scheduler Configuration
DEFAULT_TIMEZONE=UTC

# Logging Configuration
LOG_LEVEL=INFO
```

### Browser Options

- **Playwright** (Recommended): Faster, more reliable, better error handling
- **Selenium**: Traditional approach, good for legacy systems

## 📁 Project Structure

```
browser-automation-agent/
├── automation_engine.py      # Core browser automation engine
├── gemini_integration.py     # Gemini AI integration
├── workflow_executor.py      # Workflow execution logic
├── workflow_scheduler.py     # Scheduling functionality
├── web_interface.py          # FastAPI web interface
├── cli.py                    # Command-line interface
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── README.md                # This file
├── workflows/               # Saved workflows
├── results/                 # Execution results
└── schedules/               # Saved schedules
```

## 🔌 API Endpoints

### Core Endpoints

- `POST /execute` - Execute a workflow from natural language
- `POST /generate` - Generate a workflow without executing
- `POST /execute_file` - Execute a saved workflow file

### Scheduling Endpoints

- `POST /schedule` - Schedule a workflow at a specific time
- `POST /schedule_interval` - Schedule a workflow at intervals
- `GET /jobs` - List all scheduled jobs
- `GET /jobs/{job_name}` - Get job status
- `DELETE /jobs/{job_name}` - Remove a scheduled job

### Management Endpoints

- `POST /schedule/save` - Save current schedule
- `POST /schedule/load` - Load a saved schedule
- `GET /health` - Health check

## 🤖 Workflow Actions

The system supports the following actions:

- **navigate**: Go to a URL
- **click**: Click an element
- **type**: Type text into an input field
- **wait**: Wait for an element to appear
- **get_text**: Extract text from an element
- **screenshot**: Take a screenshot

### Selector Types

- **css**: CSS selector (default)
- **xpath**: XPath selector
- **id**: Element ID

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

1. **Gemini API Key Error**
   ```bash
   # Make sure your API key is set in .env
   echo $GEMINI_API_KEY
   ```

2. **Browser Installation Issues**
   ```bash
   # Reinstall Playwright browsers
   playwright install
   
   # For Selenium, ensure Chrome is installed
   # The webdriver-manager will handle ChromeDriver
   ```

3. **Permission Issues**
   ```bash
   # Make sure the script is executable
   chmod +x cli.py
   ```

### Debug Mode

Enable debug logging by setting `LOG_LEVEL=DEBUG` in your `.env` file.

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

1. Check the troubleshooting section
2. Review the API documentation at `/docs`
3. Open an issue on GitHub

---

**Happy Automating! 🚀**