"""
Module for interacting with Lyzr agent inference API.
"""

import requests
import logging
import json
from typing import Dict, Any, Optional, Union

# Configure logging
logger = logging.getLogger(__name__)

# Constants
DEFAULT_API_ENDPOINT = "https://agent-prod.studio.lyzr.ai/v3/inference/chat/"

class APIError(Exception):
    """Exception raised for API errors."""
    pass

def send_agent_request(
    user_id: str,
    agent_id: str,
    session_id: str,
    message: str,
    api_key: Optional[str] = None,
    endpoint: str = DEFAULT_API_ENDPOINT,
    timeout: int = 60,
    **kwargs
) -> Dict[str, Any]:
    """
    Send a request to a Lyzr agent and get the response.
    
    Args:
        user_id: Unique identifier for the user
        agent_id: ID of the Lyzr agent to query
        session_id: Session identifier for conversation continuity
        message: The message to send to the agent
        api_key: API key for authentication (if None, must be set in environment)
        endpoint: API endpoint URL (defaults to production endpoint)
        timeout: Request timeout in seconds
        **kwargs: Additional parameters to include in the request
        
    Returns:
        Dict containing the agent's response
        
    Raises:
        APIError: If the API request fails
    """
    headers = {
        "Content-Type": "application/json",
    }
    
    # Add API key if provided
    if api_key:
        headers["x-api-key"] = api_key
        
    # Prepare the payload
    payload = {
        "user_id": user_id,
        "agent_id": agent_id,
        "session_id": session_id,
        "message": message,
        **kwargs
    }
    
    logger.debug(f"Sending request to {endpoint} for agent {agent_id}")
    
    try:
        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=timeout
        )
        
        # Check for HTTP errors
        response.raise_for_status()

        # ADDED: Print raw response content for debugging
        logger.debug(f"Raw API Response Content: {response.text}")

        # Parse the response
        data = response.json()
        logger.debug(f"Parsed API Response Data: {data}")
        logger.debug(f"Received response from agent {agent_id}")
        return data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise APIError(f"Failed to communicate with Lyzr API: {str(e)}")
    
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse API response: {str(e)}")
        raise APIError(f"Invalid response from Lyzr API: {str(e)}")

def get_agent_response(
    user_id: str,
    agent_id: str,
    session_id: Optional[str] = None,
    message: str = "",
    api_key: Optional[str] = None,
    **kwargs
) -> str:
    """
    Simplified wrapper that returns just the agent's text response.
    
    Args:
        user_id: Unique identifier for the user
        agent_id: ID of the Lyzr agent to query
        session_id: Session identifier (defaults to agent_id if None)
        message: The message to send to the agent
        api_key: API key for authentication
        **kwargs: Additional parameters passed to send_agent_request
        
    Returns:
        String containing the agent's text response
        
    Raises:
        APIError: If the API request fails
    """
    # Use the agent_id as the session_id if none provided
    if session_id is None:
        session_id = agent_id
        
    # Get the full response
    response_data = send_agent_request(
        user_id=user_id,
        agent_id=agent_id,
        session_id=session_id,
        message=message,
        api_key=api_key,
        **kwargs
    )
    
    # Extract just the text response
    # Note: This assumes a specific response format and may need adjustment
    try:
        # ADDED: Log the data being processed
        logger.debug(f"Extracting response from data: {response_data}")
        return response_data.get("data", {}).get("response", "")
    except (AttributeError, KeyError) as e:
        logger.error(f"Failed to extract response text: {str(e)}")
        raise APIError(f"Unexpected response format: {str(e)}") 