"""
Configuration loader for AkronNova
Handles loading and accessing configuration values
"""

import json
from typing import Any, Union


class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self.load_config()
        
    def load_config(self) -> dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file not found at {self.config_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Invalid JSON in config file: {self.config_path}")
            return {}
            
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation
        Example: get("api_endpoints.tts_server")
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
                
        return value
        
    def set(self, key_path: str, value: Any):
        """Set a configuration value using dot notation"""
        keys = key_path.split('.')
        config_ref = self.config
        
        for key in keys[:-1]:
            if key not in config_ref or not isinstance(config_ref[key], dict):
                config_ref[key] = {}
            config_ref = config_ref[key]
            
        config_ref[keys[-1]] = value
        
    def save(self):
        """Save the current configuration to file"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)