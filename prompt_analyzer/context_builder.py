import json
from promptflow.core import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def prompt_context_builder(prompt:str, # the initial prompt of the user
    chat_history: str | None,
    prompt_shield: dict | None,
    profile: dict | None,
    text_moderation: dict | None,
    pii_recognition: dict | None,
    grammar_n_coherence: dict | None,
) -> dict:
    """
    Combines the outputs from various tools into a structured JSON object for AI .

    Args:
    - prompt_shield (dict | None): Output from the prompt shield tool.
    - profile (dict | None): Profile information.
    - text_moderation (dict | None): Output from the text moderation tool.
    - pii_recognition (dict | None): Output from the PII recognition tool.
    - grammar_n_coherence (dict | None): Output from the grammar and coherence tool.

    Returns:
    - dict: A structured JSON object containing all the outputs.
    """

    filters_data = {
        "profile": profile or {},
        "prompt": prompt or {},
        "chat_history": chat_history or {},
        "prompt_shield": prompt_shield or {},
        "text_moderation": text_moderation or {},
        "pii_recognition": pii_recognition or {},
        "grammar_n_coherence": grammar_n_coherence or {},
    }

    return build_prompt_context(filters_data)

def build_prompt_context(json_output, history_depth=5):
    """
    Builds a structured AI prompt using the filtered data.
    
    :param json_output: JSON string containing filter results.
    :param history_depth: Number of previous chat messages to include.
    :return: AI-ready formatted prompt.
    """
    triggered_filter = False
    data = json_output
    profile = data.get("profile", "unknown")
    prompt = data.get("prompt", "")
    chat_history = data.get("chat_history", "")
    chat_messages = chat_history.split("\n") if chat_history else []
    
    corrected_prompt = data["grammar_n_coherence"].get("corrected_text", prompt)
    redacted_prompt = data["pii_recognition"].get("redacted_text", corrected_prompt)
    pii_detected = data["pii_recognition"].get("PII_detected", False)
    attack_detected = data["prompt_shield"].get("attackDetected", False)
    moderation_suggestions = data["text_moderation"].get("suggested_action", "Accept")

    # Start building the AI prompt
    ai_prompt = f"Profile: {profile}\n"
    ai_prompt += f"Current Prompt: {prompt}\n\n"

    # Add relevant chat history dynamically
    if chat_messages:
        ai_prompt += "[PREVIOUS CONVERSATION CONTEXT]:\n"
        ai_prompt += "\n".join(chat_messages[-history_depth:])  # Keep last `history_depth` messages
        ai_prompt += "\n\n"

    # Add PII status
    if pii_detected:
        ai_prompt += "⚠️ [PII DETECTED]: The input contained personally identifiable information (PII), which has been redacted.\n"
        ai_prompt += f"Redacted Prompt: {redacted_prompt}\n\n"
        triggered_filter = True
    else:
        ai_prompt += "[PII STATUS]: No personally identifiable information detected.\n\n"

    # Add grammar corrections
    if corrected_prompt != redacted_prompt:
        ai_prompt += "[GRAMMAR & COHERENCE]: The input has been corrected for grammar and coherence.\n"
        ai_prompt += f"Corrected Prompt: {corrected_prompt}\n\n"

    # Check for adversarial/jailbreak attempts
    if attack_detected:
        ai_prompt += "🚨 [SECURITY WARNING]: Potential attack detected in the input. Proceed with caution.\n\n"
        triggered_filter = True

    # Add moderation categories
    ai_prompt += "[CONTENT MODERATION STATUS]:\n"
    for category, action in data["text_moderation"].get("action_by_category", {}).items():
        ai_prompt += f"  - {category}: {action}\n"
    ai_prompt += f"Moderation Suggested Action: {moderation_suggestions}\n\n"

    if moderation_suggestions == "Blocked":
        triggered_filter = True

    # Final AI-ready instruction
    ai_prompt += "[FINAL PROCESSED PROMPT]:\n"
    ai_prompt += corrected_prompt if not pii_detected else redacted_prompt

    return {
        "ai_prompt":ai_prompt,
        "triggered_filter": triggered_filter
    }
