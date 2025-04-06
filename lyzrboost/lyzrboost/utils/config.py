"""
Utilities for loading and managing configurations.
"""

import os
import yaml
import json
import logging
from typing import Dict, Any, Optional, Union

# Configure logging
logger = logging.getLogger(__name__)

class ConfigError(Exception):
    """Exception raised for configuration errors."""
    pass

def load_config(
    config_path: str,
    format: Optional[str] = None
) -> Dict[str, Any]:
    """
    Load a configuration file in YAML or JSON format.
    
    Args:
        config_path: Path to the configuration file
        format: Optional format specifier ('yaml', 'json')
                If None, format is inferred from file extension
    
    Returns:
        Dictionary containing the configuration
        
    Raises:
        ConfigError: If the file cannot be loaded or has invalid format
    """
    if not os.path.exists(config_path):
        raise ConfigError(f"Configuration file not found: {config_path}")
        
    # Infer format from file extension if not specified
    if format is None:
        _, ext = os.path.splitext(config_path)
        ext = ext.lower()
        
        if ext in ('.yml', '.yaml'):
            format = 'yaml'
        elif ext == '.json':
            format = 'json'
        else:
            raise ConfigError(f"Unable to infer format from file extension: {ext}")
    
    try:
        with open(config_path, 'r') as f:
            if format == 'yaml':
                return yaml.safe_load(f)
            elif format == 'json':
                return json.load(f)
            else:
                raise ConfigError(f"Unsupported format: {format}")
                
    except yaml.YAMLError as e:
        raise ConfigError(f"Error parsing YAML file: {str(e)}")
    except json.JSONDecodeError as e:
        raise ConfigError(f"Error parsing JSON file: {str(e)}")
    except Exception as e:
        raise ConfigError(f"Error loading configuration: {str(e)}")

def save_config(
    config: Dict[str, Any],
    config_path: str,
    format: Optional[str] = None
) -> None:
    """
    Save a configuration dictionary to a file in YAML or JSON format.
    
    Args:
        config: Dictionary containing the configuration
        config_path: Path to save the configuration file
        format: Optional format specifier ('yaml', 'json')
                If None, format is inferred from file extension
                
    Raises:
        ConfigError: If the file cannot be saved or has invalid format
    """
    # Infer format from file extension if not specified
    if format is None:
        _, ext = os.path.splitext(config_path)
        ext = ext.lower()
        
        if ext in ('.yml', '.yaml'):
            format = 'yaml'
        elif ext == '.json':
            format = 'json'
        else:
            raise ConfigError(f"Unable to infer format from file extension: {ext}")
    
    try:
        with open(config_path, 'w') as f:
            if format == 'yaml':
                yaml.dump(config, f, default_flow_style=False)
            elif format == 'json':
                json.dump(config, f, indent=2)
            else:
                raise ConfigError(f"Unsupported format: {format}")
                
        logger.debug(f"Configuration saved to: {config_path}")
                
    except Exception as e:
        raise ConfigError(f"Error saving configuration: {str(e)}")

def merge_configs(
    base_config: Dict[str, Any],
    override_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Merge two configuration dictionaries, with override_config taking precedence.
    
    Args:
        base_config: Base configuration dictionary
        override_config: Configuration to override base values
        
    Returns:
        Merged configuration dictionary
    """
    # Create a deep copy of the base config
    result = {}
    
    # Copy all keys from base config
    for key, value in base_config.items():
        if isinstance(value, dict) and key in override_config and isinstance(override_config[key], dict):
            # Recursively merge nested dictionaries
            result[key] = merge_configs(value, override_config[key])
        else:
            result[key] = value
            
    # Add keys from override config that aren't in base config
    for key, value in override_config.items():
        if key not in base_config:
            result[key] = value
            
    return result

def get_config_value(
    config: Dict[str, Any],
    key_path: str,
    default: Any = None
) -> Any:
    """
    Get a value from a nested configuration dictionary using a dot-notation path.
    
    Args:
        config: Configuration dictionary
        key_path: Dot-notation path to the desired value (e.g., 'database.host')
        default: Default value to return if the key isn't found
        
    Returns:
        The value at the specified path, or the default if not found
    """
    keys = key_path.split('.')
    result = config
    
    for key in keys:
        if isinstance(result, dict) and key in result:
            result = result[key]
        else:
            return default
            
    return result 