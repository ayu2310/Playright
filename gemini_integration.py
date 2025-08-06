import google.generativeai as genai
import json
import logging
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiWorkflowGenerator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Define the workflow generation prompt
        self.workflow_prompt = """
You are a browser automation expert. Given a user's request, generate a detailed workflow that can be executed by a browser automation system.

The workflow should be returned as a JSON object with the following structure:
{
    "name": "Workflow Name",
    "description": "Brief description of what this workflow does",
    "steps": [
        {
            "action": "navigate",
            "url": "https://example.com",
            "description": "Navigate to the website"
        },
        {
            "action": "click",
            "selector": "button.login",
            "selector_type": "css",
            "description": "Click the login button"
        },
        {
            "action": "type",
            "selector": "input#username",
            "selector_type": "css",
            "text": "username",
            "description": "Enter username"
        },
        {
            "action": "wait",
            "selector": "div.loading",
            "selector_type": "css",
            "timeout": 10,
            "description": "Wait for loading to complete"
        },
        {
            "action": "screenshot",
            "path": "result.png",
            "description": "Take a screenshot of the result"
        }
    ]
}

Available actions:
- navigate: Navigate to a URL
- click: Click an element
- type: Type text into an input field
- wait: Wait for an element to appear
- get_text: Extract text from an element
- screenshot: Take a screenshot

Selector types:
- css: CSS selector
- xpath: XPath selector
- id: Element ID

Generate a workflow for the following request: {user_request}

Return only the JSON object, no additional text.
"""
    
    def generate_workflow(self, user_request: str) -> Dict[str, Any]:
        """Generate a workflow from a natural language request"""
        try:
            prompt = self.workflow_prompt.format(user_request=user_request)
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            content = response.text.strip()
            
            # Try to find JSON in the response
            if content.startswith('{') and content.endswith('}'):
                workflow = json.loads(content)
            else:
                # Try to extract JSON from markdown code blocks
                import re
                json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    workflow = json.loads(json_match.group(1))
                else:
                    # Try to find JSON object in the text
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        workflow = json.loads(json_match.group(0))
                    else:
                        raise ValueError("Could not extract JSON from response")
            
            logger.info(f"Generated workflow: {workflow.get('name', 'Unknown')}")
            return workflow
            
        except Exception as e:
            logger.error(f"Failed to generate workflow: {e}")
            raise
    
    def validate_workflow(self, workflow: Dict[str, Any]) -> bool:
        """Validate a workflow structure"""
        try:
            required_fields = ["name", "description", "steps"]
            for field in required_fields:
                if field not in workflow:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            if not isinstance(workflow["steps"], list):
                logger.error("Steps must be a list")
                return False
            
            valid_actions = ["navigate", "click", "type", "wait", "get_text", "screenshot"]
            
            for i, step in enumerate(workflow["steps"]):
                if "action" not in step:
                    logger.error(f"Step {i} missing action")
                    return False
                
                if step["action"] not in valid_actions:
                    logger.error(f"Step {i} has invalid action: {step['action']}")
                    return False
                
                # Validate action-specific requirements
                if step["action"] == "navigate":
                    if "url" not in step:
                        logger.error(f"Step {i} (navigate) missing url")
                        return False
                
                elif step["action"] in ["click", "type", "wait", "get_text"]:
                    if "selector" not in step:
                        logger.error(f"Step {i} ({step['action']}) missing selector")
                        return False
                
                elif step["action"] == "type":
                    if "text" not in step:
                        logger.error(f"Step {i} (type) missing text")
                        return False
            
            logger.info("Workflow validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Workflow validation failed: {e}")
            return False
    
    def get_workflow_summary(self, workflow: Dict[str, Any]) -> str:
        """Get a human-readable summary of the workflow"""
        try:
            summary = f"Workflow: {workflow['name']}\n"
            summary += f"Description: {workflow['description']}\n"
            summary += f"Steps: {len(workflow['steps'])}\n\n"
            
            for i, step in enumerate(workflow['steps'], 1):
                summary += f"{i}. {step['action'].upper()}: {step.get('description', 'No description')}\n"
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate workflow summary: {e}")
            return "Unable to generate summary"