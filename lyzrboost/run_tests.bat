@echo off
echo LyzrBoost Test Runner
echo ===================
echo.

:: Set the API key as an environment variable
set LYZR_API_KEY=sk-default-9wdTatnu1figlN2UilBoBW0yz58wNokO

echo Running basic StudyBuddy test...
python test_studybuddy.py
echo.

echo Running multi-agent workflow example...
python examples\multi_agent_workflow.py "Machine Learning Basics"
echo.

echo To run the Streamlit demo app, use:
echo streamlit run demo_app.py
echo.

echo All tests completed!
pause 