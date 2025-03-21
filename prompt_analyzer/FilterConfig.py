import yaml

from promptflow.core import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

MODERATION_PROFILES_PATH = ".\\filters_configuration.yaml"

# Definir perfil por defecto
DEFAULT_PROFILE = { 
    "hate": "medium_sensitivity",
    "self_harm": "medium_sensitivity",
    "sexual": "medium_sensitivity",
    "violence": "medium_sensitivity",
    "pii_entities": ['PhoneNumber','Address','Email','IPAddress'],
    "pii_enbled": "True"
}

# Load moderation profiles YAML file
def load_moderation_profiles(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return data["moderation_profiles"]

@tool
def filterConfig(question: str, profile: str) -> dict:
    moderation_profiles = load_moderation_profiles(MODERATION_PROFILES_PATH)
    profile = profile.lower()
    if len(moderation_profiles)> 0 and profile in moderation_profiles.keys():
        profile =  moderation_profiles[profile].get("category_filters")
        profile["pii_enabled"] = profile.get("pii_entities") is not None and len(profile.get("pii_entities")) > 0
        return profile
    return DEFAULT_PROFILE