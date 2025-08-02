
# Clinic Patient Intake & Pre-Screening Chatbot

This project is a robust, modular, and extensible conversational AI assistant designed for configurable domain specific workflows. Built with Python and Streamlit, it leverages Large Language Models (LLMs) from multiple providers (Google, OpenAI, Anthropic) and supports advanced configuration, secure API key management, and customizable system prompts.

---

## Features

- **Multi-provider LLM support:** Easily switch between Google Gemini, OpenAI GPT, and Anthropic Claude via configuration.
- **Configurable system prompts:** Tailor the assistant's persona and guardrails using `config.json`.
- **Streamlit UI:** Modern, interactive chat interface for patient intake and triage.
- **Session-based chat history:** Maintains context throughout the conversation.
- **Secure API key management:** Uses `.env` for sensitive credentials.
- **Extensible architecture:** Modular design for adding new LLM providers or business logic.

---

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd domain-specific-conversational-agent
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys:**
   - Add your LLM provider API keys to Streamlit secrets. Create a `.streamlit/secrets.toml` file in the project root with the following format:

     ```toml
     OPENAI_API_KEY = "sk-..."
     GOOGLE_API_KEY = "..."
     ANTHROPIC_API_KEY = "..."
     ```

5. **Edit configuration (optional):**
   - Adjust `config.json` to set the active LLM provider, model, and system prompts.

6. **Run the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

---

## Project Structure

- `streamlit_app.py` — Main Streamlit web application.
- `config.json` — Central configuration for LLM provider, model, and system prompts.
- `requirements.txt` — Python dependencies.
- `llm_manager/` — LLM orchestration and provider modules.
- `config/settings.py` — Settings loader for environment/configuration variables.

---

## Configuration

### `config.json`

- `LLM_PROVIDER`: Selects the active LLM provider (`google`, `openai`, `anthropic`).
- `LLM_MODEL`: Model name for the selected provider.
- `MAX_TOKENS`, `TEMPERATURE`: LLM generation parameters.
- `ACTIVE_SYSTEM_PROMPT`: Key for the default system prompt.
- `SYSTEM_PROMPTS`: Dictionary of available system prompts (e.g., `formal`, `guardrail_strict`).


### `secrets.toml`

Store your API keys in `.streamlit/secrets.toml` as follows:

```toml
OPENAI_API_KEY = "sk-..."
GOOGLE_API_KEY = "..."
ANTHROPIC_API_KEY = "..."
```

---

## Usage

1. Open the Streamlit app in your browser.
2. The assistant will greet you and guide the intake process.
3. Enter patient information or questions in the chat input box.
4. The assistant will respond and may end the conversation with:
   > I’ll end our conversation here. Take care.
   At this point, the chat input will be disabled.

---

## Architecture Overview

- **LLMManager:** Central class for routing messages to the correct LLM provider.
- **LLM Service:** Each provider (Google, OpenAI, Anthropic) has its own implementation.
- **Settings loader:** Loads environment variables and config for secure, flexible operation.
- **Streamlit UI:** Handles chat display, session state, and user interaction.

---

## Extending the Project

To add a new LLM provider:
1. Implement a new provider class in `llm_manager/` following the existing interface.
2. Register the provider in `llm_manager/llm_factory.py`.
3. Add configuration options to `config.json` as needed.

---