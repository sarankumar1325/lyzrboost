"""
Module for defining and executing workflows with Lyzr agents.
"""

import logging
from typing import List, Callable, Dict, Any, Optional, Union

# Configure logging
logger = logging.getLogger(__name__)

class WorkflowStep:
    """
    Represents a single step in a workflow.
    
    A workflow step is a callable function that takes an input and returns an output.
    It can also have pre-conditions and post-processing logic.
    """
    
    def __init__(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
        condition: Optional[Callable[[Any], bool]] = None
    ):
        """
        Initialize a workflow step.
        
        Args:
            func: The function to execute in this step
            name: Optional name for the step (defaults to function name)
            description: Optional description of the step
            condition: Optional function that determines if this step should execute
        """
        self.func = func
        self.name = name or func.__name__
        self.description = description
        self.condition = condition
        
    def should_execute(self, input_data: Any) -> bool:
        """
        Determine if this step should be executed based on its condition.
        
        Args:
            input_data: The input data to check against the condition
            
        Returns:
            True if the step should execute, False otherwise
        """
        if self.condition is None:
            return True
        return self.condition(input_data)
        
    def execute(self, input_data: Any) -> Any:
        """
        Execute this workflow step.
        
        Args:
            input_data: The input data for this step
            
        Returns:
            The result of executing the step function
        """
        logger.debug(f"Executing workflow step: {self.name}")
        return self.func(input_data)

class Workflow:
    """
    Defines a sequence of steps to be executed in order.
    
    A workflow consists of multiple steps, where the output of one step becomes
    the input to the next step.
    """
    
    def __init__(
        self,
        steps: List[Union[Callable, WorkflowStep]],
        name: str = "workflow",
        description: Optional[str] = None
    ):
        """
        Initialize a workflow.
        
        Args:
            steps: List of functions or WorkflowStep objects to execute
            name: Name of the workflow
            description: Optional description of the workflow
        """
        self.name = name
        self.description = description
        
        # Convert any function steps to WorkflowStep objects
        self.steps = []
        for step in steps:
            if isinstance(step, WorkflowStep):
                self.steps.append(step)
            elif callable(step):
                self.steps.append(WorkflowStep(step))
            else:
                raise TypeError(f"Step must be callable or WorkflowStep, got {type(step)}")
                
        logger.debug(f"Initialized workflow '{name}' with {len(self.steps)} steps")
    
    def run(self, initial_input: Any) -> Any:
        """
        Run the entire workflow.
        
        Args:
            initial_input: The initial input to the first step of the workflow
            
        Returns:
            The output from the final step in the workflow
        """
        logger.info(f"Starting workflow: {self.name}")
        
        current_data = initial_input
        
        for step in self.steps:
            if step.should_execute(current_data):
                try:
                    current_data = step.execute(current_data)
                    logger.debug(f"Step '{step.name}' completed successfully")
                except Exception as e:
                    logger.error(f"Error in workflow step '{step.name}': {str(e)}")
                    raise
            else:
                logger.debug(f"Skipping step '{step.name}' (condition not met)")
                
        logger.info(f"Workflow '{self.name}' completed")
        return current_data

def create_workflow_from_config(config: Dict[str, Any]) -> Workflow:
    """
    Create a workflow from a configuration dictionary.
    
    This is a placeholder for a more sophisticated workflow builder
    that would allow defining workflows from JSON/YAML configurations.
    
    Args:
        config: A dictionary containing workflow configuration
        
    Returns:
        A Workflow object
        
    Raises:
        ValueError: If the configuration is invalid
    """
    # This is a basic implementation - would need to be expanded
    # to support more complex workflow definitions
    
    if "steps" not in config:
        raise ValueError("Workflow configuration must contain 'steps' key")
        
    # This is a placeholder - in a real implementation, we'd parse the
    # step definitions and create actual callable steps
    
    name = config.get("name", "workflow")
    description = config.get("description")
    
    return Workflow([], name=name, description=description) 