"""
Example demonstrating a multi-agent workflow with LyzrBoost.

This workflow simulates using multiple agents for a content creation process:
1. A research agent to gather information on a topic
2. A writing agent to create content based on research
3. An editing agent to refine and polish the content
"""

import os
import sys
from lyzrboost.core.agent_api import get_agent_response
from lyzrboost.core.workflow import Workflow, WorkflowStep
from lyzrboost.utils.logger import setup_logger

# Configure logging
logger = setup_logger(level="INFO")

# Default parameters - replace with your actual agent IDs
USER_ID = "sarankumar131313@gmail.com"
STUDY_BUDDY_AGENT_ID = "67e56da36443c3d4ecfc5e2a"  # Using StudyBuddy for all steps in this demo
API_KEY = "sk-default-9wdTatnu1figlN2UilBoBW0yz58wNokO"

# Step 1: Research a topic
def research_topic(topic):
    """
    Research phase: Gather information about the topic.
    In a real scenario, this would use a specialized research agent.
    """
    logger.info(f"Step 1: Researching topic '{topic}'")
    
    message = (
        f"You are a research assistant. Research the topic '{topic}' "
        f"and provide key facts, statistics, and insights. "
        f"Format the research as bullet points with main categories."
    )
    
    research = get_agent_response(
        user_id=USER_ID,
        agent_id=STUDY_BUDDY_AGENT_ID,  # Using StudyBuddy as research agent
        message=message,
        api_key=API_KEY
    )
    
    return {
        "topic": topic,
        "research": research
    }

# Step 2: Write content based on research
def write_content(data):
    """
    Writing phase: Create content based on the research.
    In a real scenario, this would use a specialized writing agent.
    """
    topic = data["topic"]
    research = data["research"]
    
    logger.info(f"Step 2: Writing content for '{topic}'")
    
    message = (
        f"You are a content writer. Based on the following research about '{topic}', "
        f"write a comprehensive and engaging blog post (around 500 words).\n\n"
        f"Research:\n{research}"
    )
    
    content = get_agent_response(
        user_id=USER_ID,
        agent_id=STUDY_BUDDY_AGENT_ID,  # Using StudyBuddy as writing agent
        message=message,
        api_key=API_KEY
    )
    
    data["draft_content"] = content
    return data

# Step 3: Edit and refine the content
def edit_content(data):
    """
    Editing phase: Polish and improve the content.
    In a real scenario, this would use a specialized editing agent.
    """
    topic = data["topic"]
    draft = data["draft_content"]
    
    logger.info(f"Step 3: Editing content for '{topic}'")
    
    message = (
        f"You are an editor. Review and improve the following draft blog post about '{topic}'. "
        f"Fix any grammar issues, improve flow, and enhance clarity while keeping the main ideas intact.\n\n"
        f"Draft:\n{draft}"
    )
    
    edited_content = get_agent_response(
        user_id=USER_ID,
        agent_id=STUDY_BUDDY_AGENT_ID,  # Using StudyBuddy as editing agent
        message=message,
        api_key=API_KEY
    )
    
    data["final_content"] = edited_content
    return data

def main():
    """
    Run the multi-agent content creation workflow.
    """
    # Check for API key
    api_key = os.environ.get("LYZR_API_KEY") or API_KEY
    if not api_key:
        print("Error: API key not provided")
        print("Set LYZR_API_KEY environment variable or update the API_KEY in the script")
        return 1
    
    # Get topic from command line or use default
    topic = sys.argv[1] if len(sys.argv) > 1 else "Artificial Intelligence Ethics"
    
    try:
        print(f"Starting multi-agent content creation workflow for topic: {topic}")
        print("-" * 80)
        
        # Create the workflow with defined steps
        workflow = Workflow(
            steps=[
                WorkflowStep(research_topic, name="Research"),
                WorkflowStep(write_content, name="Write"),
                WorkflowStep(edit_content, name="Edit")
            ],
            name="ContentCreationWorkflow",
            description="A workflow for researching, writing, and editing content on a topic."
        )
        
        # Run the workflow
        result = workflow.run(topic)
        
        # Display the results
        print("\nFinal Content:")
        print("=" * 80)
        print(result["final_content"])
        print("=" * 80)
        
        # Show workflow metrics
        print("\nWorkflow Summary:")
        print(f"Topic: {result['topic']}")
        print(f"Research length: {len(result['research'])} characters")
        print(f"Draft length: {len(result['draft_content'])} characters")
        print(f"Final length: {len(result['final_content'])} characters")
        
        return 0
        
    except Exception as e:
        print(f"Workflow error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 