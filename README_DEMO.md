# LyzrBoost Demos

This repository contains demo applications that showcase how to use LyzrBoost to interact with Lyzr AI agents and build multi-agent workflows.

## What is LyzrBoost?

LyzrBoost is a Python package designed to simplify the orchestration and debugging of Lyzr AI agents. It provides developers with a unified interface to interact with Lyzr agent APIs, manage multi-step workflows, and streamline the process of building generative AI applications.

## Features

- **Simplified Agent Integration**: Clean API to interact with Lyzr's agent inference endpoints
- **Workflow Orchestration**: Chain calls to different agents and manage sessions
- **Enhanced Developer Productivity**: CLI tools, logging, and debugging utilities
- **Easy Installation**: Simple pip installation with clear documentation

## Prerequisites

Before running the demos, make sure you have:

1. Python 3.7 or higher installed
2. A Lyzr account with API access
3. Agent IDs for the Lyzr agents you want to use

## Installation

### Option 1: Using the Setup Script

The easiest way to get started is to run the setup script, which will install all required dependencies and guide you through the setup process:

```bash
python setup_demo.py
```

### Option 2: Using requirements.txt

You can install the required packages using the provided requirements.txt file:

```bash
pip install -r requirements.txt
```

### Option 3: Manual Installation

Alternatively, you can install the required packages manually:

```bash
pip install lyzr lyzrboost pyyaml requests
```

### Setting Up Your API Key

You can provide your Lyzr API key in one of the following ways:

1. Set the `LYZR_API_KEY` environment variable:

   ```bash
   # On Windows
   set LYZR_API_KEY=your_api_key

   # On macOS/Linux
   export LYZR_API_KEY=your_api_key
   ```

2. Pass it as a command-line argument when running the demos:

   ```bash
   python simple_agent_demo.py "Your question" --api-key your_api_key
   ```

## Demo Applications

### 1. Simple Agent Demo

This demo shows how to use LyzrBoost to interact with a single Lyzr agent.

```bash
python simple_agent_demo.py "What is artificial intelligence?" --api-key YOUR_API_KEY --user-id YOUR_USER_ID --agent-id YOUR_AGENT_ID
```

### 2. Content Generation Workflow Demo

This demo showcases a multi-agent workflow for content generation, demonstrating how LyzrBoost simplifies orchestrating multiple agent calls.

```bash
python demo_content_generator.py "Artificial Intelligence" --api-key YOUR_API_KEY --user-id YOUR_USER_ID
```

### 3. Configuration-Driven Workflow Demo

This demo shows how to define workflows using YAML configuration files, allowing for more flexible and maintainable workflows without changing code.

```bash
python config_workflow_demo.py workflow_config.yaml --input "Artificial Intelligence" --api-key YOUR_API_KEY --user-id YOUR_USER_ID
```

### 4. CLI Demo

This demo showcases how to build a command-line interface using LyzrBoost, providing commands for interacting with Lyzr agents and running workflows.

```bash
# Chat with an agent
python lyzrboost_cli_demo.py chat --agent YOUR_AGENT_ID --message "What is AI?" --api-key YOUR_API_KEY --user-id YOUR_USER_ID

# Run a workflow from a configuration file
python lyzrboost_cli_demo.py run --config workflow_config.yaml --input "Artificial Intelligence" --api-key YOUR_API_KEY --user-id YOUR_USER_ID

# Debug an agent interaction with detailed logging
python lyzrboost_cli_demo.py debug --agent YOUR_AGENT_ID --message "Test message" --api-key YOUR_API_KEY --user-id YOUR_USER_ID
```

### 5. ChatBot Integration Demo

This demo shows how to use LyzrBoost to enhance the Lyzr ChatBot module, creating a simple chatbot that can answer questions about a PDF document.

```bash
# Ask a question about a PDF document
python chatbot_demo.py path/to/document.pdf "What is this document about?" --api-key YOUR_API_KEY

# Generate a summary of the document
python chatbot_demo.py path/to/document.pdf --summarize --api-key YOUR_API_KEY

# Extract key points from the document
python chatbot_demo.py path/to/document.pdf --key-points --api-key YOUR_API_KEY
```

## Customizing the Demos

To use these demos with your own Lyzr agents:

1. Replace the placeholder agent IDs in the scripts with your actual agent IDs
2. Update the user ID to your Lyzr user ID
3. Provide your API key either as a command-line argument or by setting the `LYZR_API_KEY` environment variable

## Key Components

### Agent API

LyzrBoost provides a simplified API for interacting with Lyzr agents:

```python
from lyzrboost.core.agent_api import get_agent_response

response = get_agent_response(
    user_id="your_user_id",
    agent_id="your_agent_id",
    message="Your message to the agent",
    api_key="your_api_key"  # Optional if set in environment
)
```

### Workflow Orchestration

LyzrBoost makes it easy to chain multiple agent calls into a workflow:

```python
from lyzrboost.core.workflow import Workflow, WorkflowStep

# Define workflow steps as functions
def step1(input_data):
    # Process input and call an agent
    return result

def step2(input_from_step1):
    # Process input from step1 and call another agent
    return result

# Create and run a workflow
workflow = Workflow(
    steps=[
        WorkflowStep(step1, name="Step1"),
        WorkflowStep(step2, name="Step2")
    ],
    name="MyWorkflow"
)

result = workflow.run(initial_input)
```

## Error Handling

LyzrBoost provides robust error handling for API calls:

```python
from lyzrboost.core.agent_api import get_agent_response, APIError

try:
    response = get_agent_response(...)
except APIError as e:
    print(f"API Error: {str(e)}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

## Logging

LyzrBoost includes a configurable logging system:

```python
from lyzrboost.utils.logger import setup_logger

# Configure logging
logger = setup_logger(name="my_app", level="DEBUG")

# Use the logger
logger.info("Starting workflow")
logger.debug("Detailed debug information")
logger.error("An error occurred")
```

## Configuration-Driven Workflows

LyzrBoost supports defining workflows using YAML configuration files:

```yaml
# Sample workflow configuration
name: "Content Generation Workflow"
description: "A workflow that generates content on a given topic"

# Define the workflow steps
steps:
  - name: "Research"
    agent_id: "research_agent_id"
    prompt_template: "Provide key information about: {input}"
    output_key: "research"

  - name: "Write"
    agent_id: "writing_agent_id"
    prompt_template: "Create an article about {input} based on: {research}"
    output_key: "content"

# Output configuration
output_format: "final_only"
final_output_key: "content"
```

## CLI Integration

LyzrBoost can be used to build command-line interfaces for interacting with Lyzr agents:

```python
from lyzrboost.utils.logger import setup_logger
from lyzrboost.core.agent_api import get_agent_response

# Configure logging
logger = setup_logger(name="my_cli", level="INFO")

# Define CLI commands
def chat_command(args):
    response = get_agent_response(
        user_id=args.user_id,
        agent_id=args.agent,
        message=args.message
    )
    print(response)
```

## Next Steps

After exploring these demos, you can:

1. Build your own workflows using LyzrBoost
2. Integrate LyzrBoost into your existing applications
3. Create custom CLI tools for your team
4. Develop configuration-driven workflows for specific use cases

## Resources

- [LyzrBoost Documentation](https://github.com/lyzr-ai/lyzrboost)
- [Lyzr Documentation](https://docs.lyzr.ai/)
- [Lyzr Website](https://www.lyzr.ai/)
