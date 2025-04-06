# LyzrBoost

LyzrBoost is a Python package designed to simplify the orchestration and debugging of Lyzr AI agents. It provides developers with a unified interface to interact with Lyzr agent APIs, manage multi-step workflows, and streamline the process of building generative AI applications.

## Features

- **Simplified Agent Integration**: Clean API to interact with Lyzr's agent inference endpoints
- **Workflow Orchestration**: Chain calls to different agents and manage sessions
- **Enhanced Developer Productivity**: CLI tools, logging, and debugging utilities
- **Easy Installation**: Simple pip installation with clear documentation

## Installation

```bash
pip install lyzrboost
```

## Quick Start

```python
from lyzrboost.core.agent_api import send_agent_request

# Initialize parameters
user_id = "your_user_id"
agent_id = "your_agent_id"
session_id = "session_123"
message = "Tell me about AI agents."

# Send a request to the Lyzr agent
response = send_agent_request(user_id, agent_id, session_id, message)
print(response)
```

## Workflow Example

```python
from lyzrboost.core.workflow import Workflow

def my_workflow(input_data):
    # Define your workflow steps here
    # This is a placeholder for a more complex workflow
    pass

# Create and run a workflow
workflow = Workflow(steps=[my_workflow])
result = workflow.run("Your input data")
```

## CLI Usage

```bash
# Run a workflow from a configuration file
lyzrboost run workflow.yaml

# Debug an agent interaction
lyzrboost debug --agent your_agent_id --message "Test message"
```

## License

MIT License

## Links

- [Documentation](https://github.com/lyzr-ai/lyzrboost)
- [PyPI](https://pypi.org/project/lyzrboost/)
- [Issue Tracker](https://github.com/lyzr-ai/lyzrboost/issues) 