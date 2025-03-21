from xml.dom.minidom import Document
import requests

from promptflow.core import tool, ToolProvider
from promptflow.connections import AzureContentSafetyConnection
from promptflow.tools.exception import AzureContentSafetySystemError


class ContentSafetyPromptShield(object):
    def __init__(self, endpoint: str, subscription_key: str, api_version: str) -> None:
        """
        Creates a new ContentSafety instance.

        Args:
        - endpoint (str): The endpoint URL for the Content Safety API.
        - subscription_key (str): The subscription key for the Content Safety API.
        - api_version (str): The version of the Content Safety API to use.
        """
        self.endpoint = endpoint
        self.subscription_key = subscription_key
        self.api_version = api_version

    def build_url(self) -> str:
        """
        Builds the URL for the Content Safety API

        Returns:
        - str: The URL for the Content Safety API.
        """

        return f"{self.endpoint}/contentsafety/text:shieldPrompt?api-version={self.api_version}"


    def build_headers(self) -> dict[str, str]:
        """
        Builds the headers for the Content Safety API request.

        Returns:
        - dict[str, str]: The headers for the Content Safety API request.
        """
        return {
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Content-Type": "application/json",
        }

    def build_request_body(self,user_prompt: str,documents: list) -> dict:
        """
        Builds the request body for the Content Safety API request.

        Args:
        - user_prompt (str): The user prompt to analyze.
        - documents (list): The documents to analyze.

        Returns:
        - dict: The request body for the Content Safety API request.
        """
        body = {
        "userPrompt": user_prompt,
        "documents": documents
        }
        return body
    
    def detect_groundness(self,user_prompt: str,documents: list) -> dict:
        """
        Detects the groundness of the user prompt and the documents.

        Args:
        - user_prompt (str): The user prompt to analyze.
        - documents (list): The documents to analyze.

        Returns:
        - dict: The result of the Content Safety API request.
        """
        url = self.build_url()
        headers = self.build_headers()
        data = self.build_request_body(user_prompt=user_prompt,documents=documents)
        response = requests.post(url, headers=headers, json=data)
        print("status code:", response.status_code)
        print("response:", response.json())
        res_content = response.json()
        if response.status_code != 200:
            error_message = f"Error: {response.status_code} - {res_content['error']['message']}"
            raise AzureContentSafetySystemError(message=error_message)
        return response.json()

class AzurePromptShield(ToolProvider):

    def __init__(self, connection: AzureContentSafetyConnection):
        self.connection = connection
        super(AzurePromptShield, self).__init__()


    def detect_groundness(self, user_prompt: str, documents: list) -> dict:
        """
        Detects the groundness of the user prompt and the documents.

        Args:
        - user_prompt (str): The user prompt to analyze.
        - documents (list): The documents to analyze.

        Returns:
        - dict: The result of the Content Safety API request.
        """
        promptShield = ContentSafetyPromptShield(
            endpoint=self.connection.endpoint,
            subscription_key=self.connection.api_key,
            api_version=self.connection.api_version
        )

        detection_result = promptShield.detect_groundness(user_prompt=user_prompt, documents=documents)
        return detection_result

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def prompt_detect(connection: AzureContentSafetyConnection, user_prompt: str, documents: list = [] ) -> dict:
    """
    Detects the groundness of the user prompt and the documents.

    Args:
    - user_prompt (str): The user prompt to analyze.
    - documents (list): The documents to analyze.

    Returns:
    - dict: The result of the Content Safety API request.
    """
    detect_result = AzurePromptShield(connection).detect_groundness(user_prompt=user_prompt, documents=documents)

    detect_result["attackDetected"] = atack_detected(detect_result)    

    return detect_result


def atack_detected(detect_result: dict) -> bool:

    user_analysis = detect_result["userPromptAnalysis"]
    document_analysis = detect_result["documentsAnalysis"]
    if user_analysis and user_analysis["attackDetected"]:
        return True

    if document_analysis and len(document_analysis)> 0:
        for document in document_analysis:
            if document["attackDetected"]:
                return True