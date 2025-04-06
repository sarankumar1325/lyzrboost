"""
Streamlit demo app for LyzrBoost showcasing the LyzrStudyBuddy agent.
"""

import os
import streamlit as st
import time
import subprocess
import sys
from lyzrboost.utils.logger import setup_logger

# ADDED: Setup logger for the demo app
logger = setup_logger(name="lyzrboost_demo", level="DEBUG")

# Default constants
DEFAULT_USER_ID = "sarankumar131313@gmail.com"
DEFAULT_AGENT_ID = "67e56da36443c3d4ecfc5e2a"
DEFAULT_API_KEY = "sk-default-9wdTatnu1figlN2UilBoBW0yz58wNokO"

# Set page config
st.set_page_config(
    page_title="LyzrStudyBuddy Demo",
    page_icon="📚",
    layout="wide",
)

# Custom CSS
st.markdown("""
<style>
.title {
    font-size: 42px;
    font-weight: bold;
    color: #4169E1;
    margin-bottom: 20px;
}
.subtitle {
    font-size: 20px;
    color: #555;
    margin-bottom: 30px;
}
.flashcard {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #4169E1;
    margin-bottom: 10px;
}
.loading {
    color: #888;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# App title
st.markdown("<div class='title'>📚 LyzrStudyBuddy</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Powered by LyzrBoost - Learn smarter, not harder!</div>", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Lyzr API Key", value=DEFAULT_API_KEY, type="password")
    user_id = st.text_input("User ID", value=DEFAULT_USER_ID)
    agent_id = st.text_input("Agent ID", value=DEFAULT_AGENT_ID)
    
    st.header("About")
    st.markdown("""
    This demo showcases the LyzrBoost package interacting with the LyzrStudyBuddy agent.
    
    LyzrStudyBuddy helps you:
    - Break down complex topics
    - Create effective flashcards
    - Optimize your study sessions
    
    [GitHub Repository](https://github.com/lyzr-ai/lyzrboost)
    """)

# Main app functionality
tab1, tab2, tab3 = st.tabs(["Explain a Topic", "Generate Key Points", "Pomodoro Planner"])

# Tab 1: Explain a Topic
with tab1:
    st.header("Explain a Topic")
    
    topic = st.text_input("Enter a topic or concept you want to learn:", placeholder="e.g., Transformer architecture, Python decorators, SQL joins", key="explain_topic_input")
    explain_button = st.button("Explain Topic", key="explain_btn")
    
    if explain_button and topic:
        with st.spinner(f"Generating explanation for '{topic}'... Please wait."):
            try:
                response = get_mock_agent_response(
                    message = f"Explain {topic} in simple terms with key concepts and examples.",
                    timeout=120
                )

                # Display response
                st.markdown("## Explanation")
                if response:
                    st.markdown(response)
                elif "Error:" in response:
                    st.error(response)
                else:
                    st.warning("Received no content from the mock agent.")
                
            except Exception as e:
                st.error(f"An unexpected error occurred in Streamlit: {e}")

# Tab 2: Generate Key Points
with tab2:
    st.header("Generate Key Points")
    
    flashcard_topic = st.text_input("Enter a topic to get key points for:", placeholder="e.g., Machine Learning algorithms, JavaScript basics", key="flashcard_topic_input")
    num_cards = st.slider("Number of points", min_value=3, max_value=10, value=5, key="flashcard_num_slider")
    generate_button = st.button("Generate Points", key="flashcard_btn")
    
    if generate_button and flashcard_topic:
        with st.spinner(f"Generating {num_cards} key points for '{flashcard_topic}'... Please wait."):
            try:
                response = get_mock_agent_response(
                    message = f"List {num_cards} key points or concepts about {flashcard_topic}. Provide a brief explanation for each.",
                    timeout=120
                )

                # Display response in a standard box
                st.markdown("## Agent Response")
                if response:
                    st.markdown(response)
                elif "Error:" in response:
                    st.error(response)
                else:
                    st.warning("Received no content from the mock agent.")
                
            except Exception as e:
                st.error(f"An unexpected error occurred in Streamlit: {e}")

# Tab 3: Pomodoro Planner
with tab3:
    st.header("Pomodoro Study Planner")
    
    study_topic = st.text_input("What topic are you studying?", placeholder="e.g., Calculus, Programming, History", key="pomodoro_topic_input")
    study_hours = st.number_input("How many hours do you want to study?", min_value=1, max_value=8, value=2, key="pomodoro_hours_input")
    plan_button = st.button("Create Study Plan", key="plan_btn")
    
    if plan_button and study_topic:
        with st.spinner(f"Creating a {study_hours}-hour Pomodoro plan for '{study_topic}'... Please wait."):
            try:
                plan_message = f"Create a detailed Pomodoro study plan for {study_hours} hours of studying {study_topic}. Break it down into 25-minute focused work sessions and 5-minute breaks. Include a longer 15-minute break after every 4 Pomodoros."
                plan_response = get_mock_agent_response(message=plan_message, timeout=120)
                
                # Display the study plan
                st.markdown("## Your Pomodoro Study Plan")
                if plan_response:
                     st.markdown(plan_response)
                elif "Error:" in plan_response:
                    st.error(plan_response)
                else:
                    st.warning("Received no content from the mock agent for the plan.")
                    
            except Exception as e:
                st.error(f"An unexpected error occurred while creating the plan: {e}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using LyzrBoost")

# --- MOCK FUNCTION --- 
def get_mock_agent_response(message: str, timeout: int = 120) -> str:
    """Calls the mock_agent_demo.py script and returns its stdout."""
    script_path = os.path.join(os.path.dirname(__file__), "mock_agent_demo.py")
    python_executable = sys.executable # Use the same python that runs streamlit
    logger.info(f"Calling mock agent: {python_executable} {script_path} '{message[:50]}...'")
    
    # Check if GEMINI_API_KEY is set (crucial for the mock script)
    if not os.environ.get("GEMINI_API_KEY"):
        logger.error("GEMINI_API_KEY is not set in the environment for the mock agent.")
        return "Error: GEMINI_API_KEY environment variable not set for the mock agent."
        
    try:
        process = subprocess.run(
            [python_executable, script_path, message],
            capture_output=True, 
            text=True, 
            timeout=timeout, # Use the timeout
            check=True, # Raise error if script fails
            encoding='utf-8' # Specify encoding
        )
        logger.debug(f"Mock agent stdout: {process.stdout}")
        logger.debug(f"Mock agent stderr: {process.stderr}")
        return process.stdout.strip()
    except FileNotFoundError:
        logger.error(f"Mock script not found at {script_path}")
        return f"Error: Mock script not found at {script_path}"
    except subprocess.TimeoutExpired:
        logger.error(f"Mock agent script timed out after {timeout} seconds.")
        return f"Error: Mock agent script timed out after {timeout} seconds."
    except subprocess.CalledProcessError as e:
        logger.error(f"Mock agent script failed with error code {e.returncode}")
        logger.error(f"Stderr: {e.stderr}")
        return f"Error executing mock agent script: {e.stderr}"
    except Exception as e:
        logger.error(f"Unexpected error calling mock agent: {e}", exc_info=True)
        return f"Unexpected Error calling mock agent: {e}" 