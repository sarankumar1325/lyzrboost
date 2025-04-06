import os
from google import generativeai as genai

def generate_lyzrboost_plan():
    """Generate a plan for LyzrBoost package that enhances Lyzr with multi-agent capabilities."""
    
    # API key handling - use environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    genai.configure(api_key=api_key)
    
    # Create the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Define the prompt
    prompt = """
    Create a detailed plan for enhancing the Lyzr AI framework with a Python package called LyzrBoost
    that adds multi-agent collaboration capabilities. The package should:

    1. Simplify orchestration between multiple Lyzr agents
    2. Provide easy workflow creation (similar to Crew AI)
    3. Include debugging and monitoring tools
    4. Maintain compatibility with existing Lyzr functionality
    
    Outline the:
    - Key modules and their functions
    - Core classes and methods
    - Example usage (with code snippets)
    - Implementation approach
    - How this compares to Crew AI's approach

    Make it production-ready, addressing error handling, testing, and documentation.
    """
    
    # Generate content
    response = model.generate_content(prompt)
    
    # Print the response
    print("\n=========== LYZRBOOST PLANNING DOCUMENT ===========\n")
    print(response.text)
    print("\n====================================================\n")

if __name__ == "__main__":
    print("Generating comprehensive plan for LyzrBoost package to enhance Lyzr with multi-agent capabilities...")
    generate_lyzrboost_plan() 