from dotenv import load_dotenv

from abc import ABC, abstractmethod

class BaseLLM(ABC):
    def __init__(self) -> None:
        load_dotenv()
    
    @abstractmethod
    def chat_completion(self):
        pass
    
    @abstractmethod
    def get_source(self):
        pass

    @abstractmethod
    def get_api_key(self):
        pass

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def get_models(self):
        pass

    @abstractmethod
    def verify_access_key(self):
        pass