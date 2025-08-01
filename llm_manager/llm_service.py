from config.settings import settings
from llm_manager.llm_factory import get_llm_client
from google import genai

class LLMManager:
    def __init__(self):
        self.llm_provider = settings.LLM_PROVIDER
        self.llm_model = settings.LLM_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
        
        self.system_prompt_text = settings.SYSTEM_PROMPTS.get(
            settings.ACTIVE_SYSTEM_PROMPT, 
            settings.SYSTEM_PROMPTS.get("default", "You are a helpful assistant.")
        )
        
        # Pass the API key to the factory based on the provider
        if self.llm_provider.lower() == "openai":
            api_key = settings.OPENAI_API_KEY
        elif self.llm_provider.lower() == "google":
            api_key = settings.GOOGLE_API_KEY
        elif self.llm_provider.lower() == "anthropic":
            api_key = settings.ANTHROPIC_API_KEY
        else:
            api_key = None # Or raise an error
            
        self.client = get_llm_client(self.llm_provider, api_key)

    def get_response(self, messages: list, prompt: str) -> str:
        system_message = [{"role": "system", "content": self.system_prompt_text + f"\n All of your responses must always be less than {self.max_tokens} words."}]
        messages = system_message + messages
        try:
            # Handle API calls based on the provider
            if self.llm_provider.lower() == "openai":
                response = self.client.chat.completions.create(
                    model=self.llm_model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return response.choices[0].message.content
            
            elif self.llm_provider.lower() == "google":
                context = "\n".join(m["role"] + " - " + m["content"] + "\n" for m in messages)
                response = self.client.models.generate_content(
                    model=self.llm_model,
                    contents=context,
                    config={"max_output_tokens":self.max_tokens,
                            "temperature":self.temperature},
                    # system_instruction=self.system_prompt_text
                )
                return response.text
            
            # The placeholder call for Anthropic will work as before
            elif self.llm_provider.lower() == "anthropic":
                # Anthropic's API call using messages.create
                response = self.client.messages.create(
                    model=self.llm_model,
                    system=self.system_prompt_text, # System prompt is a separate parameter
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                )
                # The response object needs to be parsed for the content
                return response.content[0].text
            
        except Exception as e:
            return f"An error occurred while getting a response: {e}"