#!/usr/bin/env python3
"""
Test runner for PizzaTrinity project
Usage: python run_tests.py
"""

import subprocess
import sys
import os

def run_command(command):
    """Run command and return result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🧪 PizzaTrinity Test Runner")
    print("=" * 50)
    
    # Check if pytest is installed
    success, _, _ = run_command("pytest --version")
    if not success:
        print("❌ pytest not found. Installing dependencies...")
        success, output, error = run_command("pip install -r requirements.txt")
        if not success:
            print(f"❌ Failed to install dependencies: {error}")
            sys.exit(1)
        print("✅ Dependencies installed successfully!")
    
    # Run unit tests
    print("\n🔬 Running Unit Tests...")
    success, output, error = run_command("pytest test_pizza_trinity.py::TestPizza -v")
    if success:
        print("✅ Unit tests passed!")
    else:
        print("❌ Some unit tests failed:")
        print(error)
    
    # Run all tests with coverage
    print("\n📊 Running All Tests with Coverage...")
    success, output, error = run_command("pytest test_pizza_trinity.py --cov=PizzaTrinity --cov-report=term-missing")
    
    if success:
        print("✅ All tests passed!")
        print("\n📈 Test Summary:")
        print(output)
        
        # Generate HTML coverage report
        print("\n📄 Generating HTML coverage report...")
        run_command("pytest test_pizza_trinity.py --cov=PizzaTrinity --cov-report=html")
        print("📁 Coverage report generated in htmlcov/index.html")
        
    else:
        print("❌ Some tests failed:")
        print(error)
        sys.exit(1)
    
    print("\n🎉 Testing completed!")

if __name__ == "__main__":
    main()
