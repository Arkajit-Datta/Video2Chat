import os
import logging

from video2chat.llms.base_llm import BaseLLM

logging.basicConfig(filename="out.log", level=logging.INFO)
logger = logging.getLogger(__name__)

class Gemini(BaseLLM):
    def __init__(self, model = "gpt-4-0125-preview", temperature = 0.3, max_tokens = 1000, top_p = 0.95, frequency_penalty = 1, presence_penalty = 1, is_output_json_obj = True):
        super().__init__()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.is_output_json_obj = is_output_json_obj
    
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
    def get_source(self):
        return "gemini"

    def get_api_key(self):
        """
        Returns:
            str: The API key.
        """
        return self.api_key

    def get_model(self):
        """
        Returns:
            str: The model.
        """
        return self.model
    
    def chat_completion(self, messages) -> str:
        pass