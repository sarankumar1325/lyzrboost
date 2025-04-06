import os
from google import genai
from google.genai import types

def generate():
    # Get API key from environment or use provided key
    api_key = os.environ.get("GEMINI_API_KEY") or "AIzaSyAA1heyOQ8a2yAwXuOWjGCVLCbpHy5iPYE"
    
    client = genai.Client(
        api_key=api_key,
    )

    model = "gemini-1.5-flash"  # Use 1.5 Flash for faster response
    
    # Define prompt
    prompt = """
    Create a detailed plan for enhancing the Lyzr AI framework with a Python package called LyzrBoost
    that adds multi-agent collaboration capabilities. The package should:

    1. Simplify orchestration between multiple Lyzr agents (similar to Crew AI)
    2. Provide easy workflow creation with minimal code
    3. Include debugging and monitoring tools
    4. Maintain compatibility with existing Lyzr functionality
    
    Outline the:
    - Key modules and their functions
    - Core classes and methods
    - Example usage (with code snippets showing how developers would use it)
    - Implementation approach 
    - How this provides advantages over using Lyzr alone
    
    Make it production-ready, addressing error handling, testing, and documentation.
    """
    
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    print("\n=========== LYZRBOOST PLANNING DOCUMENT ===========\n")
    
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")
    
    print("\n\n====================================================\n")

if __name__ == "__main__":
    print("Generating comprehensive plan for LyzrBoost package to enhance Lyzr with multi-agent capabilities...")
    generate() 