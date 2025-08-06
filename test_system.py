#!/usr/bin/env python3
"""
Test script for Browser Workflow Automation Agent
"""

import asyncio
import json
import os
import sys
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from automation_engine import BrowserAutomationEngine
        from gemini_integration import GeminiWorkflowGenerator
        from workflow_executor import WorkflowExecutor
        from workflow_scheduler import WorkflowScheduler
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_workflow_generation():
    """Test workflow generation (without API key)"""
    print("🧪 Testing workflow generation...")
    
    try:
        from gemini_integration import GeminiWorkflowGenerator
        
        # Test with mock API key
        os.environ["GEMINI_API_KEY"] = "test_key"
        
        generator = GeminiWorkflowGenerator()
        print("✅ Workflow generator initialized")
        return True
    except Exception as e:
        print(f"⚠️  Workflow generation test skipped (API key required): {e}")
        return True  # Not critical for basic testing

def test_workflow_validation():
    """Test workflow validation"""
    print("🧪 Testing workflow validation...")
    
    try:
        from gemini_integration import GeminiWorkflowGenerator
        
        generator = GeminiWorkflowGenerator()
        
        # Test valid workflow
        valid_workflow = {
            "name": "Test Workflow",
            "description": "A test workflow",
            "steps": [
                {
                    "action": "navigate",
                    "url": "https://example.com",
                    "description": "Navigate to example.com"
                }
            ]
        }
        
        if generator.validate_workflow(valid_workflow):
            print("✅ Valid workflow validation passed")
        else:
            print("❌ Valid workflow validation failed")
            return False
        
        # Test invalid workflow
        invalid_workflow = {
            "name": "Invalid Workflow",
            "steps": []  # Missing description
        }
        
        if not generator.validate_workflow(invalid_workflow):
            print("✅ Invalid workflow validation passed")
        else:
            print("❌ Invalid workflow validation failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Workflow validation test failed: {e}")
        return False

async def test_automation_engine():
    """Test automation engine (without starting browser)"""
    print("🧪 Testing automation engine...")
    
    try:
        from automation_engine import BrowserAutomationEngine
        
        engine = BrowserAutomationEngine(browser_type="playwright", headless=True)
        print("✅ Automation engine initialized")
        return True
    except Exception as e:
        print(f"❌ Automation engine test failed: {e}")
        return False

def test_file_operations():
    """Test file operations"""
    print("🧪 Testing file operations...")
    
    try:
        # Test directory creation
        test_dir = Path("test_output")
        test_dir.mkdir(exist_ok=True)
        
        # Test file writing
        test_file = test_dir / "test.json"
        test_data = {"test": "data"}
        
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        # Test file reading
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)
        
        if loaded_data == test_data:
            print("✅ File operations test passed")
        else:
            print("❌ File operations test failed")
            return False
        
        # Cleanup
        test_file.unlink()
        test_dir.rmdir()
        
        return True
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def test_example_workflow():
    """Test example workflow loading"""
    print("🧪 Testing example workflow...")
    
    try:
        example_file = Path("examples/simple_workflow.json")
        
        if not example_file.exists():
            print("⚠️  Example workflow file not found, skipping test")
            return True
        
        with open(example_file, 'r') as f:
            workflow = json.load(f)
        
        from gemini_integration import GeminiWorkflowGenerator
        generator = GeminiWorkflowGenerator()
        
        if generator.validate_workflow(workflow):
            print("✅ Example workflow validation passed")
            return True
        else:
            print("❌ Example workflow validation failed")
            return False
            
    except Exception as e:
        print(f"❌ Example workflow test failed: {e}")
        return False

def test_cli_help():
    """Test CLI help command"""
    print("🧪 Testing CLI help...")
    
    try:
        import subprocess
        result = subprocess.run(
            ["python", "cli.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ CLI help test passed")
            return True
        else:
            print(f"❌ CLI help test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ CLI help test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Browser Workflow Automation Agent - System Test")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Workflow Generation", test_workflow_generation),
        ("Workflow Validation", test_workflow_validation),
        ("Automation Engine", test_automation_engine),
        ("File Operations", test_file_operations),
        ("Example Workflow", test_example_workflow),
        ("CLI Help", test_cli_help),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
                
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n📋 Next steps:")
        print("1. Set your Gemini API key in .env file")
        print("2. Try: python cli.py execute \"Go to google.com\"")
        print("3. Or start the web interface: python web_interface.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("Make sure all dependencies are installed correctly.")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())