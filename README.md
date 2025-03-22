🛡️ CognitivePrompt

This solution provides an AI prompt preprocesor that filter and improve AI prompts to get a acurate response from any MaaS LLM, primarily designed for **educational institutions**, but not limited to this sector.

We found and existing bug with the Text Moderation Tool of the promptflow extension that delayed us with the completion of the project: 
https://github.com/microsoft/promptflow/issues/3984

## Demo Video

Check out the demo video [here](https://www.youtube.com/embed/URZLwYUqaIM?si=S2M5Wwf5X5fQe_c1).


## Features
- **Prompt Shield**: Detects prompt injection attacks.
- **Moderation Profiles**: Create and customize different profiles with the desired sensitivity levels for different categories like hate, violence, and self-harm and a list of PII categories to detect.
- **PII Recognition**: Detect Personally Identifiable Information from the profile list.
- **Content Safety (Text Content Moderation)**: Detects harmful or unsafe content in prompts and documents based on the moderation profiles.
- **Grammar and Coherence Checks**: Ensures the input text is grammatically correct and coherent.

## Project Structure

![image](https://github.com/user-attachments/assets/5a56ea9f-38e7-44b8-9de6-3611c69dfd19)


- `prompt_analyzer/`: Contains the core tools and configurations for analyzing prompts.
- `requirements.txt`: Lists the dependencies required for the project.
- `pyproject.toml`: Configuration file for the project.
- `filters_configuration.yaml`: Defines moderation profiles for different domains.
- `models_profile.yaml`: Contains model parameters configurations.

## Requirements
   Azure AI Service Resource
   MaaS
   Promptflow extension Visual Studio Code
   uv (optional)
   
## Configuration

We recomend to use python 3.12

### Using `uv` for Dependency Management

This project uses [uv](https://github.com/uv-py/uv) for Python project and dependency management. To set up the project using `uv`, follow these steps:

1. Install `uv`:
   ```bash
   pip install uv
   ```
2. Navigate to the project directory
3. Create virtual environment
   ```bash
   uv venv
   ```
3. activate environment
    ```bash
   .venv\Script\activate
   ```
4. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

### Using `requirements.txt`

If you prefer not to use `uv`, you can install the dependencies directly from the `requirements.txt` file:

1. Navigate to the project directory:
2. Create virtual environment
    ```bash
   python -m venv .venv
   ```
3. activate environment
    ```bash
   .venv\Script\activate
   ```
4. Install the dependencies:
   ```bash
   pip install -r .requirements.txt
   ```

### Environment Variables (Optional)

The project requires certain environment variables to be set for Azure services. Create a `.env` file in the project root and add the following variables:

```
AZURE_AI_SERVICE_ENDPOINT=<your_azure_endpoint>
AZURE_AI_MODEL_NAME=<your_model_name>
AZURE_AI_SERVICE_API_KEY=<your_api_key>
```

Replace `<your_azure_endpoint>`, `<your_model_name>`, and `<your_api_key>` with your Azure service details.

### Prompflow Connections

The project requires to create connections to the different resouces eg. Azure AI Service, Azure AI Content Safety, CustomConections, etc...

![image](https://github.com/user-attachments/assets/4f56ab2f-2f76-447b-8b95-34809be8ef18)

## Running the Project

1. Ensure all dependencies are installed, connections and environment variables (optional) are configured.
2. Run the desired tools or scripts from the `prompt_analyzer` extension.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
