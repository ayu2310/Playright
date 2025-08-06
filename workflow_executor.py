import asyncio
import logging
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from automation_engine import BrowserAutomationEngine
from gemini_integration import GeminiWorkflowGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowExecutor:
    def __init__(self, browser_type: str = "playwright", headless: bool = False):
        self.browser_type = browser_type
        self.headless = headless
        self.engine = None
        self.gemini = GeminiWorkflowGenerator()
        
    async def execute_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow and return results"""
        results = {
            "workflow_name": workflow.get("name", "Unknown"),
            "start_time": datetime.now().isoformat(),
            "steps_executed": 0,
            "total_steps": len(workflow.get("steps", [])),
            "success": True,
            "errors": [],
            "screenshots": [],
            "extracted_data": {}
        }
        
        try:
            # Initialize browser
            self.engine = BrowserAutomationEngine(
                browser_type=self.browser_type,
                headless=self.headless
            )
            await self.engine.start_browser()
            
            # Execute each step
            for i, step in enumerate(workflow.get("steps", []), 1):
                try:
                    logger.info(f"Executing step {i}: {step.get('action', 'unknown')}")
                    await self._execute_step(step, results)
                    results["steps_executed"] += 1
                    
                except Exception as e:
                    error_msg = f"Step {i} failed: {str(e)}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
                    results["success"] = False
                    break
            
        except Exception as e:
            error_msg = f"Workflow execution failed: {str(e)}"
            logger.error(error_msg)
            results["errors"].append(error_msg)
            results["success"] = False
            
        finally:
            # Clean up
            if self.engine:
                await self.engine.close_browser()
            
            results["end_time"] = datetime.now().isoformat()
            return results
    
    async def _execute_step(self, step: Dict[str, Any], results: Dict[str, Any]):
        """Execute a single workflow step"""
        action = step.get("action")
        
        if action == "navigate":
            url = step.get("url")
            if not url:
                raise ValueError("Navigate action requires 'url' parameter")
            await self.engine.navigate_to(url)
            
        elif action == "click":
            selector = step.get("selector")
            selector_type = step.get("selector_type", "css")
            if not selector:
                raise ValueError("Click action requires 'selector' parameter")
            await self.engine.click_element(selector, selector_type)
            
        elif action == "type":
            selector = step.get("selector")
            text = step.get("text")
            selector_type = step.get("selector_type", "css")
            if not selector or not text:
                raise ValueError("Type action requires 'selector' and 'text' parameters")
            await self.engine.type_text(selector, text, selector_type)
            
        elif action == "wait":
            selector = step.get("selector")
            timeout = step.get("timeout", 10)
            selector_type = step.get("selector_type", "css")
            if not selector:
                raise ValueError("Wait action requires 'selector' parameter")
            await self.engine.wait_for_element(selector, timeout, selector_type)
            
        elif action == "get_text":
            selector = step.get("selector")
            selector_type = step.get("selector_type", "css")
            key = step.get("key", f"text_{len(results['extracted_data'])}")
            if not selector:
                raise ValueError("Get_text action requires 'selector' parameter")
            text = await self.engine.get_text(selector, selector_type)
            results["extracted_data"][key] = text
            
        elif action == "screenshot":
            path = step.get("path", f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            await self.engine.take_screenshot(path)
            results["screenshots"].append(path)
            
        else:
            raise ValueError(f"Unknown action: {action}")
    
    async def generate_and_execute(self, user_request: str) -> Dict[str, Any]:
        """Generate a workflow from user request and execute it"""
        try:
            # Generate workflow
            logger.info("Generating workflow from user request...")
            workflow = self.gemini.generate_workflow(user_request)
            
            # Validate workflow
            if not self.gemini.validate_workflow(workflow):
                raise ValueError("Generated workflow is invalid")
            
            # Execute workflow
            logger.info("Executing generated workflow...")
            results = await self.execute_workflow(workflow)
            
            # Add workflow info to results
            results["workflow"] = workflow
            results["workflow_summary"] = self.gemini.get_workflow_summary(workflow)
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to generate and execute workflow: {e}")
            raise
    
    def save_results(self, results: Dict[str, Any], filename: str = None) -> str:
        """Save execution results to a JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"workflow_results_{timestamp}.json"
        
        try:
            # Create results directory if it doesn't exist
            os.makedirs("results", exist_ok=True)
            filepath = os.path.join("results", filename)
            
            with open(filepath, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"Results saved to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
            raise
    
    def load_workflow(self, filepath: str) -> Dict[str, Any]:
        """Load a workflow from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                workflow = json.load(f)
            
            if not self.gemini.validate_workflow(workflow):
                raise ValueError("Loaded workflow is invalid")
            
            logger.info(f"Loaded workflow: {workflow.get('name', 'Unknown')}")
            return workflow
            
        except Exception as e:
            logger.error(f"Failed to load workflow: {e}")
            raise