"""
Command-line interface for LyzrBoost.
"""

import argparse
import sys
import os
import logging
from typing import List, Optional, Dict, Any

from ..core.agent_api import send_agent_request, get_agent_response, APIError
from ..core.workflow import Workflow, create_workflow_from_config
from ..utils.config import load_config, ConfigError
from ..utils.logger import setup_logger

def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the LyzrBoost CLI.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    if args is None:
        args = sys.argv[1:]
        
    # Set up the main parser
    parser = argparse.ArgumentParser(
        description="LyzrBoost - Tools for Lyzr AI agent orchestration"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times)"
    )
    parser.add_argument(
        "--api-key",
        help="Lyzr API key (defaults to LYZR_API_KEY environment variable)"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # 'run' command - Run a workflow
    run_parser = subparsers.add_parser("run", help="Run a workflow")
    run_parser.add_argument("workflow_file", help="Path to workflow configuration file")
    run_parser.add_argument("--input", "-i", help="Input data for the workflow")
    
    # 'debug' command - Debug an agent interaction
    debug_parser = subparsers.add_parser("debug", help="Debug an agent interaction")
    debug_parser.add_argument("--agent", required=True, help="Agent ID to interact with")
    debug_parser.add_argument("--user", required=True, help="User ID for the request")
    debug_parser.add_argument("--session", help="Session ID (defaults to agent ID if not provided)")
    debug_parser.add_argument("--message", "-m", required=True, help="Message to send to the agent")
    
    # 'version' command - Show version information
    version_parser = subparsers.add_parser("version", help="Show version information")
    
    # Parse arguments
    parsed_args = parser.parse_args(args)
    
    # Set up logging based on verbosity
    log_level = logging.WARNING
    if parsed_args.verbose == 1:
        log_level = logging.INFO
    elif parsed_args.verbose >= 2:
        log_level = logging.DEBUG
        
    logger = setup_logger(level=log_level)
    
    # Get API key from args or environment
    api_key = parsed_args.api_key or os.environ.get("LYZR_API_KEY")
    
    # Handle commands
    try:
        if parsed_args.command == "run":
            return run_workflow_command(parsed_args, api_key, logger)
        elif parsed_args.command == "debug":
            return debug_agent_command(parsed_args, api_key, logger)
        elif parsed_args.command == "version":
            return show_version_command()
        else:
            # No command specified, show help
            parser.print_help()
            return 0
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

def run_workflow_command(args: argparse.Namespace, api_key: Optional[str], logger: logging.Logger) -> int:
    """
    Run a workflow from a configuration file.
    
    Args:
        args: Parsed command line arguments
        api_key: Lyzr API key
        logger: Logger instance
        
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        # Load the workflow configuration
        logger.info(f"Loading workflow from {args.workflow_file}")
        config = load_config(args.workflow_file)
        
        # This is a placeholder for more sophisticated workflow loading
        # In a real implementation, we'd parse the steps and create callables
        logger.error("Workflow execution from config files is not yet implemented")
        return 1
        
    except ConfigError as e:
        logger.error(f"Configuration error: {str(e)}")
        return 1
    except Exception as e:
        logger.error(f"Error running workflow: {str(e)}")
        return 1

def debug_agent_command(args: argparse.Namespace, api_key: Optional[str], logger: logging.Logger) -> int:
    """
    Debug an agent interaction by sending a message and showing the response.
    
    Args:
        args: Parsed command line arguments
        api_key: Lyzr API key
        logger: Logger instance
        
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        # Use agent ID as session ID if not provided
        session_id = args.session or args.agent
        
        logger.info(f"Sending debug message to agent {args.agent}")
        
        # Send the request to the agent
        response = send_agent_request(
            user_id=args.user,
            agent_id=args.agent,
            session_id=session_id,
            message=args.message,
            api_key=api_key
        )
        
        # Print the full response in debug mode
        logger.debug(f"Full response: {response}")
        
        # Print just the response text for normal output
        text_response = response.get("data", {}).get("response", "")
        print(f"Agent response:\n{text_response}")
        
        return 0
        
    except APIError as e:
        logger.error(f"API error: {str(e)}")
        return 1
    except Exception as e:
        logger.error(f"Error debugging agent: {str(e)}")
        return 1

def show_version_command() -> int:
    """
    Show version information.
    
    Returns:
        Exit code (always 0)
    """
    from .. import __version__
    print(f"LyzrBoost version {__version__}")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 