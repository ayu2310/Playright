from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import asyncio
import logging
import json
import os
from datetime import datetime

from workflow_executor import WorkflowExecutor
from workflow_scheduler import WorkflowScheduler
from gemini_integration import GeminiWorkflowGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Browser Workflow Automation Agent",
    description="A browser automation agent with Gemini AI integration and scheduling",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
executor = WorkflowExecutor(browser_type="playwright", headless=True)
scheduler = WorkflowScheduler(browser_type="playwright", headless=True)
gemini = GeminiWorkflowGenerator()

# Start scheduler
scheduler.start_scheduler()

# Pydantic models
class WorkflowRequest(BaseModel):
    user_request: str
    browser_type: str = "playwright"
    headless: bool = True

class ScheduleRequest(BaseModel):
    user_request: str
    schedule_time: str  # HH:MM format
    job_name: Optional[str] = None
    repeat: bool = False
    browser_type: str = "playwright"
    headless: bool = True

class IntervalRequest(BaseModel):
    user_request: str
    interval_minutes: int
    job_name: Optional[str] = None
    browser_type: str = "playwright"
    headless: bool = True

class WorkflowFileRequest(BaseModel):
    filepath: str
    browser_type: str = "playwright"
    headless: bool = True

class ScheduleFileRequest(BaseModel):
    filepath: str

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with basic information"""
    return {
        "message": "Browser Workflow Automation Agent",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "execute": "/execute",
            "generate": "/generate",
            "schedule": "/schedule",
            "schedule_interval": "/schedule_interval",
            "jobs": "/jobs",
            "remove_job": "/jobs/{job_name}",
            "save_schedule": "/schedule/save",
            "load_schedule": "/schedule/load"
        }
    }

@app.post("/execute")
async def execute_workflow(request: WorkflowRequest):
    """Execute a workflow from a natural language request"""
    try:
        logger.info(f"Executing workflow: {request.user_request}")
        
        # Generate and execute workflow
        results = await executor.generate_and_execute(request.user_request)
        
        # Save results
        filepath = executor.save_results(results)
        
        return {
            "success": True,
            "message": "Workflow executed successfully",
            "results_file": filepath,
            "workflow_summary": results.get("workflow_summary", ""),
            "execution_stats": {
                "steps_executed": results.get("steps_executed", 0),
                "total_steps": results.get("total_steps", 0),
                "success": results.get("success", False),
                "errors": results.get("errors", [])
            }
        }
        
    except Exception as e:
        logger.error(f"Workflow execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
async def generate_workflow(request: WorkflowRequest):
    """Generate a workflow from a natural language request without executing it"""
    try:
        logger.info(f"Generating workflow: {request.user_request}")
        
        # Generate workflow
        workflow = gemini.generate_workflow(request.user_request)
        
        # Validate workflow
        if not gemini.validate_workflow(workflow):
            raise ValueError("Generated workflow is invalid")
        
        # Save workflow
        os.makedirs("workflows", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"workflow_{timestamp}.json"
        filepath = os.path.join("workflows", filename)
        
        with open(filepath, 'w') as f:
            json.dump(workflow, f, indent=2)
        
        return {
            "success": True,
            "message": "Workflow generated successfully",
            "workflow_file": filepath,
            "workflow": workflow,
            "workflow_summary": gemini.get_workflow_summary(workflow)
        }
        
    except Exception as e:
        logger.error(f"Workflow generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute_file")
async def execute_workflow_file(request: WorkflowFileRequest):
    """Execute a workflow from a saved file"""
    try:
        logger.info(f"Executing workflow from file: {request.filepath}")
        
        # Load workflow
        workflow = executor.load_workflow(request.filepath)
        
        # Execute workflow
        results = await executor.execute_workflow(workflow)
        
        # Save results
        filepath = executor.save_results(results)
        
        return {
            "success": True,
            "message": "Workflow executed successfully",
            "results_file": filepath,
            "workflow_summary": gemini.get_workflow_summary(workflow),
            "execution_stats": {
                "steps_executed": results.get("steps_executed", 0),
                "total_steps": results.get("total_steps", 0),
                "success": results.get("success", False),
                "errors": results.get("errors", [])
            }
        }
        
    except Exception as e:
        logger.error(f"Workflow file execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/schedule")
async def schedule_workflow(request: ScheduleRequest):
    """Schedule a workflow to run at a specific time"""
    try:
        logger.info(f"Scheduling workflow: {request.user_request} for {request.schedule_time}")
        
        # Schedule workflow
        job_name = scheduler.schedule_workflow_from_request(
            request.user_request,
            request.schedule_time,
            request.job_name,
            request.repeat
        )
        
        return {
            "success": True,
            "message": "Workflow scheduled successfully",
            "job_name": job_name,
            "schedule_time": request.schedule_time,
            "repeat": request.repeat
        }
        
    except Exception as e:
        logger.error(f"Workflow scheduling failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/schedule_interval")
async def schedule_interval_workflow(request: IntervalRequest):
    """Schedule a workflow to run at regular intervals"""
    try:
        logger.info(f"Scheduling interval workflow: {request.user_request} every {request.interval_minutes} minutes")
        
        # Generate workflow
        workflow = gemini.generate_workflow(request.user_request)
        
        # Schedule workflow
        job_name = scheduler.schedule_interval_workflow(
            workflow,
            request.interval_minutes,
            request.job_name
        )
        
        return {
            "success": True,
            "message": "Interval workflow scheduled successfully",
            "job_name": job_name,
            "interval_minutes": request.interval_minutes
        }
        
    except Exception as e:
        logger.error(f"Interval workflow scheduling failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs")
async def get_scheduled_jobs():
    """Get all scheduled jobs"""
    try:
        jobs = scheduler.get_scheduled_jobs()
        return {
            "success": True,
            "jobs": jobs,
            "total_jobs": len(jobs)
        }
        
    except Exception as e:
        logger.error(f"Failed to get scheduled jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs/{job_name}")
async def get_job_status(job_name: str):
    """Get status of a specific job"""
    try:
        job_status = scheduler.get_job_status(job_name)
        if not job_status:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return {
            "success": True,
            "job_name": job_name,
            "status": job_status
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get job status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/jobs/{job_name}")
async def remove_job(job_name: str):
    """Remove a scheduled job"""
    try:
        success = scheduler.remove_job(job_name)
        if not success:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return {
            "success": True,
            "message": f"Job '{job_name}' removed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to remove job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/schedule/save")
async def save_schedule():
    """Save the current schedule to a file"""
    try:
        filepath = scheduler.save_schedule()
        return {
            "success": True,
            "message": "Schedule saved successfully",
            "filepath": filepath
        }
        
    except Exception as e:
        logger.error(f"Failed to save schedule: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/schedule/load")
async def load_schedule(request: ScheduleFileRequest):
    """Load a schedule from a file"""
    try:
        scheduler.load_schedule(request.filepath)
        return {
            "success": True,
            "message": "Schedule loaded successfully",
            "filepath": request.filepath
        }
        
    except Exception as e:
        logger.error(f"Failed to load schedule: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "scheduler_running": scheduler.running
    }

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down application...")
    scheduler.stop_scheduler()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)