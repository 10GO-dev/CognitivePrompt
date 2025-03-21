
from promptflow.core import tool
from promptflow.connections import AzureContentSafetyConnection
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


# Example method for detecting sensitive information (PII) from text 
@tool
def pii_recognition_detect(user_input: str, conn: AzureContentSafetyConnection) -> dict:
    
    # Authenticate the client using your key and endpoint 
    text_analytics_client = TextAnalyticsClient(
        endpoint=conn.endpoint,
        credential=AzureKeyCredential(conn.api_key)
    )
    
    documents = []
    documents.append(user_input)

    response = text_analytics_client.recognize_pii_entities(documents, language="en")
    result = [doc for doc in response if not doc.is_error]
    for doc in result:
        print("Redacted Text: {}".format(doc.redacted_text))
        for entity in doc.entities:
            print("Entity: {}".format(entity.text))
            print("	Category: {}".format(entity.category))
            print("	Confidence Score: {}".format(entity.confidence_score))
            print("	Offset: {}".format(entity.offset))
            print("	Length: {}".format(entity.length))

    return response