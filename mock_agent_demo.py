"""
LyzrBoost Demo: Gemini API Agent Workflow

This demo shows how to use LyzrBoost's workflow orchestration capabilities
with Google's Gemini API to generate content.

Usage:
    python mock_agent_demo.py "Artificial Intelligence"
    python mock_agent_demo.py -i  # Interactive mode
"""

import sys
import argparse
import time
import os
from typing import Dict, Any, List

# Import Google Gemini API modules
try:
    import google.generativeai as genai
except ImportError:
    print("Error: Google Generative AI package not found.")
    print("Please install it using: pip install -U google-generativeai")
    sys.exit(1)

# Import LyzrBoost workflow module and agent manager
try:
    from lyzrboost.core.workflow import Workflow, WorkflowStep
    from lyzrboost.core.agent_manager import AgentManager
except ImportError:
    # If LyzrBoost is not installed, create simple mock classes
    print("Note: Using mock workflow classes as LyzrBoost is not properly installed.")

    class WorkflowStep:
        def __init__(self, func, name=None, condition=None):
            self.func = func
            self.name = name or func.__name__
            self.condition = condition

        def should_execute(self, data):
            if self.condition is None:
                return True
            return self.condition(data)

        def execute(self, data):
            return self.func(data)

    class Workflow:
        def __init__(self, steps, name="workflow", description=None):
            self.steps = []
            for step in steps:
                if callable(step):
                    self.steps.append(WorkflowStep(step))
                else:
                    self.steps.append(step)
            self.name = name
            self.description = description

        def run(self, initial_input):
            print(f"Starting workflow: {self.name}")
            current_data = initial_input

            for step in self.steps:
                if step.should_execute(current_data):
                    print(f"Executing step: {step.name}")
                    current_data = step.execute(current_data)
                else:
                    print(f"Skipping step: {step.name}")

            return current_data

    class AgentManager:
        def __init__(self, api_key=None, default_endpoint=None):
            self.api_key = api_key
            self.default_endpoint = default_endpoint
            self._sessions = {}
            
        def generate_session_id(self, agent_id=None, prefix=""):
            import uuid
            session_id = f"{prefix}{uuid.uuid4().hex}"
            self._sessions[session_id] = {
                "created_at": None,
                "last_access": None,
                "agent_id": agent_id,
                "history": []
            }
            return session_id
            
        def store_interaction(self, session_id, user_message, agent_response, metadata=None):
            if session_id not in self._sessions:
                raise KeyError(f"Session {session_id} not found")
                
            interaction = {
                "user_message": user_message,
                "agent_response": agent_response,
                "timestamp": None,
                "metadata": metadata or {}
            }
            
            self._sessions[session_id]["history"].append(interaction)

# Set up the Gemini API client
def setup_gemini_client():
    """
    Set up and return the Gemini API client.
    """
    # Use environment variable for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    # Configure the Gemini API client
    genai.configure(api_key=api_key)
    
    return genai

# Agent functions using Gemini API
def gemini_research_agent(topic: str) -> str:
    """
    Use Gemini API to research a topic.

    Args:
        topic: The topic to research

    Returns:
        Research information about the topic
    """
    print("Gemini research agent processing...")
    setup_gemini_client()
    
    prompt = f"""
    Provide a concise research summary about {topic}. Include:
    - Key definitions and concepts
    - Historical context and development
    - Main applications and use cases
    - Current state and trends
    - Challenges and limitations
    
    Format the response with bullet points for key information.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating research content: {str(e)}")
        return f"Research about {topic} could not be generated due to an error."

def gemini_writing_agent(topic: str, research: str) -> str:
    """
    Use Gemini API to write content based on research.

    Args:
        topic: The topic to write about
        research: Research information about the topic

    Returns:
        Written content about the topic
    """
    print("Gemini writing agent processing...")
    setup_gemini_client()
    
    prompt = f"""
    Write a comprehensive article about {topic} based on the following research:
    
    {research}
    
    The article should include:
    - An engaging introduction explaining the importance of {topic}
    - Clear sections with headings covering different aspects
    - Technical explanations that are accessible to a general audience
    - Real-world examples and applications
    - A thoughtful conclusion
    
    Use markdown formatting with # for main headings and ## for subheadings.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating written content: {str(e)}")
        return f"Article about {topic} could not be generated due to an error."

def gemini_editing_agent(topic: str, content: str) -> str:
    """
    Use Gemini API to edit and polish content.

    Args:
        topic: The topic of the content
        content: The content to edit

    Returns:
        Edited and improved content
    """
    print("Gemini editing agent processing...")
    setup_gemini_client()
    
    prompt = f"""
    Edit and improve the following article about {topic}:
    
    {content}
    
    Your edits should:
    - Improve clarity and flow
    - Enhance structure and organization
    - Add depth to important sections
    - Fix any grammar or style issues
    - Ensure technical accuracy
    - Maintain the original markdown formatting
    
    Return the complete edited article.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error editing content: {str(e)}")
        return content  # Return the original content if editing fails

# Workflow steps
def research_topic(topic: str) -> Dict[str, Any]:
    """
    Step 1: Research a topic using Gemini API.

    Args:
        topic: The topic to research

    Returns:
        Dict containing the topic and research results
    """
    print(f"\nResearching topic: {topic}")
    print("-" * 40)

    # Call the Gemini research agent
    research_response = gemini_research_agent(topic)

    print("Research completed successfully")

    return {
        "topic": topic,
        "research": research_response
    }

def write_content(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Step 2: Write content based on the research using Gemini API.

    Args:
        data: Dict containing the topic and research results

    Returns:
        Dict containing the topic, research, and draft content
    """
    topic = data["topic"]
    research = data["research"]

    print(f"\nWriting content for: {topic}")
    print("-" * 40)

    # Call the Gemini writing agent
    content_response = gemini_writing_agent(topic, research)

    print("Content writing completed successfully")

    # Add the draft content to the data
    data["draft_content"] = content_response
    return data

def edit_content(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Step 3: Edit and polish the content using Gemini API.

    Args:
        data: Dict containing the topic, research, and draft content

    Returns:
        Dict containing the topic, research, draft content, and final content
    """
    topic = data["topic"]
    draft_content = data["draft_content"]

    print(f"\nEditing content for: {topic}")
    print("-" * 40)

    # Call the Gemini editing agent
    edited_response = gemini_editing_agent(topic, draft_content)

    print("Content editing completed successfully")

    # Add the final content to the data
    data["final_content"] = edited_response
    return data

def format_output(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Final step: Format the output for display.

    Args:
        data: Dict containing all workflow data

    Returns:
        Dict with formatted output
    """
    print("\nFormatting output...")
    print("-" * 40)

    return {
        "topic": data["topic"],
        "final_content": data["final_content"],
        "metadata": {
            "research_length": len(data["research"]),
            "draft_length": len(data["draft_content"]),
            "final_length": len(data["final_content"]),
            "generated_with": "Google Gemini API + LyzrBoost"
        }
    }

def interactive_mode():
    """
    Run the program in interactive mode, allowing the user to input questions.
    """
    print("\nEntering interactive mode with Gemini API")
    print("Type 'exit' to quit\n")
    
    setup_gemini_client()
    agent_manager = AgentManager()
    session_id = agent_manager.generate_session_id(prefix="gemini_")
    
    # Create a model for generating responses
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    while True:
        # Get user input
        user_query = input("\nEnter your question: ")
        
        # Check if user wants to exit
        if user_query.lower() in ['exit', 'quit', 'q']:
            print("Exiting interactive mode")
            break
        
        print("Processing your question...")
        
        try:
            # Generate response
            print("\nResponse:")
            print("-" * 40)
            
            response = model.generate_content(user_query)
            print(response.text)
            
            print("-" * 40)
            
            # Store the interaction in the agent manager (for history)
            agent_manager.store_interaction(
                session_id=session_id,
                user_message=user_query,
                agent_response=response.text
            )
            
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate content on a topic using Gemini API")
    parser.add_argument("topic", nargs="?", help="The topic to generate content about")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed output")
    parser.add_argument("-i", "--interactive", action="store_true", help="Run in interactive mode")

    args = parser.parse_args()

    print("Using Gemini API with model: gemini-2.0-flash")

    try:
        # Check if running in interactive mode
        if args.interactive:
            interactive_mode()
            return 0
            
        # Check if a topic was provided
        if not args.topic:
            print("Error: Please provide a topic or use the --interactive flag")
            parser.print_help()
            return 1
            
        # Create the workflow with defined steps
        workflow = Workflow(
            steps=[
                WorkflowStep(research_topic, name="Research"),
                WorkflowStep(write_content, name="Write"),
                WorkflowStep(edit_content, name="Edit"),
                WorkflowStep(format_output, name="Format")
            ],
            name="GeminiContentGenerationWorkflow",
            description="A workflow for researching, writing, and editing content on a topic using Gemini API."
        )

        # Run the workflow with the provided topic
        print(f"Starting content generation workflow for topic: {args.topic}")
        print("=" * 80)

        result = workflow.run(args.topic)

        # Print the result
        print("\nGenerated Content:")
        print("=" * 80)
        print(f"Topic: {result['topic']}")
        print("-" * 80)

        # Always show at least the first part of the content
        if args.verbose:
            # Show the full content
            print(result["final_content"])
        else:
            # Show just the first 300 characters
            content_preview = result["final_content"][:300] + "..." if len(result["final_content"]) > 300 else result["final_content"]
            print(content_preview)
            print("\n(Use --verbose to see the full content)")

        print("-" * 80)
        print(f"Metadata: {result['metadata']}")

        return 0

    except Exception as e:
        print(f"Workflow failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
