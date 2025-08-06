import schedule
import time
import threading
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from workflow_executor import WorkflowExecutor
from gemini_integration import GeminiWorkflowGenerator
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowScheduler:
    def __init__(self, browser_type: str = "playwright", headless: bool = True):
        self.browser_type = browser_type
        self.headless = headless
        self.scheduled_jobs = {}
        self.executor = WorkflowExecutor(browser_type, headless)
        self.gemini = GeminiWorkflowGenerator()
        self.running = False
        self.scheduler_thread = None
        
    def schedule_workflow(self, 
                         workflow: Dict[str, Any], 
                         schedule_time: str, 
                         job_name: str = None,
                         repeat: bool = False) -> str:
        """
        Schedule a workflow to run at a specific time
        
        Args:
            workflow: The workflow to execute
            schedule_time: Time in HH:MM format (e.g., "14:30")
            job_name: Optional name for the job
            repeat: Whether to repeat daily
            
        Returns:
            Job ID
        """
        if not job_name:
            job_name = f"workflow_{len(self.scheduled_jobs) + 1}"
        
        def job_function():
            try:
                logger.info(f"Executing scheduled workflow: {job_name}")
                asyncio.run(self._execute_scheduled_workflow(workflow, job_name))
            except Exception as e:
                logger.error(f"Scheduled workflow {job_name} failed: {e}")
        
        if repeat:
            schedule.every().day.at(schedule_time).do(job_function).tag(job_name)
        else:
            schedule.every().day.at(schedule_time).do(job_function).tag(job_name)
        
        self.scheduled_jobs[job_name] = {
            "workflow": workflow,
            "schedule_time": schedule_time,
            "repeat": repeat,
            "created_at": datetime.now().isoformat(),
            "last_run": None,
            "next_run": self._get_next_run_time(schedule_time)
        }
        
        logger.info(f"Scheduled workflow '{job_name}' for {schedule_time}")
        return job_name
    
    def schedule_workflow_from_request(self, 
                                     user_request: str, 
                                     schedule_time: str, 
                                     job_name: str = None,
                                     repeat: bool = False) -> str:
        """
        Generate a workflow from user request and schedule it
        
        Args:
            user_request: Natural language description of the workflow
            schedule_time: Time in HH:MM format
            job_name: Optional name for the job
            repeat: Whether to repeat daily
            
        Returns:
            Job ID
        """
        try:
            # Generate workflow
            workflow = self.gemini.generate_workflow(user_request)
            
            if not self.gemini.validate_workflow(workflow):
                raise ValueError("Generated workflow is invalid")
            
            # Schedule the workflow
            return self.schedule_workflow(workflow, schedule_time, job_name, repeat)
            
        except Exception as e:
            logger.error(f"Failed to schedule workflow from request: {e}")
            raise
    
    def schedule_interval_workflow(self, 
                                 workflow: Dict[str, Any], 
                                 interval_minutes: int, 
                                 job_name: str = None) -> str:
        """
        Schedule a workflow to run at regular intervals
        
        Args:
            workflow: The workflow to execute
            interval_minutes: Interval in minutes
            job_name: Optional name for the job
            
        Returns:
            Job ID
        """
        if not job_name:
            job_name = f"interval_workflow_{len(self.scheduled_jobs) + 1}"
        
        def job_function():
            try:
                logger.info(f"Executing interval workflow: {job_name}")
                asyncio.run(self._execute_scheduled_workflow(workflow, job_name))
            except Exception as e:
                logger.error(f"Interval workflow {job_name} failed: {e}")
        
        schedule.every(interval_minutes).minutes.do(job_function).tag(job_name)
        
        self.scheduled_jobs[job_name] = {
            "workflow": workflow,
            "interval_minutes": interval_minutes,
            "repeat": True,
            "created_at": datetime.now().isoformat(),
            "last_run": None,
            "next_run": datetime.now() + timedelta(minutes=interval_minutes)
        }
        
        logger.info(f"Scheduled interval workflow '{job_name}' every {interval_minutes} minutes")
        return job_name
    
    async def _execute_scheduled_workflow(self, workflow: Dict[str, Any], job_name: str):
        """Execute a scheduled workflow and update job status"""
        try:
            # Execute workflow
            results = await self.executor.execute_workflow(workflow)
            
            # Update job status
            if job_name in self.scheduled_jobs:
                self.scheduled_jobs[job_name]["last_run"] = datetime.now().isoformat()
                self.scheduled_jobs[job_name]["last_result"] = results
            
            # Save results
            filename = f"scheduled_{job_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            self.executor.save_results(results, filename)
            
            logger.info(f"Scheduled workflow '{job_name}' completed successfully")
            
        except Exception as e:
            logger.error(f"Scheduled workflow '{job_name}' failed: {e}")
            if job_name in self.scheduled_jobs:
                self.scheduled_jobs[job_name]["last_error"] = str(e)
    
    def _get_next_run_time(self, schedule_time: str) -> datetime:
        """Calculate the next run time for a scheduled job"""
        try:
            hour, minute = map(int, schedule_time.split(':'))
            now = datetime.now()
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            if next_run <= now:
                next_run += timedelta(days=1)
            
            return next_run
        except Exception as e:
            logger.error(f"Failed to calculate next run time: {e}")
            return datetime.now() + timedelta(days=1)
    
    def start_scheduler(self):
        """Start the scheduler in a separate thread"""
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        self.running = True
        
        def run_scheduler():
            logger.info("Scheduler started")
            while self.running:
                schedule.run_pending()
                time.sleep(1)
            logger.info("Scheduler stopped")
        
        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        logger.info("Scheduler stopped")
    
    def remove_job(self, job_name: str) -> bool:
        """Remove a scheduled job"""
        try:
            schedule.clear(job_name)
            if job_name in self.scheduled_jobs:
                del self.scheduled_jobs[job_name]
            logger.info(f"Removed scheduled job: {job_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to remove job {job_name}: {e}")
            return False
    
    def get_scheduled_jobs(self) -> Dict[str, Any]:
        """Get all scheduled jobs"""
        return self.scheduled_jobs.copy()
    
    def get_job_status(self, job_name: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific job"""
        return self.scheduled_jobs.get(job_name)
    
    def save_schedule(self, filename: str = None) -> str:
        """Save the current schedule to a JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"schedule_{timestamp}.json"
        
        try:
            os.makedirs("schedules", exist_ok=True)
            filepath = os.path.join("schedules", filename)
            
            # Convert datetime objects to strings for JSON serialization
            schedule_data = {}
            for job_name, job_info in self.scheduled_jobs.items():
                schedule_data[job_name] = job_info.copy()
                if isinstance(job_info.get("next_run"), datetime):
                    schedule_data[job_name]["next_run"] = job_info["next_run"].isoformat()
            
            with open(filepath, 'w') as f:
                json.dump(schedule_data, f, indent=2)
            
            logger.info(f"Schedule saved to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to save schedule: {e}")
            raise
    
    def load_schedule(self, filepath: str):
        """Load a schedule from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                schedule_data = json.load(f)
            
            # Clear existing schedule
            schedule.clear()
            self.scheduled_jobs.clear()
            
            # Load jobs
            for job_name, job_info in schedule_data.items():
                workflow = job_info["workflow"]
                
                if "interval_minutes" in job_info:
                    # Interval job
                    self.schedule_interval_workflow(
                        workflow, 
                        job_info["interval_minutes"], 
                        job_name
                    )
                else:
                    # Time-based job
                    self.schedule_workflow(
                        workflow,
                        job_info["schedule_time"],
                        job_name,
                        job_info.get("repeat", False)
                    )
            
            logger.info(f"Schedule loaded from {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to load schedule: {e}")
            raise