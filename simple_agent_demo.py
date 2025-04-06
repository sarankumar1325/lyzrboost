"""
LyzrBoost Demo: Simple Agent Interaction

This demo shows how to use LyzrBoost to interact with a Lyzr agent in a simple way.
It demonstrates the basic API wrapper functionality and error handling.

Usage:
    python simple_agent_demo.py "What is artificial intelligence?"
"""

import os
import sys
import argparse
from lyzrboost.core.agent_api import get_agent_response, APIError
from lyzrboost.utils.logger import setup_logger

# Configure logging
logger = setup_logger(name="simple_agent_demo", level="INFO")

# Default values from LyzrStudyBuddy demo
DEFAULT_USER_ID = "sarankumar131313@gmail.com"  # Default user ID
DEFAULT_AGENT_ID = "67e56da36443c3d4ecfc5e2a"  # LyzrStudyBuddy agent ID
DEFAULT_API_KEY = "sk-default-9wdTatnu1figlN2UilBoBW0yz58wNokO"  # Default API key

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Interact with a Lyzr agent using LyzrBoost")
    parser.add_argument("message", help="The message to send to the agent")
    parser.add_argument("--api-key", help="Lyzr API key (or set LYZR_API_KEY environment variable)")
    parser.add_argument("--user-id", help="User ID for Lyzr API", default=DEFAULT_USER_ID)
    parser.add_argument("--agent-id", help="Agent ID to interact with", default=DEFAULT_AGENT_ID)
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Set API key from args, environment, or default
    if args.api_key:
        os.environ["LYZR_API_KEY"] = args.api_key
    else:
        # Use default API key if not provided
        os.environ["LYZR_API_KEY"] = DEFAULT_API_KEY

    # Set logging level based on verbosity
    if args.verbose:
        logger.setLevel("DEBUG")

    try:
        print(f"Sending message to agent {args.agent_id}...")
        print(f"Message: {args.message}")
        print("-" * 80)

        # Use LyzrBoost's simplified API to get a response
        response = get_agent_response(
            user_id=args.user_id,
            agent_id=args.agent_id,
            message=args.message,
            timeout=60  # 1 minute timeout
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

if __name__ == "__main__":
    sys.exit(main())
