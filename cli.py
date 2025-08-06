#!/usr/bin/env python3
"""
Command Line Interface for Browser Workflow Automation Agent
"""

import asyncio
import argparse
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any

from workflow_executor import WorkflowExecutor
from workflow_scheduler import WorkflowScheduler
from gemini_integration import GeminiWorkflowGenerator

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🚀 Browser Workflow Automation Agent")
    print("=" * 60)
    print("Powered by Playwright, Selenium, and Gemini AI")
    print("=" * 60)

def print_workflow_summary(workflow: Dict[str, Any]):
    """Print a formatted workflow summary"""
    print(f"\n📋 Workflow: {workflow.get('name', 'Unknown')}")
    print(f"📝 Description: {workflow.get('description', 'No description')}")
    print(f"🔢 Steps: {len(workflow.get('steps', []))}")
    print("\n📋 Steps:")
    for i, step in enumerate(workflow.get('steps', []), 1):
        action = step.get('action', 'unknown').upper()
        desc = step.get('description', 'No description')
        print(f"  {i}. {action}: {desc}")

def print_execution_results(results: Dict[str, Any]):
    """Print execution results in a formatted way"""
    print(f"\n✅ Execution Results:")
    print(f"   Workflow: {results.get('workflow_name', 'Unknown')}")
    print(f"   Status: {'✅ Success' if results.get('success') else '❌ Failed'}")
    print(f"   Steps: {results.get('steps_executed', 0)}/{results.get('total_steps', 0)}")
    print(f"   Duration: {results.get('start_time', 'Unknown')} to {results.get('end_time', 'Unknown')}")
    
    if results.get('screenshots'):
        print(f"   Screenshots: {len(results['screenshots'])} taken")
        for screenshot in results['screenshots']:
            print(f"     - {screenshot}")
    
    if results.get('extracted_data'):
        print(f"   Extracted Data:")
        for key, value in results['extracted_data'].items():
            print(f"     - {key}: {value[:100]}{'...' if len(str(value)) > 100 else ''}")
    
    if results.get('errors'):
        print(f"   Errors:")
        for error in results['errors']:
            print(f"     - {error}")

async def execute_workflow(args):
    """Execute a workflow from command line arguments"""
    try:
        print_banner()
        print(f"\n🎯 Executing workflow: {args.request}")
        
        # Initialize executor
        executor = WorkflowExecutor(
            browser_type=args.browser_type,
            headless=args.headless
        )
        
        # Generate and execute workflow
        results = await executor.generate_and_execute(args.request)
        
        # Print results
        print_execution_results(results)
        
        # Save results if requested
        if args.save_results:
            filepath = executor.save_results(results)
            print(f"\n💾 Results saved to: {filepath}")
        
        return results
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

async def generate_workflow(args):
    """Generate a workflow without executing it"""
    try:
        print_banner()
        print(f"\n🎯 Generating workflow: {args.request}")
        
        # Initialize generator
        gemini = GeminiWorkflowGenerator()
        
        # Generate workflow
        workflow = gemini.generate_workflow(args.request)
        
        # Print workflow summary
        print_workflow_summary(workflow)
        
        # Save workflow if requested
        if args.save_workflow:
            os.makedirs("workflows", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"workflow_{timestamp}.json"
            filepath = os.path.join("workflows", filename)
            
            with open(filepath, 'w') as f:
                json.dump(workflow, f, indent=2)
            
            print(f"\n💾 Workflow saved to: {filepath}")
        
        return workflow
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

async def schedule_workflow(args):
    """Schedule a workflow"""
    try:
        print_banner()
        print(f"\n⏰ Scheduling workflow: {args.request}")
        print(f"   Time: {args.time}")
        print(f"   Repeat: {'Yes' if args.repeat else 'No'}")
        
        # Initialize scheduler
        scheduler = WorkflowScheduler(
            browser_type=args.browser_type,
            headless=args.headless
        )
        
        # Schedule workflow
        job_name = scheduler.schedule_workflow_from_request(
            args.request,
            args.time,
            args.job_name,
            args.repeat
        )
        
        print(f"\n✅ Workflow scheduled successfully!")
        print(f"   Job Name: {job_name}")
        print(f"   Schedule Time: {args.time}")
        print(f"   Repeat: {'Yes' if args.repeat else 'No'}")
        
        # Start scheduler if requested
        if args.start_scheduler:
            print(f"\n🚀 Starting scheduler...")
            scheduler.start_scheduler()
            
            try:
                # Keep scheduler running
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print(f"\n⏹️  Stopping scheduler...")
                scheduler.stop_scheduler()
        
        return job_name
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

async def schedule_interval_workflow(args):
    """Schedule a workflow to run at intervals"""
    try:
        print_banner()
        print(f"\n⏰ Scheduling interval workflow: {args.request}")
        print(f"   Interval: {args.interval} minutes")
        
        # Initialize scheduler
        scheduler = WorkflowScheduler(
            browser_type=args.browser_type,
            headless=args.headless
        )
        
        # Generate workflow
        gemini = GeminiWorkflowGenerator()
        workflow = gemini.generate_workflow(args.request)
        
        # Schedule workflow
        job_name = scheduler.schedule_interval_workflow(
            workflow,
            args.interval,
            args.job_name
        )
        
        print(f"\n✅ Interval workflow scheduled successfully!")
        print(f"   Job Name: {job_name}")
        print(f"   Interval: {args.interval} minutes")
        
        # Start scheduler if requested
        if args.start_scheduler:
            print(f"\n🚀 Starting scheduler...")
            scheduler.start_scheduler()
            
            try:
                # Keep scheduler running
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print(f"\n⏹️  Stopping scheduler...")
                scheduler.stop_scheduler()
        
        return job_name
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

async def list_jobs(args):
    """List scheduled jobs"""
    try:
        print_banner()
        print(f"\n📋 Scheduled Jobs:")
        
        # Initialize scheduler
        scheduler = WorkflowScheduler()
        
        # Get jobs
        jobs = scheduler.get_scheduled_jobs()
        
        if not jobs:
            print("   No scheduled jobs found.")
            return
        
        for job_name, job_info in jobs.items():
            print(f"\n   🔹 Job: {job_name}")
            print(f"      Created: {job_info.get('created_at', 'Unknown')}")
            print(f"      Last Run: {job_info.get('last_run', 'Never')}")
            
            if 'schedule_time' in job_info:
                print(f"      Schedule: {job_info['schedule_time']} {'(Daily)' if job_info.get('repeat') else '(Once)'}")
            elif 'interval_minutes' in job_info:
                print(f"      Interval: Every {job_info['interval_minutes']} minutes")
            
            if job_info.get('last_error'):
                print(f"      Last Error: {job_info['last_error']}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

async def remove_job(args):
    """Remove a scheduled job"""
    try:
        print_banner()
        print(f"\n🗑️  Removing job: {args.job_name}")
        
        # Initialize scheduler
        scheduler = WorkflowScheduler()
        
        # Remove job
        success = scheduler.remove_job(args.job_name)
        
        if success:
            print(f"✅ Job '{args.job_name}' removed successfully!")
        else:
            print(f"❌ Job '{args.job_name}' not found.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Browser Workflow Automation Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute a workflow immediately
  python cli.py execute "Go to google.com and search for 'python automation'"
  
  # Generate a workflow without executing
  python cli.py generate "Login to a website" --save-workflow
  
  # Schedule a workflow to run daily at 9 AM
  python cli.py schedule "Check website status" --time "09:00" --repeat --start-scheduler
  
  # Schedule a workflow to run every 30 minutes
  python cli.py interval "Monitor website" --interval 30 --start-scheduler
  
  # List scheduled jobs
  python cli.py list-jobs
  
  # Remove a scheduled job
  python cli.py remove-job "my_workflow"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Execute command
    execute_parser = subparsers.add_parser('execute', help='Execute a workflow immediately')
    execute_parser.add_argument('request', help='Natural language description of the workflow')
    execute_parser.add_argument('--browser-type', choices=['playwright', 'selenium'], default='playwright', help='Browser type to use')
    execute_parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    execute_parser.add_argument('--save-results', action='store_true', help='Save execution results to file')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a workflow without executing')
    generate_parser.add_argument('request', help='Natural language description of the workflow')
    generate_parser.add_argument('--save-workflow', action='store_true', help='Save workflow to file')
    
    # Schedule command
    schedule_parser = subparsers.add_parser('schedule', help='Schedule a workflow to run at a specific time')
    schedule_parser.add_argument('request', help='Natural language description of the workflow')
    schedule_parser.add_argument('--time', required=True, help='Time in HH:MM format (e.g., 09:30)')
    schedule_parser.add_argument('--job-name', help='Optional name for the job')
    schedule_parser.add_argument('--repeat', action='store_true', help='Repeat daily')
    schedule_parser.add_argument('--browser-type', choices=['playwright', 'selenium'], default='playwright', help='Browser type to use')
    schedule_parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    schedule_parser.add_argument('--start-scheduler', action='store_true', help='Start the scheduler after scheduling')
    
    # Interval command
    interval_parser = subparsers.add_parser('interval', help='Schedule a workflow to run at intervals')
    interval_parser.add_argument('request', help='Natural language description of the workflow')
    interval_parser.add_argument('--interval', type=int, required=True, help='Interval in minutes')
    interval_parser.add_argument('--job-name', help='Optional name for the job')
    interval_parser.add_argument('--browser-type', choices=['playwright', 'selenium'], default='playwright', help='Browser type to use')
    interval_parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    interval_parser.add_argument('--start-scheduler', action='store_true', help='Start the scheduler after scheduling')
    
    # List jobs command
    list_parser = subparsers.add_parser('list-jobs', help='List all scheduled jobs')
    
    # Remove job command
    remove_parser = subparsers.add_parser('remove-job', help='Remove a scheduled job')
    remove_parser.add_argument('job_name', help='Name of the job to remove')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute appropriate command
    if args.command == 'execute':
        asyncio.run(execute_workflow(args))
    elif args.command == 'generate':
        asyncio.run(generate_workflow(args))
    elif args.command == 'schedule':
        asyncio.run(schedule_workflow(args))
    elif args.command == 'interval':
        asyncio.run(schedule_interval_workflow(args))
    elif args.command == 'list-jobs':
        asyncio.run(list_jobs(args))
    elif args.command == 'remove-job':
        asyncio.run(remove_job(args))

if __name__ == "__main__":
    main()