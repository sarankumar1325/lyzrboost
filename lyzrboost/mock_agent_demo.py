import os
import sys
import logging
from google.api_core import exceptions as google_exceptions

# Try importing google.generativeai, handle if not installed
try:
    import google.generativeai as genai
    from google.generativeai import types
except ImportError:
    print("ERROR: google.generativeai package not found.")
    print("Please install it: pip install google-generativeai")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Security Warning --- 
# NEVER hardcode API keys directly in code.
# Use environment variables.
# Example: export GEMINI_API_KEY='YOUR_API_KEY'
# Or on Windows: set GEMINI_API_KEY=YOUR_API_KEY
# ------------------------

def generate_response(input_text: str):
    """Generates a response using Google Gemini based on input text."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY environment variable not set.")
        print("Error: GEMINI_API_KEY not set. Cannot contact Gemini.")
        return # Return None or raise an error if preferred

    try:
        genai.configure(api_key=api_key)
        
        # Model selection (using flash for speed/cost)
        model = genai.GenerativeModel('gemini-1.5-flash-latest') # Using 1.5 flash

        # Generate content
        # Note: Simple text generation, not a chat session for this mock
        response = model.generate_content(input_text)
        
        # Accessing the text part safely
        if response.parts:
            generated_text = "".join(part.text for part in response.parts)
            print(generated_text) # Print the response directly to stdout
        else:
            # Handle cases where response might be blocked or empty
            logger.warning("Gemini response was empty or blocked.")
            if hasattr(response, 'prompt_feedback'):
                logger.warning(f"Prompt Feedback: {response.prompt_feedback}")
            print("(Gemini returned no content)")

    except google_exceptions.PermissionDenied as e:
        logger.error(f"Gemini API Key Error: {e}")
        print(f"Error: Invalid or insufficient permissions for Gemini API Key.")
    except google_exceptions.ResourceExhausted as e:
        logger.error(f"Gemini Quota Error: {e}")
        print(f"Error: Gemini API quota exceeded. Please check your usage limits.")
    except Exception as e:
        logger.error(f"An unexpected error occurred during Gemini generation: {e}", exc_info=True)
        print(f"Error: An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_query = " ".join(sys.argv[1:])
        logger.info(f"Received query: {input_query}")
        generate_response(input_query)
    else:
        print("Usage: python mock_agent_demo.py <your input text>")
        logger.warning("No input text provided to mock agent.") 