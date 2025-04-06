"""
Example demonstrating how to create and run a simple workflow with LyzrBoost.
"""

import os
import sys
from lyzrboost.core.agent_api import get_agent_response, APIError
from lyzrboost.core.workflow import Workflow, WorkflowStep

# Check for API key at module level
API_KEY = os.environ.get("LYZR_API_KEY")

def research_topic(topic):
    """
    Step 1: Research a given topic using a research agent.
    """
    user_id = "example@lyzr.ai"  # Replace with your user ID
    agent_id = "research_agent_id"  # Replace with your research agent ID
    message = f"Research the following topic and provide key points: {topic}"
    
    print(f"Step 1: Researching topic '{topic}'...")
    
    try:
        response = get_agent_response(
            user_id=user_id,
            agent_id=agent_id,
            message=message,
            api_key=API_KEY
        )
        
        # Return research results for the next step
        return {
            "topic": topic,
            "research": response
        }
        
    except APIError as e:
        print(f"Error in research step: {str(e)}")
        raise

def generate_summary(data):
    """
    Step 2: Generate a summary based on the research.
    """
    user_id = "example@lyzr.ai"  # Replace with your user ID
    agent_id = "summary_agent_id"  # Replace with your summarization agent ID
    
    topic = data.get("topic", "")
    research = data.get("research", "")
    
    message = f"Create a concise summary of this research on {topic}: {research}"
    
    print(f"Step 2: Generating summary for '{topic}'...")
    
    try:
        response = get_agent_response(
            user_id=user_id,
            agent_id=agent_id,
            message=message,
            api_key=API_KEY
        )
        
        # Update data with the summary
        data["summary"] = response
        return data
        
    except APIError as e:
        print(f"Error in summary step: {str(e)}")
        raise

def format_output(data):
    """
    Step 3: Format the final output.
    """
    print(f"Step 3: Formatting output...")
    
    topic = data.get("topic", "")
    summary = data.get("summary", "")
    
    # Format the output as a dictionary
    return {
        "topic": topic,
        "summary": summary,
        "timestamp": None  # Placeholder for timestamp
    }

def main():
    """Run the simple workflow example."""
    # Check for API key
    if not API_KEY:
        print("Error: LYZR_API_KEY environment variable not set")
        print("Please set your API key: export LYZR_API_KEY=your_api_key")
        return 1
        
    # Get the topic from command line or use a default
    topic = sys.argv[1] if len(sys.argv) > 1 else "artificial intelligence"
    
    try:
        # Create the workflow
        workflow = Workflow(
            steps=[
                WorkflowStep(research_topic, name="Research"),
                WorkflowStep(generate_summary, name="Summarize"),
                WorkflowStep(format_output, name="Format")
            ],
            name="ResearchSummaryWorkflow",
            description="A workflow that researches a topic and generates a summary."
        )
        
        # Run the workflow
        print(f"Starting workflow for topic: {topic}")
        result = workflow.run(topic)
        
        # Print the result
        print("\nWorkflow Result:")
        print("----------------")
        print(f"Topic: {result['topic']}")
        print(f"Summary: {result['summary']}")
        
        return 0
        
    except Exception as e:
        print(f"Workflow error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 