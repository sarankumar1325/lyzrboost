"""
Simple example demonstrating how to use LyzrBoost to call a Lyzr agent.
"""

import os
import sys
from lyzrboost.core.agent_api import get_agent_response, APIError

def main():
    """Run a simple agent call example."""
    # Check for API key
    api_key = os.environ.get("LYZR_API_KEY")
    if not api_key:
        print("Error: LYZR_API_KEY environment variable not set")
        print("Please set your API key: export LYZR_API_KEY=your_api_key")
        return 1
        
    # Set up agent parameters
    user_id = "example@lyzr.ai"  # Replace with your user ID
    agent_id = "your_agent_id"   # Replace with your agent ID
    message = "Tell me about AI agents and how they can be used."
    
    print(f"Sending request to agent {agent_id}...")
    
    try:
        # Send request and get response
        response = get_agent_response(
            user_id=user_id,
            agent_id=agent_id,
            message=message,
            api_key=api_key
        )
        
        # Print the response
        print("\nAgent response:")
        print("--------------")
        print(response)
        
        return 0
        
    except APIError as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 