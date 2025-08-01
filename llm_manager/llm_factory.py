import streamlit as st
from config.settings import settings
from openai import OpenAI
from google import genai
from anthropic import Anthropic

# Placeholder class for Anthropic
class AnthropicClient:
    def __init__(self, api_key: str):
        if not api_key:
            st.error("Anthropic API Key is not set.")
            st.stop()
        self.api_key = api_key
        st.info("Using Anthropic client placeholder.")
    def get_completion(self, model: str, messages: list, temperature: float):
        return f"Anthropic completion for {model}"

def get_llm_client(provider_name: str, api_key: str):
    """
    Factory function to get an LLM client based on the provider name.
    """
    if provider_name.lower() == "openai":
        if not api_key:
            st.error("OpenAI API Key is not configured.")
            st.stop()
        return OpenAI(api_key=api_key)
    
    elif provider_name.lower() == "google":
        if not api_key:
            st.error("Google API Key is not configured.")
            st.stop()
        return genai.Client(api_key=api_key)
    
    elif provider_name.lower() == "anthropic":
        if not api_key:
            st.error("Anthropic API Key is not configured.")
            st.stop()
        # Instantiate the real Anthropic client
        return Anthropic(api_key=api_key)
    
    else:
        st.error(f"Unsupported LLM provider: {provider_name}")
        st.stop()