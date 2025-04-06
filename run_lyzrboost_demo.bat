@echo off
echo Setting up Gemini API key...
set GEMINI_API_KEY=AIzaSyAA1heyOQ8a2yAwXuOWjGCVLCbpHy5iPYE

echo.
echo ==========================================
echo LYZRBOOST CONCEPTUAL EXAMPLE
echo ==========================================
echo.
python lyzrboost_example.py

echo.
echo ==========================================
echo GENERATING DETAILED LYZRBOOST PLAN
echo ==========================================
echo.
python lyzrboost_planner_stream.py

echo.
echo ==========================================
echo Demo completed! These files can be found in your current directory:
echo - lyzrboost_example.py: Shows how the API would work
echo - lyzrboost_planner.py: Generates package design (non-streaming)
echo - lyzrboost_planner_stream.py: Generates package design (streaming)
echo ==========================================

pause 