# AI Prompt Processor

This project is designed to analyze and process AI prompts using various tools and configurations. It includes features like content safety analysis, grammar and coherence checks, and moderation profiles.

## Features

- **Content Safety Analysis**: Detects harmful or unsafe content in prompts and documents.
- **Grammar and Coherence Checks**: Ensures the input text is grammatically correct and coherent.
- **Moderation Profiles**: Customizable sensitivity levels for different categories like hate, violence, and self-harm.

## Project Structure

- `prompt_analyzer/`: Contains the core tools and configurations for analyzing prompts.
- `requirements.txt`: Lists the dependencies required for the project.
- `pyproject.toml`: Configuration file for the project.
- `moderation_profiles.yaml`: Defines moderation profiles for different domains.
- `models_profile.yaml`: Contains model configurations for grammar and coherence checks.

## Configuration

We recomend to use python 3.12

### Using `uv` for Dependency Management

This project uses [uv](https://github.com/uv-py/uv) for Python project and dependency management. To set up the project using `uv`, follow these steps:

1. Install `uv`:
   ```bash
   pip install uv
   ```

2. Navigate to the project directory:
   ```bash
   cd d:\Programing\ai_prompt_procesor
   ```

3. Install dependencies using `uv`:
   ```bash
   uv install
   ```

### Using `requirements.txt`

If you prefer not to use `uv`, you can install the dependencies directly from the `requirements.txt` file:

1. Navigate to the project directory:
   ```bash
   cd d:\Programing\ai_prompt_procesor
   ```

2. Install the dependencies:
   ```bash
   pip install -r .requirements.txt
   ```

### Environment Variables

The project requires certain environment variables to be set for Azure services. Create a `.env` file in the project root and add the following variables:

```
AZURE_AI_SERVICE_ENDPOINT=<your_azure_endpoint>
AZURE_AI_MODEL_NAME=<your_model_name>
AZURE_AI_SERVICE_API_KEY=<your_api_key>
```

Replace `<your_azure_endpoint>`, `<your_model_name>`, and `<your_api_key>` with your Azure service details.

## Running the Project

1. Ensure all dependencies are installed and environment variables are configured.
2. Run the desired tools or scripts from the `prompt_analyzer` directory.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
