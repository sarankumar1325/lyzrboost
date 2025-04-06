# Testing LyzrBoost

This document provides instructions for testing the LyzrBoost package before publishing to PyPI.

## Prerequisites

Before testing, ensure you have:

1. Installed the package in development mode:
   ```
   pip install -e .
   ```

2. The required dependencies:
   ```
   pip install -r requirements_demo.txt
   ```

## Included Test Scripts

### 1. Basic Agent Test

The `test_studybuddy.py` script tests basic interaction with the LyzrStudyBuddy agent:

```bash
python test_studybuddy.py
```

This performs two tests:
- A simple query to the agent
- Flashcard generation

### 2. Multi-Agent Workflow Example

The `examples/multi_agent_workflow.py` demonstrates a workflow that chains multiple agent calls:

```bash
python examples/multi_agent_workflow.py "Your Topic"
```

This simulates a content creation workflow with research, writing, and editing steps.

### 3. Streamlit Demo App

A Streamlit app that showcases the package's capabilities:

```bash
streamlit run demo_app.py
```

This provides a user-friendly interface with three tabs:
- Explain a Topic
- Generate Flashcards
- Pomodoro Planner

## Automated Testing

For convenience, we've included scripts to run the tests automatically:

### Windows:
```
run_tests.bat
```

### Linux/Mac:
```
chmod +x run_tests.sh
./run_tests.sh
```

## What to Check During Testing

1. **API Interaction**: Verify that the package correctly sends requests to and receives responses from the Lyzr agent API.

2. **Error Handling**: Test with invalid credentials or inputs to confirm proper error handling.

3. **Workflow Orchestration**: Check that the multi-step workflow correctly passes data between steps.

4. **CLI Functionality**: Verify the command-line interface works:
   ```
   lyzrboost version
   ```

5. **Performance**: Assess the responsiveness and efficiency of the package.

## Troubleshooting

- **API Key Issues**: Ensure the API key is correctly set either in the script or as the `LYZR_API_KEY` environment variable.

- **Connection Errors**: Check network connectivity and verify the API endpoint.

- **Import Errors**: Confirm the package is installed in development mode and all dependencies are installed.

## Next Steps After Testing

Once testing is complete and all functionality is verified, you can proceed with:

1. Making any necessary fixes or improvements
2. Updating the version number in `__init__.py` and `setup.py` if needed
3. Building the distribution packages
4. Publishing to PyPI 