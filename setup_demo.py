"""
Setup script for LyzrBoost demos.

This script installs the required dependencies for running the LyzrBoost demos.
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if the Python version is compatible."""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        sys.exit(1)

def install_dependencies():
    """Install the required dependencies."""
    print("Installing dependencies...")
    
    # List of required packages
    packages = [
        "lyzr",       # Lyzr SDK
        "lyzrboost",  # LyzrBoost package
        "pyyaml",     # For YAML configuration
        "requests",   # For API requests
    ]
    
    # Install each package
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"Error: Failed to install {package}")
            sys.exit(1)

def setup_environment():
    """Set up the environment variables."""
    print("\nSetting up environment...")
    
    # Check if LYZR_API_KEY is already set
    if "LYZR_API_KEY" in os.environ:
        print("LYZR_API_KEY environment variable is already set.")
    else:
        # Prompt for API key
        api_key = input("Enter your Lyzr API key (or press Enter to skip): ")
        if api_key:
            os.environ["LYZR_API_KEY"] = api_key
            print("LYZR_API_KEY environment variable set.")
        else:
            print("No API key provided. You'll need to provide it when running the demos.")

def print_instructions():
    """Print instructions for running the demos."""
    print("\n" + "=" * 80)
    print("LyzrBoost Demos Setup Complete!")
    print("=" * 80)
    print("\nYou can now run the demo applications:")
    print("\n1. Simple Agent Demo:")
    print("   python simple_agent_demo.py \"What is artificial intelligence?\" --agent-id YOUR_AGENT_ID")
    
    print("\n2. Content Generation Workflow Demo:")
    print("   python demo_content_generator.py \"Artificial Intelligence\"")
    
    print("\n3. Configuration-Driven Workflow Demo:")
    print("   python config_workflow_demo.py workflow_config.yaml --input \"Artificial Intelligence\"")
    
    print("\n4. CLI Demo:")
    print("   python lyzrboost_cli_demo.py chat --agent YOUR_AGENT_ID --message \"What is AI?\"")
    
    print("\n5. ChatBot Integration Demo:")
    print("   python chatbot_demo.py path/to/document.pdf \"What is this document about?\"")
    
    print("\nFor more information, see the README_DEMO.md file.")
    print("=" * 80)

def main():
    """Main function."""
    print("Setting up LyzrBoost demos...")
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Set up environment
    setup_environment()
    
    # Print instructions
    print_instructions()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
