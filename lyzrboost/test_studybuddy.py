"""
Test script for LyzrBoost using the LyzrStudyBuddy agent.
"""

import os
import json
from lyzrboost.core.agent_api import send_agent_request, get_agent_response, APIError
from lyzrboost.utils.logger import setup_logger

# Configure logging
logger = setup_logger(level="DEBUG")

# Agent parameters
USER_ID = "sarankumar131313@gmail.com"
AGENT_ID = "67e56da36443c3d4ecfc5e2a"
SESSION_ID = AGENT_ID  # Using the agent_id as the session_id
API_KEY = "sk-default-9wdTatnu1figlN2UilBoBW0yz58wNokO"

def test_study_buddy():
    """Test basic interaction with the LyzrStudyBuddy agent."""
    message = "Explain Transformer architecture for NLP in simple terms."
    
    print(f"\nSending request to LyzrStudyBuddy agent...")
    print(f"Message: '{message}'")
    
    try:
        # Use our LyzrBoost package to call the agent with a shorter timeout
        response = send_agent_request(
            user_id=USER_ID,
            agent_id=AGENT_ID,
            session_id=SESSION_ID,
            message=message,
            api_key=API_KEY,
            timeout=30  # Shorter timeout
        )
        
        # Print the full response for debugging
        print("\nFull Response:")
        print(json.dumps(response, indent=2))
        
        # Extract and print just the text response
        if "data" in response and "response" in response["data"]:
            text_response = response["data"]["response"]
            print("\nAgent Response:")
            print("-" * 80)
            print(text_response)
            print("-" * 80)
        else:
            print("\nUnexpected response format. See full response above.")
            
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nAPI TEST FAILED - This could be due to:")
        print("1. Network connectivity issues")
        print("2. Invalid API credentials")
        print("3. Endpoint timeout (try increasing the timeout parameter)")
        print("4. The API endpoint may be temporarily unavailable")
        return False

def test_flashcard_generation():
    """Test flashcard generation with the LyzrStudyBuddy agent."""
    message = "Create flashcards about Python decorators."
    
    print(f"\nRequesting flashcards about Python decorators...")
    
    try:
        # Use the simplified wrapper for just the text response
        response = get_agent_response(
            user_id=USER_ID,
            agent_id=AGENT_ID,
            session_id=SESSION_ID,
            message=message,
            api_key=API_KEY
        )
        
        print("\nFlashcards Generated:")
        print("-" * 80)
        print(response)
        print("-" * 80)
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_cli_version():
    """Test the CLI version command."""
    try:
        # We can't directly call the CLI, but we can import the function
        from lyzrboost.cli.main import show_version_command
        
        print("\nTesting CLI version command...")
        show_version_command()
        return True
        
    except Exception as e:
        print(f"Error with CLI version command: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing LyzrBoost with LyzrStudyBuddy agent...")
    
    # Save the API key as an environment variable too
    os.environ["LYZR_API_KEY"] = API_KEY
    
    # Run tests
    api_test_result = test_study_buddy()
    cli_test_result = test_cli_version()
    
    # Print summary
    print("\nTest Summary:")
    print(f"API Test: {'PASSED' if api_test_result else 'FAILED'}")
    print(f"CLI Test: {'PASSED' if cli_test_result else 'FAILED'}")
    
    if api_test_result and cli_test_result:
        print("\nAll tests PASSED! The package appears to be working correctly.")
    else:
        print("\nSome tests FAILED. Please check the errors above.")
        
    print("\nFor further testing, try the Streamlit demo app:")
    print("streamlit run demo_app.py") 