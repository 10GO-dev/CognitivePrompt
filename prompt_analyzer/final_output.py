
import json
import yaml
from promptflow.core import tool
from promptflow.connections import CustomConnection
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from AzureCustomModel import ModelConfig, ModelParams

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

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
def final_output(filtered_prompt: str, optimization_prompt: str, filters_triggered: bool, conn: CustomConnection) -> str:

    m_profile_name = "prompt_optimization"
    system_prompt = optimization_prompt
    if filters_triggered:
        m_profile_name = "filter_context_evaluation"
        system_prompt = filtered_prompt


    model_profile = load_model_profile('.\models_profile.yaml', m_profile_name)
    model_params = ModelParams()
    model_params.load_from_dict(model_profile['parameters'])
    if(conn):
        model_config = ModelConfig(model_params,api_key=conn.secrets.get('api_key'), endpoint=conn.configs.get('api_url'))
    else:
        model_config = ModelConfig(model_params)

    client = ChatCompletionsClient(
    endpoint=model_config.get_endpoint(),
    credential=AzureKeyCredential(model_config.get_api_key()),
    )

    response = client.complete(
        messages=[
            UserMessage(content=system_prompt),
        ],
        max_tokens=model_config.get_model_max_tokens(),
        temperature=model_config.get_model_temperature(),
        top_p=model_config.get_model_top_p(),
        presence_penalty=model_config.get_model_presence_penalty(),
        frequency_penalty=model_config.get_model_frequency_penalty(),
        model=model_config.get_model_name(),
    )

    model_res = response.choices[0].message.content
    print(model_res)
    return model_res


def string_to_json(string_data: str):
    try:
        # Intentar convertir directamente
        return json.loads(string_data)
    except json.JSONDecodeError:
        try:
            # Si falla, intentar decodificar caracteres escapados antes de convertir
            cleaned_string = json.loads(string_data.replace('\n', '').replace('\\n', '\n'))
            return cleaned_string
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
