import os
import json
import streamlit as st
from typing import Dict, Any

# Define the path to our JSON configuration file
CONFIG_FILE_PATH = "config.json"

class Settings:
    """
    Manages all application settings, loading from a JSON file and
    prioritizing Streamlit secrets for API keys.
    """
    def __init__(self):
        self._config_data: Dict[str, Any] = self._load_config_from_file()

        
        # LLM Configuration from JSON file
        self.LLM_PROVIDER: str = self._config_data.get("LLM_PROVIDER", "openai")
        self.LLM_MODEL: str = self._config_data.get("LLM_MODEL", "gpt-3.5-turbo")
        self.MAX_TOKENS: int = int(self._config_data.get("MAX_TOKENS", 150))
        self.TEMPERATURE: float = float(self._config_data.get("TEMPERATURE", 0.7))

        # System Prompt and Guardrail Configuration
        self.SYSTEM_PROMPTS: Dict[str, str] = self._config_data.get("SYSTEM_PROMPTS", {})
        self.ACTIVE_SYSTEM_PROMPT: str = self._config_data.get("ACTIVE_SYSTEM_PROMPT", "default")
        
        
        # API Keys - prioritize Streamlit secrets
        self.OPENAI_API_KEY: str = st.secrets.get("OPENAI_API_KEY", "")
        self.GOOGLE_API_KEY: str = st.secrets.get("GOOGLE_API_KEY", "")
        self.ANTHROPIC_API_KEY: str = st.secrets.get("ANTHROPIC_API_KEY", "")

    def _load_config_from_file(self) -> Dict[str, Any]:
        """
        Loads configuration from the specified JSON file.
        Includes error handling for file not found or invalid JSON format.
        """
        if not os.path.exists(CONFIG_FILE_PATH):
            st.error(f"Configuration file not found at: {CONFIG_FILE_PATH}")
            st.stop()
        
        try:
            with open(CONFIG_FILE_PATH, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON from {CONFIG_FILE_PATH}: {e}")
            st.stop()
        except Exception as e:
            st.error(f"An unexpected error occurred while loading {CONFIG_FILE_PATH}: {e}")
            st.stop()

# Create a single, accessible instance of the settings class
settings = Settings()