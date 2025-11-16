"""
Configuration loader for Streamlit UI
Reads settings from uiconfigfile.ini
"""
import configparser
import os
from pathlib import Path
from typing import Dict, List, Optional


class UIConfig:
    """UI Configuration loader"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration loader
        
        Args:
            config_path: Path to config file. If None, uses default location
        """
        if config_path is None:
            # Default to src/ui/uiconfigfile.ini
            current_dir = Path(__file__).parent
            config_path = current_dir / "uiconfigfile.ini"
        
        self.config_path = Path(config_path)
        self.config = configparser.ConfigParser()
        
        if self.config_path.exists():
            self.config.read(self.config_path)
        else:
            # Use defaults if config file doesn't exist
            self._set_defaults()
    
    def _set_defaults(self):
        """Set default configuration values"""
        self.config['DEFAULT'] = {
            'PAGE_TITLE': 'Agentic Blog Generator',
            'PAGE_ICON': '📝',
            'LAYOUT': 'wide',
            'API_ENDPOINT': 'http://localhost:8000/blogs',
            'API_TIMEOUT': '120',
            'DEFAULT_MODEL': 'gpt-4o',
            'DEFAULT_TEMPERATURE': '0.7',
            'TEMPERATURE_MIN': '0.0',
            'TEMPERATURE_MAX': '2.0',
            'TEMPERATURE_STEP': '0.1',
            'LANGUAGES': 'hindi, french, hausa, yoruba, igbo',
            'LANGUAGE_DEFAULT': '',
        }
    
    def get(self, key: str, fallback: Optional[str] = None) -> str:
        """Get a configuration value"""
        return self.config.get('DEFAULT', key, fallback=fallback)
    
    def get_int(self, key: str, fallback: int = 0) -> int:
        """Get a configuration value as integer"""
        return self.config.getint('DEFAULT', key, fallback=fallback)
    
    def get_float(self, key: str, fallback: float = 0.0) -> float:
        """Get a configuration value as float"""
        return self.config.getfloat('DEFAULT', key, fallback=fallback)
    
    def get_list(self, key: str, separator: str = ',') -> List[str]:
        """Get a configuration value as list"""
        value = self.get(key, '')
        return [item.strip() for item in value.split(separator) if item.strip()]
    
    def get_page_config(self) -> Dict:
        """Get Streamlit page configuration"""
        return {
            'page_title': self.get('PAGE_TITLE'),
            'page_icon': self.get('PAGE_ICON'),
            'layout': self.get('LAYOUT')
        }
    
    def get_api_config(self) -> Dict:
        """Get API configuration"""
        return {
            'endpoint': self.get('API_ENDPOINT'),
            'timeout': self.get_int('API_TIMEOUT')
        }
    
    def get_llm_config(self) -> Dict:
        """Get LLM default configuration"""
        return {
            'default_model': self.get('DEFAULT_MODEL'),
            'default_temperature': self.get_float('DEFAULT_TEMPERATURE'),
            'temperature_min': self.get_float('TEMPERATURE_MIN'),
            'temperature_max': self.get_float('TEMPERATURE_MAX'),
            'temperature_step': self.get_float('TEMPERATURE_STEP')
        }
    
    def get_languages(self) -> List[str]:
        """Get supported languages"""
        return self.get_list('LANGUAGES')
    
    def get_ui_text(self, key: str, fallback: str = '') -> str:
        """Get UI text configuration"""
        return self.get(key, fallback)


# Global config instance
_config_instance: Optional[UIConfig] = None


def get_config(config_path: Optional[str] = None) -> UIConfig:
    """Get or create global config instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = UIConfig(config_path)
    return _config_instance
