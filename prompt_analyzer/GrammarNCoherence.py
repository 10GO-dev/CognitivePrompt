
from fastapi import params
from openai import api_key
from promptflow.core import tool
from promptflow.connections import CustomConnection
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from AzureCustomModel import ModelConfig, ModelParams
import yaml
import os

def load_model_profile(file_path: str, profile_name: str) -> dict:
    """
    Load a model profile from a YAML file.

    Args:
        file_path (str): Path to the YAML file.
        profile_name (str): Name of the profile to load.

    Returns:
        dict: The model profile configuration.
    """


    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    
    if 'model_profiles' not in data or profile_name not in data['model_profiles']:
        raise ValueError(f"Profile '{profile_name}' not found in the YAML file.")
    
    return data['model_profiles'][profile_name]


@tool
def grammar_n_coherence(question: str, profile: str, conn: CustomConnection) -> dict:

    model_profile = load_model_profile('.\models_profile.yaml', "grammar_n_coherence")
    print(model_profile['parameters']['max_tokens'])
    model_params = ModelParams()
    model_params.load_from_dict(model_profile['parameters'])
    model_config = ModelConfig(model_params,api_key=conn.secrets.get('key1'), endpoint=conn.configs.get('api_url'))

    client = ChatCompletionsClient(
    endpoint=model_config.get_endpoint(),
    credential=AzureKeyCredential(model_config.get_api_key()),
    )

    response = client.complete(
        messages=[
            SystemMessage(content=model_profile['system_message']),
            UserMessage(content=question),
        ],
        max_tokens=model_config.get_model_max_tokens(),
        temperature=model_config.get_model_temperature(),
        top_p=model_config.get_model_top_p(),
        presence_penalty=model_config.get_model_presence_penalty(),
        frequency_penalty=model_config.get_model_frequency_penalty(),
        model=model_config.get_model_name(),
    )

    print(response.choices[0].message.content)

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
