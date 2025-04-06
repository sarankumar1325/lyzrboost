"""
Enhanced logging utilities for LyzrBoost.
"""

import logging
import sys
import os
from typing import Optional, Dict, Any, Union

# Default log format
DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def setup_logger(
    name: str = "lyzrboost",
    level: Union[int, str] = logging.INFO,
    format_string: Optional[str] = None,
    log_file: Optional[str] = None,
    console: bool = True
) -> logging.Logger:
    """
    Configure a logger with custom settings.
    
    Args:
        name: Logger name
        level: Logging level (e.g., logging.DEBUG, logging.INFO)
        format_string: Format string for log messages
        log_file: Optional path to write logs to a file
        console: Whether to output logs to console
        
    Returns:
        Configured logger instance
    """
    # Get the logger
    logger = logging.getLogger(name)
    
    # If logger is already configured, return it
    if logger.handlers:
        return logger
        
    # Set the logging level
    if isinstance(level, str):
        level = getattr(logging, level.upper())
    logger.setLevel(level)
    
    # Use the default format if none specified
    if format_string is None:
        format_string = DEFAULT_FORMAT
        
    formatter = logging.Formatter(format_string)
    
    # Add console handler if requested
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    # Add file handler if log_file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

def get_logger(name: str = "lyzrboost") -> logging.Logger:
    """
    Get an existing logger or create a new one with default settings.
    
    Args:
        name: Logger name (default is 'lyzrboost')
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    
    # If logger is not configured, set up with defaults
    if not logger.handlers:
        return setup_logger(name)
        
    return logger

class LogContext:
    """
    Context manager for adding temporary context to logs.
    
    This allows adding temporary fields to log records within a specific context.
    """
    
    def __init__(self, logger: logging.Logger, **context):
        """
        Initialize the log context.
        
        Args:
            logger: Logger instance to add context to
            **context: Key-value pairs to add to log records
        """
        self.logger = logger
        self.context = context
        self.old_factory = logging.getLogRecordFactory()
        
    def __enter__(self):
        """
        Enter the context and modify the log record factory.
        """
        old_factory = self.old_factory
        context = self.context
        
        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            for key, value in context.items():
                setattr(record, key, value)
            return record
            
        logging.setLogRecordFactory(record_factory)
        return self.logger
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context and restore the original log record factory.
        """
        logging.setLogRecordFactory(self.old_factory) 