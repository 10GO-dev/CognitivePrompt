from promptflow.core import tool
from promptflow.connections import AzureContentSafetyConnection
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def authenticate_client(conn: AzureContentSafetyConnection) -> TextAnalyticsClient:
    """Authenticate the Text Analytics client using the provided connection."""
    return TextAnalyticsClient(
        endpoint=conn.endpoint,
        credential=AzureKeyCredential(conn.api_key)
    )


def analyze_pii_entities(client: TextAnalyticsClient, user_input: str, category_list: list) -> list:
    """Analyze the input text for PII entities and filter by category list."""
    documents = [user_input]
    response = client.recognize_pii_entities(documents, language="en", categories_filter=category_list)
    print(response)
    filtered_results = []
    for doc in response:
        if not doc.is_error:
            filtered_entities = [
                entity for entity in doc.entities if entity.category in category_list
            ]
            doc.entities = filtered_entities
            filtered_results.append(doc)
    return filtered_results


def log_pii_entities(result: list) -> None:
    """Log the PII entities and redacted text."""
    for doc in result:
        print("Redacted Text: {}".format(doc.redacted_text))
        for entity in doc.entities:
            print("Entity: {}".format(entity.text))
            print("	Category: {}".format(entity.category))
            print("	Confidence Score: {}".format(entity.confidence_score))
            print("	Offset: {}".format(entity.offset))
            print("	Length: {}".format(entity.length))


def format_pii_result(result: list) -> dict:
    """Format the PII detection result into a readable JSON structure."""
    doc = result[0]
    if doc.is_error:
        return [{"error": doc.error}]
    
    doc_data = {
        "redacted_text": doc.redacted_text,
        "entities": [
            {
                "text": entity.text,
                "category": entity.category,
                "subcategory": entity.subcategory,
                "length": entity.length,
                "offset": entity.offset,
                "confidence_score": entity.confidence_score,
            }
            for entity in doc.entities
        ],
        "PII_detected": len(doc.entities) > 0,
    }
    return doc_data



@tool
def pii_recognition_detect(user_input: str, categoryList: list, conn: AzureContentSafetyConnection) -> dict:
    """Main function to detect PII entities in the input text."""
    client = authenticate_client(conn)
    result = analyze_pii_entities(client, user_input, categoryList)
    log_pii_entities(result)
    return format_pii_result(result)


