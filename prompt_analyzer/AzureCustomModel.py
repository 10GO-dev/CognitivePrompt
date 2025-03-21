import os
from dotenv import load_dotenv

load_dotenv()
endpoint = os.getenv("AZURE_AI_SERVICE_ENDPOINT")
model_name = os.getenv("AZURE_AI_MODEL_NAME")
api_key = os.getenv("AZURE_AI_SERVICE_API_KEY")


class ModelParams:
    def __init__(self, max_tokens: int = 250, temperature: float = 0.7, top_p: float = 0.95, presence_penalty: float = 0, frequency_penalty: float = 0):
        self.max_tokens: int = max_tokens
        self.temperature: float = temperature
        self.top_p: float = top_p
        self.presence_penalty: float = presence_penalty
        self.frequency_penalty: float = frequency_penalty

    def load_from_dict(self, params: dict):
        self.max_tokens = params.get("max_tokens", self.max_tokens)
        self.temperature = params.get("temperature", self.temperature)
        self.top_p = params.get("top_p", self.top_p)
        self.presence_penalty = params.get("presence_penalty", self.presence_penalty)
        self.frequency_penalty = params.get("frequency_penalty", self.frequency_penalty)

    def get_model_max_tokens(self):
        return self.max_tokens
    
    def get_model_temperature(self):
        return self.temperature
    
    def get_model_top_p(self):
        return self.top_p
    
    def get_model_presence_penalty(self):
        return self.presence_penalty
    
    def get_model_frequency_penalty(self):
        return self.frequency_penalty
        

class ModelConfig:
    def __init__(self, model_params: ModelParams, model_name: str = model_name, api_key: str = api_key, endpoint: str = endpoint):
        self.endpoint: str | None  = endpoint
        self.model_name: str | None = model_name
        self.api_key: str | None = api_key
        self.model_params: ModelParams = model_params
        if not endpoint:
            raise ValueError("AZURE_AI_MODELS_ENDPOINT is not set")
        if not model_name:
            raise ValueError("AZURE_AI_MODEL_NAME is not set")
        if not api_key:
            raise ValueError("AZURE_AI_MODELS_API_KEY is not set")

    def get_endpoint(self):
        return self.endpoint+"models/"
    
    def get_model_name(self):
        return self.model_name
    
    def get_api_key(self):
        return self.api_key
    
    def get_model_max_tokens(self):
        return self.model_params.max_tokens
    
    def get_model_temperature(self):
        return self.model_params.temperature
    
    def get_model_top_p(self):
        return self.model_params.top_p
    
    def get_model_presence_penalty(self):
        return self.model_params.presence_penalty
    
    def get_model_frequency_penalty(self):
        return self.model_params.frequency_penalty
    
    def get_model_params(self):
        return self.model_params