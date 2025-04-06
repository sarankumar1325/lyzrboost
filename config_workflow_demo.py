"""
LyzrBoost Demo: Configuration-Driven Workflow

This demo shows how to use LyzrBoost to define and run workflows using YAML configuration files.
This approach allows for more flexible and maintainable workflows without changing code.

Usage:
    python config_workflow_demo.py workflow_config.yaml
"""

import os
import sys
import argparse
import yaml
from typing import Dict, Any

from lyzrboost.core.agent_api import get_agent_response, APIError
from lyzrboost.core.workflow import Workflow, WorkflowStep
from lyzrboost.utils.logger import setup_logger
from lyzrboost.utils.config import load_config, merge_configs

# Configure logging
logger = setup_logger(name="config_workflow_demo", level="INFO")

# Default user ID (replace with your user ID)
DEFAULT_USER_ID = "your_user_id"  # Replace with your user ID

def load_workflow_config(config_path: str) -> Dict[str, Any]:
    """
    Load workflow configuration from a YAML file.
    
    Args:
        config_path: Path to the YAML configuration file
        
    Returns:
        Dict containing the workflow configuration
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            
        logger.info(f"Loaded workflow configuration from {config_path}")
        return config
        
    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        raise

def create_agent_step(step_config: Dict[str, Any]):
    """
    Create a workflow step function based on step configuration.
    
    Args:
        step_config: Configuration for the step
        
    Returns:
        A function that can be used as a workflow step
    """
    agent_id = step_config.get("agent_id")
    prompt_template = step_config.get("prompt_template")
    timeout = step_config.get("timeout", 60)
    
    def step_function(input_data):
        """
        Workflow step function that calls a Lyzr agent.
        
        Args:
            input_data: Input data for the step
            
        Returns:
            Dict containing the step results
        """
        # Extract variables from input_data to use in the prompt template
        if isinstance(input_data, dict):
            # Format the prompt template with variables from input_data
            try:
                message = prompt_template.format(**input_data)
            except KeyError as e:
                logger.error(f"Missing variable in prompt template: {str(e)}")
                raise
        else:
            # If input_data is not a dict, use it directly in the template
            message = prompt_template.format(input=input_data)
            
        logger.info(f"Calling agent {agent_id}")
        logger.debug(f"Message: {message}")
        
        try:
            # Call the Lyzr agent
            response = get_agent_response(
                user_id=DEFAULT_USER_ID,
                agent_id=agent_id,
                message=message,
                timeout=timeout
            )
            
            # Create result dict
            if isinstance(input_data, dict):
                # Merge input data with response
                result = input_data.copy()
                result[step_config.get("output_key", "response")] = response
                return result
            else:
                # Create a new dict with the response
                return {
                    "input": input_data,
                    step_config.get("output_key", "response"): response
                }
                
        except APIError as e:
            logger.error(f"API Error in step: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in step: {str(e)}")
            raise
            
    return step_function

def build_workflow_from_config(config: Dict[str, Any]) -> Workflow:
    """
    Build a workflow from configuration.
    
    Args:
        config: Workflow configuration
        
    Returns:
        Configured Workflow object
    """
    workflow_name = config.get("name", "ConfigWorkflow")
    workflow_description = config.get("description", "")
    steps_config = config.get("steps", [])
    
    # Create workflow steps
    steps = []
    for step_config in steps_config:
        step_name = step_config.get("name", f"Step{len(steps)+1}")
        step_function = create_agent_step(step_config)
        steps.append(WorkflowStep(step_function, name=step_name))
        
    # Create the workflow
    workflow = Workflow(
        steps=steps,
        name=workflow_name,
        description=workflow_description
    )
    
    logger.info(f"Built workflow '{workflow_name}' with {len(steps)} steps")
    return workflow

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run a workflow from a YAML configuration file")
    parser.add_argument("config", help="Path to workflow configuration YAML file")
    parser.add_argument("--input", help="Input for the workflow", default="")
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
        # Load workflow configuration
        config = load_workflow_config(args.config)
        
        # Build workflow from configuration
        workflow = build_workflow_from_config(config)
        
        # Get workflow input
        workflow_input = args.input
        
        # Run the workflow
        print(f"Starting workflow: {workflow.name}")
        print(f"Description: {workflow.description}")
        print("-" * 80)
        
        result = workflow.run(workflow_input)
        
        # Print the result
        print("\nWorkflow Result:")
        print("=" * 80)
        
        # Format the output based on the configuration
        output_format = config.get("output_format", "default")
        
        if output_format == "default":
            # Print the entire result dictionary
            for key, value in result.items():
                if isinstance(value, str) and len(value) > 100:
                    # Truncate long strings for display
                    print(f"{key}: {value[:100]}...")
                else:
                    print(f"{key}: {value}")
        elif output_format == "final_only":
            # Print only the final output
            final_key = config.get("final_output_key", "response")
            if final_key in result:
                print(result[final_key])
            else:
                print(f"Final output key '{final_key}' not found in result")
        else:
            # Default to printing the entire result
            print(result)
            
        return 0
        
    except Exception as e:
        logger.error(f"Workflow failed: {str(e)}")
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
