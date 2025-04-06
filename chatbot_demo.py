"""
LyzrBoost Demo: ChatBot Integration

This demo shows how to use LyzrBoost to enhance the Lyzr ChatBot module.
It demonstrates how to create a simple chatbot that can answer questions about a PDF document.

Usage:
    python chatbot_demo.py path/to/document.pdf "Your question about the document"
"""

import os
import sys
import argparse
from typing import List, Optional

# Import Lyzr ChatBot module
try:
    from lyzr import ChatBot
except ImportError:
    print("Error: The Lyzr package is not installed. Please install it with 'pip install lyzr'.")
    sys.exit(1)

# Import LyzrBoost modules
from lyzrboost.utils.logger import setup_logger
from lyzrboost.core.workflow import Workflow, WorkflowStep

# Configure logging
logger = setup_logger(name="chatbot_demo", level="INFO")

def initialize_chatbot(pdf_path: str, api_key: Optional[str] = None) -> ChatBot:
    """
    Initialize a Lyzr ChatBot with the given PDF document.
    
    Args:
        pdf_path: Path to the PDF document
        api_key: Optional API key for Lyzr services
        
    Returns:
        Initialized ChatBot instance
    """
    logger.info(f"Initializing ChatBot with document: {pdf_path}")
    
    # Set API key if provided
    if api_key:
        os.environ["LYZR_API_KEY"] = api_key
    
    try:
        # Create a ChatBot instance with the PDF document
        chatbot = ChatBot.pdf_chat(input_files=[pdf_path])
        logger.info("ChatBot initialized successfully")
        return chatbot
    except Exception as e:
        logger.error(f"Failed to initialize ChatBot: {str(e)}")
        raise

def ask_question(chatbot: ChatBot, question: str) -> str:
    """
    Ask a question to the chatbot.
    
    Args:
        chatbot: Initialized ChatBot instance
        question: Question to ask
        
    Returns:
        Chatbot's response
    """
    logger.info(f"Asking question: {question}")
    
    try:
        # Get response from the chatbot
        response = chatbot.chat(question)
        logger.info("Received response from ChatBot")
        return response
    except Exception as e:
        logger.error(f"Error getting response from ChatBot: {str(e)}")
        raise

def summarize_document(chatbot: ChatBot) -> str:
    """
    Ask the chatbot to summarize the document.
    
    Args:
        chatbot: Initialized ChatBot instance
        
    Returns:
        Summary of the document
    """
    logger.info("Requesting document summary")
    
    try:
        # Ask for a summary
        summary = chatbot.chat("Please provide a concise summary of this document.")
        logger.info("Received document summary")
        return summary
    except Exception as e:
        logger.error(f"Error getting document summary: {str(e)}")
        raise

def extract_key_points(chatbot: ChatBot) -> str:
    """
    Ask the chatbot to extract key points from the document.
    
    Args:
        chatbot: Initialized ChatBot instance
        
    Returns:
        Key points from the document
    """
    logger.info("Requesting key points extraction")
    
    try:
        # Ask for key points
        key_points = chatbot.chat("What are the 5 most important points or takeaways from this document?")
        logger.info("Received key points")
        return key_points
    except Exception as e:
        logger.error(f"Error extracting key points: {str(e)}")
        raise

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Demo of LyzrBoost with Lyzr ChatBot")
    parser.add_argument("pdf_path", help="Path to the PDF document")
    parser.add_argument("question", nargs="?", default=None, help="Question to ask about the document")
    parser.add_argument("--api-key", help="Lyzr API key (or set LYZR_API_KEY environment variable)")
    parser.add_argument("--summarize", action="store_true", help="Summarize the document")
    parser.add_argument("--key-points", action="store_true", help="Extract key points from the document")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Set logging level based on verbosity
    if args.verbose:
        logger.setLevel("DEBUG")
    
    try:
        # Initialize the chatbot
        chatbot = initialize_chatbot(args.pdf_path, args.api_key)
        
        # Define workflow based on arguments
        if args.question:
            # Simple question-answer workflow
            def qa_workflow(question):
                return ask_question(chatbot, question)
                
            workflow = Workflow(steps=[qa_workflow], name="QA_Workflow")
            result = workflow.run(args.question)
            
            print("\nQuestion:")
            print(args.question)
            print("\nAnswer:")
            print(result)
            
        elif args.summarize:
            # Document summarization workflow
            def summarize_workflow(_):
                return summarize_document(chatbot)
                
            workflow = Workflow(steps=[summarize_workflow], name="Summarize_Workflow")
            result = workflow.run(None)
            
            print("\nDocument Summary:")
            print(result)
            
        elif args.key_points:
            # Key points extraction workflow
            def key_points_workflow(_):
                return extract_key_points(chatbot)
                
            workflow = Workflow(steps=[key_points_workflow], name="KeyPoints_Workflow")
            result = workflow.run(None)
            
            print("\nKey Points:")
            print(result)
            
        else:
            # Comprehensive analysis workflow
            def comprehensive_workflow(_):
                summary = summarize_document(chatbot)
                key_points = extract_key_points(chatbot)
                
                return {
                    "summary": summary,
                    "key_points": key_points
                }
                
            workflow = Workflow(steps=[comprehensive_workflow], name="Comprehensive_Workflow")
            result = workflow.run(None)
            
            print("\nDocument Summary:")
            print(result["summary"])
            print("\nKey Points:")
            print(result["key_points"])
        
        return 0
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
