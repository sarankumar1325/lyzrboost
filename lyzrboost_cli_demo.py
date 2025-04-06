"""
LyzrBoost CLI Demo

This script demonstrates how to build a command-line interface using LyzrBoost.
It provides commands for interacting with Lyzr agents and running workflows.

Usage:
    python lyzrboost_cli_demo.py chat --agent your_agent_id --message "Your message"
    python lyzrboost_cli_demo.py run --config workflow_config.yaml --input "Your input"
"""

import os
import sys
import argparse
import yaml
from typing import Dict, Any

from lyzrboost.core.agent_api import get_agent_response, APIError
from lyzrboost.utils.logger import setup_logger
from config_workflow_demo import load_workflow_config, build_workflow_from_config

# Configure logging
logger = setup_logger(name="lyzrboost_cli", level="INFO")

# Default user ID (replace with your user ID)
DEFAULT_USER_ID = "your_user_id"  # Replace with your user ID

def chat_command(args):
    """
    Handle the 'chat' command to interact with a Lyzr agent.
    
    Args:
        args: Command line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        print(f"Sending message to agent {args.agent}...")
        
        # Use LyzrBoost's simplified API to get a response
        response = get_agent_response(
            user_id=args.user_id,
            agent_id=args.agent,
            message=args.message,
            timeout=args.timeout
        )
        
        # Print the response
        print("\nAgent Response:")
        print("=" * 80)
        print(response)
        print("-" * 80)
        
        return 0
        
    except APIError as e:
        logger.error(f"API Error: {str(e)}")
        print(f"API Error: {str(e)}")
        return 1
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"Error: {str(e)}")
        return 1

def run_command(args):
    """
    Handle the 'run' command to execute a workflow from a configuration file.
    
    Args:
        args: Command line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        # Load workflow configuration
        config = load_workflow_config(args.config)
        
        # Build workflow from configuration
        workflow = build_workflow_from_config(config)
        
        # Get workflow input
        workflow_input = args.input
        
        # Run the workflow
        print(f"Starting workflow: {workflow.name}")
        print(f"Description: {workflow.description}")
        print("-" * 80)
        
        result = workflow.run(workflow_input)
        
        # Print the result
        print("\nWorkflow Result:")
        print("=" * 80)
        
        # Format the output based on the configuration
        output_format = config.get("output_format", "default")
        
        if output_format == "default":
            # Print the entire result dictionary
            for key, value in result.items():
                if isinstance(value, str) and len(value) > 100:
                    # Truncate long strings for display
                    print(f"{key}: {value[:100]}...")
                else:
                    print(f"{key}: {value}")
        elif output_format == "final_only":
            # Print only the final output
            final_key = config.get("final_output_key", "response")
            if final_key in result:
                print(result[final_key])
            else:
                print(f"Final output key '{final_key}' not found in result")
        else:
            # Default to printing the entire result
            print(result)
            
        return 0
        
    except Exception as e:
        logger.error(f"Workflow failed: {str(e)}")
        print(f"Error: {str(e)}")
        return 1

def debug_command(args):
    """
    Handle the 'debug' command to test an agent with detailed logging.
    
    Args:
        args: Command line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    # Set debug logging level
    logger.setLevel("DEBUG")
    
    try:
        print(f"DEBUG MODE: Sending message to agent {args.agent}...")
        print(f"User ID: {args.user_id}")
        print(f"Agent ID: {args.agent}")
        print(f"Message: {args.message}")
        print("-" * 80)
        
        # Use LyzrBoost's simplified API to get a response
        response = get_agent_response(
            user_id=args.user_id,
            agent_id=args.agent,
            message=args.message,
            timeout=args.timeout
        )
        
        # Print the response
        print("\nAgent Response:")
        print("=" * 80)
        print(response)
        print("-" * 80)
        
        return 0
        
    except APIError as e:
        logger.error(f"API Error: {str(e)}")
        print(f"API Error: {str(e)}")
        return 1
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"Error: {str(e)}")
        return 1

def version_command(args):
    """
    Handle the 'version' command to display version information.
    
    Args:
        args: Command line arguments
        
    Returns:
        Exit code (0 for success)
    """
    print("LyzrBoost CLI Demo")
    print("Version: 0.1.0")
    print("A demonstration of LyzrBoost's CLI capabilities")
    return 0

def main():
    # Create the main parser
    parser = argparse.ArgumentParser(description="LyzrBoost CLI Demo")
    parser.add_argument("--api-key", help="Lyzr API key (or set LYZR_API_KEY environment variable)")
    parser.add_argument("--user-id", help="User ID for Lyzr API", default=DEFAULT_USER_ID)
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Chat with a Lyzr agent")
    chat_parser.add_argument("--agent", required=True, help="Agent ID to interact with")
    chat_parser.add_argument("--message", required=True, help="Message to send to the agent")
    chat_parser.add_argument("--timeout", type=int, default=60, help="Timeout in seconds")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run a workflow from a configuration file")
    run_parser.add_argument("--config", required=True, help="Path to workflow configuration YAML file")
    run_parser.add_argument("--input", required=True, help="Input for the workflow")
    
    # Debug command
    debug_parser = subparsers.add_parser("debug", help="Debug an agent interaction")
    debug_parser.add_argument("--agent", required=True, help="Agent ID to interact with")
    debug_parser.add_argument("--message", required=True, help="Message to send to the agent")
    debug_parser.add_argument("--timeout", type=int, default=60, help="Timeout in seconds")
    
    # Version command
    version_parser = subparsers.add_parser("version", help="Display version information")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set API key from args or environment
    if args.api_key:
        os.environ["LYZR_API_KEY"] = args.api_key
    
    # Set logging level based on verbosity
    if args.verbose:
        logger.setLevel("DEBUG")
    
    # Handle commands
    if args.command == "chat":
        return chat_command(args)
    elif args.command == "run":
        return run_command(args)
    elif args.command == "debug":
        return debug_command(args)
    elif args.command == "version":
        return version_command(args)
    else:
        # No command specified, show help
        parser.print_help()
        return 0

if __name__ == "__main__":
    sys.exit(main())
