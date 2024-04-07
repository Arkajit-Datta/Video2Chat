import os 
import logging
from openai import OpenAI



from video2chat.llms.base_llm import BaseLLM

logging.basicConfig(filename="out.log", level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAILLM(BaseLLM):
    def __init__(self, model = "gpt-4-1106-preview", temperature = 0.2, max_tokens = 1000, top_p = 0.95, frequency_penalty = 1, presence_penalty = 1, is_output_json_obj = True):
        super().__init__()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.is_output_json_obj = is_output_json_obj
        
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = OpenAI()
        
    def get_source(self):
        return "openai"

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
        """Call the OpenAI chat completion API.

        Args:
            messages (List): List of messages to send to the model.
        Returns:
            str: The response from the model.
        """
        try:
            if self.is_output_json_obj:
                response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    top_p=self.top_p,
                    response_format={"type": "json_object"}
                )
                
            else:
                response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    top_p=self.top_p,
                    response_format={"type": "json_object"}
                )
            return response.choices[0].message.content
        except self.openai_client.error.RateLimitError as rate_limit_error:
            logger.error("OpenAi RateLimitError:", rate_limit_error)
            return "Rate limit error"
        except self.openai_client.error.AuthenticationError as authentication_error:
            logger.error("OpenAi AuthenticationError:", authentication_error)
            return "Authentication error"
        except self.openai_client.error.InvalidRequestError as invalid_request_error:
            logger.error("OpenAi InvalidRequestError:", invalid_request_error)
            return "Invalid request error"
        except Exception as exception:
            logger.error("OpenAi Exception:", exception)
            return "Error"
        
    def verify_access_key(self):
        """
        Verify the access key is valid.

        Returns:
            bool: True if the access key is valid, False otherwise.
        """
        try:
            models = self.openai_client.Model.list()
            return True
        except Exception as exception:
            logger.info("OpenAi Exception:", exception)
            return False

    def get_models(self):
        """
        Get the models.

        Returns:
            list: The models.
        """
        try:
            models = self.openai_client.Model.list()
            models = [model["id"] for model in models["data"]]
            models_supported = ['gpt-4', 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4-32k']
            return [model for model in models if model in models_supported]
        except Exception as exception:
            logger.info("OpenAi Exception:", exception)
            return []
