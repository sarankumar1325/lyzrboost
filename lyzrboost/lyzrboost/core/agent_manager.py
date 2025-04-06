"""
Module for managing agent sessions and API configurations.
"""

import os
import uuid
import logging
from typing import Dict, Optional, List, Any

# Configure logging
logger = logging.getLogger(__name__)

class AgentManager:
    """
    Manages Lyzr agent sessions and API configurations.
    
    This class provides utilities to:
    - Generate and track session IDs
    - Store and retrieve agent configurations
    - Manage API keys and endpoints
    """
    
    def __init__(self, api_key: Optional[str] = None, default_endpoint: Optional[str] = None):
        """
        Initialize the AgentManager.
        
        Args:
            api_key: Optional API key for Lyzr services
            default_endpoint: Optional API endpoint URL
        """
        # Use provided API key or check environment variable
        self.api_key = api_key or os.environ.get("LYZR_API_KEY")
        
        # Use provided endpoint or default from agent_api
        self.default_endpoint = default_endpoint
        
        # Dictionary to store active sessions
        self._sessions: Dict[str, Dict[str, Any]] = {}
        
        # Dictionary to cache agent metadata
        self._agent_cache: Dict[str, Dict[str, Any]] = {}
        
        logger.debug("AgentManager initialized")
    
    def generate_session_id(self, agent_id: str = None, prefix: str = "") -> str:
        """
        Generate a unique session ID.
        
        Args:
            agent_id: Optional agent ID to associate with the session
            prefix: Optional prefix for the session ID
            
        Returns:
            A unique session ID string
        """
        # Create a unique ID
        session_id = f"{prefix}{uuid.uuid4().hex}"
        
        # Initialize the session data
        self._sessions[session_id] = {
            "created_at": None,
            "last_access": None,
            "agent_id": agent_id,
            "history": []
        }
        
        logger.debug(f"Generated new session ID: {session_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the session data for a given session ID.
        
        Args:
            session_id: The session ID to retrieve
            
        Returns:
            Session data dictionary or None if not found
        """
        return self._sessions.get(session_id)
    
    def store_interaction(
        self,
        session_id: str,
        user_message: str,
        agent_response: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Store an interaction in the session history.
        
        Args:
            session_id: The session ID to update
            user_message: The message sent by the user
            agent_response: The response from the agent
            metadata: Optional additional data to store with the interaction
            
        Raises:
            KeyError: If the session_id is not found
        """
        if session_id not in self._sessions:
            raise KeyError(f"Session {session_id} not found")
            
        # Create the interaction record
        interaction = {
            "user_message": user_message,
            "agent_response": agent_response,
            "timestamp": None,  # Placeholder for timestamp
            "metadata": metadata or {}
        }
        
        # Add to session history
        self._sessions[session_id]["history"].append(interaction)
        logger.debug(f"Stored interaction in session {session_id}")
    
    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get the interaction history for a session.
        
        Args:
            session_id: The session ID to retrieve history for
            
        Returns:
            List of interaction records
            
        Raises:
            KeyError: If the session_id is not found
        """
        if session_id not in self._sessions:
            raise KeyError(f"Session {session_id} not found")
            
        return self._sessions[session_id]["history"]
    
    def clear_session(self, session_id: str) -> None:
        """
        Clear a session's history.
        
        Args:
            session_id: The session ID to clear
            
        Raises:
            KeyError: If the session_id is not found
        """
        if session_id not in self._sessions:
            raise KeyError(f"Session {session_id} not found")
            
        self._sessions[session_id]["history"] = []
        logger.debug(f"Cleared history for session {session_id}")
    
    def delete_session(self, session_id: str) -> None:
        """
        Delete a session.
        
        Args:
            session_id: The session ID to delete
            
        Raises:
            KeyError: If the session_id is not found
        """
        if session_id not in self._sessions:
            raise KeyError(f"Session {session_id} not found")
            
        del self._sessions[session_id]
        logger.debug(f"Deleted session {session_id}")
        
    def get_api_key(self) -> Optional[str]:
        """
        Get the current API key.
        
        Returns:
            The API key or None if not set
        """
        return self.api_key 