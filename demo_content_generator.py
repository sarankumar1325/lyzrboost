"""
LyzrBoost Demo: Content Generation Workflow

This demo showcases how LyzrBoost simplifies working with Lyzr agents by:
1. Creating a multi-agent workflow for content generation
2. Handling API calls and session management
3. Providing error handling and logging

The workflow consists of three steps:
1. Research: Gather information on a topic
2. Write: Create content based on the research
3. Edit: Polish and refine the content

Usage:
    python demo_content_generator.py "Artificial Intelligence"
"""

import os
import sys
import argparse
from lyzrboost.core.agent_api import get_agent_response
from lyzrboost.core.workflow import Workflow, WorkflowStep
from lyzrboost.utils.logger import setup_logger

# Configure logging
logger = setup_logger(name="content_generator_demo", level="INFO")

# Default agent IDs (replace with actual Lyzr agent IDs)
RESEARCH_AGENT_ID = "research_agent_id"  # Replace with actual agent ID
WRITING_AGENT_ID = "writing_agent_id"    # Replace with actual agent ID
EDITING_AGENT_ID = "editing_agent_id"    # Replace with actual agent ID

# Default user ID (replace with your user ID)
DEFAULT_USER_ID = "your_user_id"  # Replace with your user ID

def research_topic(topic):
    """
    Step 1: Research a topic using the research agent.
    
    Args:
        topic: The topic to research
        
    Returns:
        Dict containing the topic and research results
    """
    logger.info(f"Researching topic: {topic}")
    
    # Prepare the message for the research agent
    message = f"Provide key information, facts, and statistics about: {topic}"
    
    try:
        # Use LyzrBoost's simplified API to get a response from the research agent
        research_response = get_agent_response(
            user_id=DEFAULT_USER_ID,
            agent_id=RESEARCH_AGENT_ID,
            message=message,
            timeout=120  # 2 minutes timeout
        )
        
        logger.info("Research completed successfully")
        
        return {
            "topic": topic,
            "research": research_response
        }
        
    except Exception as e:
        logger.error(f"Research step failed: {str(e)}")
        raise

def write_content(data):
    """
    Step 2: Write content based on the research.
    
    Args:
        data: Dict containing the topic and research results
        
    Returns:
        Dict containing the topic, research, and draft content
    """
    topic = data["topic"]
    research = data["research"]
    
    logger.info(f"Writing content for: {topic}")
    
    # Prepare the message for the writing agent
    message = f"""
    Create a well-structured article about {topic} based on the following research:
    
    {research}
    
    The article should include an introduction, 3-4 main sections, and a conclusion.
    """
    
    try:
        # Get response from the writing agent
        content_response = get_agent_response(
            user_id=DEFAULT_USER_ID,
            agent_id=WRITING_AGENT_ID,
            message=message,
            timeout=180  # 3 minutes timeout
        )
        
        logger.info("Content writing completed successfully")
        
        # Add the draft content to the data
        data["draft_content"] = content_response
        return data
        
    except Exception as e:
        logger.error(f"Writing step failed: {str(e)}")
        raise

def edit_content(data):
    """
    Step 3: Edit and polish the content.
    
    Args:
        data: Dict containing the topic, research, and draft content
        
    Returns:
        Dict containing the topic, research, draft content, and final content
    """
    topic = data["topic"]
    draft_content = data["draft_content"]
    
    logger.info(f"Editing content for: {topic}")
    
    # Prepare the message for the editing agent
    message = f"""
    Please edit and improve the following article about {topic}:
    
    {draft_content}
    
    Focus on:
    - Improving clarity and flow
    - Fixing any grammatical or spelling errors
    - Enhancing the overall readability
    - Adding appropriate subheadings if needed
    """
    
    try:
        # Get response from the editing agent
        edited_response = get_agent_response(
            user_id=DEFAULT_USER_ID,
            agent_id=EDITING_AGENT_ID,
            message=message,
            timeout=120  # 2 minutes timeout
        )
        
        logger.info("Content editing completed successfully")
        
        # Add the final content to the data
        data["final_content"] = edited_response
        return data
        
    except Exception as e:
        logger.error(f"Editing step failed: {str(e)}")
        raise

def format_output(data):
    """
    Final step: Format the output for display.
    
    Args:
        data: Dict containing all workflow data
        
    Returns:
        Dict with formatted output
    """
    return {
        "topic": data["topic"],
        "final_content": data["final_content"],
        "metadata": {
            "research_length": len(data["research"]),
            "draft_length": len(data["draft_content"]),
            "final_length": len(data["final_content"])
        }
    }

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate content on a topic using LyzrBoost")
    parser.add_argument("topic", help="The topic to generate content about")
    parser.add_argument("--api-key", help="Lyzr API key (or set LYZR_API_KEY environment variable)")
    parser.add_argument("--user-id", help="User ID for Lyzr API", default=DEFAULT_USER_ID)
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Set API key from args or environment
    if args.api_key:
        os.environ["LYZR_API_KEY"] = args.api_key
    
    # Update user ID if provided
    if args.user_id:
        global DEFAULT_USER_ID
        DEFAULT_USER_ID = args.user_id
    
    # Set logging level based on verbosity
    if args.verbose:
        logger.setLevel("DEBUG")
    
    try:
        # Create the workflow with defined steps
        workflow = Workflow(
            steps=[
                WorkflowStep(research_topic, name="Research"),
                WorkflowStep(write_content, name="Write"),
                WorkflowStep(edit_content, name="Edit"),
                WorkflowStep(format_output, name="Format")
            ],
            name="ContentGenerationWorkflow",
            description="A workflow for researching, writing, and editing content on a topic."
        )
        
        # Run the workflow with the provided topic
        print(f"Starting content generation workflow for topic: {args.topic}")
        print("-" * 80)
        
        result = workflow.run(args.topic)
        
        # Print the result
        print("\nGenerated Content:")
        print("=" * 80)
        print(f"Topic: {result['topic']}")
        print("-" * 80)
        print(result["final_content"])
        print("-" * 80)
        print(f"Metadata: {result['metadata']}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Workflow failed: {str(e)}")
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
