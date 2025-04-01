# DeepSeek Chatbot

A Python package providing a Streamlit-based conversational interface and command-line tool for interacting with the DeepSeek-V3 language model through Azure AI Inference services.

![DeepSeek Chatbot](https://models.inference.ai.azure.com/static/ai/model-images/azure-deepseek.jpg)

## 📋 Overview

This package provides tools to interact with DeepSeek-V3, a powerful large language model available through Azure AI Inference services. Features include:

- **Streamlit web interface** for interactive conversations
- **Command-line interface** for quick queries and scripts
- Authentication via GitHub token or Azure key
- Response streaming for real-time feedback
- Multi-turn conversations with context retention
- Installable as a Python package with CLI commands

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Conda (recommended for environment management)
- A GitHub token with `models:read` permission or an Azure key

### Setup with Conda (Recommended)

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd deepseek-chatbot
   ```

2. Create and activate the conda environment automatically:

   ```bash
   # Using the provided activation script
   source activate-env.sh

   # Or using make
   make conda-env
   conda activate deepseek_chatbot
   ```

3. Install the package in development mode:

   ```bash
   make dev
   # or
   pip install -e .
   ```

### Auto-Activate Environment (Optional)

This repository is set up to automatically activate the conda environment when you navigate to the project directory. There are two ways to enable this feature:

#### Option 1: Using direnv

1. Install direnv:

   ```bash
   # On macOS
   brew install direnv

   # On Linux
   # Follow instructions at https://direnv.net/docs/installation.html
   ```

2. Add direnv hook to your shell:

   ```bash
   # Add to your ~/.bashrc, ~/.zshrc, etc.
   eval "$(direnv hook bash)" # or zsh, fish, etc.
   ```

3. Allow direnv in the repository:

   ```bash
   direnv allow
   ```

Now the conda environment will automatically activate when you enter the repository directory.

#### Option 2: Manual Activation

Simply source the activation script whenever you work on the project:

```bash
source activate-env.sh
```

### Installation via pip

You can install the package directly from the repository:

```bash
pip install git+https://github.com/yourusername/deepseek_chatbot.git
```

## 🔑 Authentication

This application requires authentication to access DeepSeek-V3. You have two options:

### GitHub Token (Free tier)

1. [Create a GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) with `models:read` permission
2. Provide this token when prompted in the application or set it as an environment variable

### Azure Key (Pay-as-you-go)

1. Set up an Azure account with access to Azure AI services
2. Generate an API key for accessing the models
3. Provide this key when prompted in the application or set it as an environment variable

You can set your token in an environment variable or `.env` file:

```bash
# Copy env_example to .env and edit with your credentials
cp env_example .env
```

## 🏃‍♂️ Running the Application

### Streamlit Web Interface

Run the web interface with:

```bash
# If installed with pip
deepseek-chat

# If running from cloned repository
make run-app
# or
streamlit run streamlit_app.py
```

The application will start and open in your default web browser at <http://localhost:8501>.

### Command-Line Interface

Use the CLI for quick queries:

```bash
# If installed with pip
deepseek-cli "What is the capital of France?"

# If running from cloned repository
python cli_app.py "What is the capital of France?"
```

For interactive mode:

```bash
# If installed with pip
deepseek-cli --interactive

# If running from cloned repository
make run-cli
# or
python cli_app.py --interactive
```

## 💬 Usage Examples

### Python API

You can use the package programmatically in your Python code:

```python
from deepseek_chatbot.core import DeepSeekChatbot
from azure.ai.inference.models import UserMessage

# Initialize the chatbot with your token
token = "your_github_token_or_azure_key"
chatbot = DeepSeekChatbot(token)

# Prepare your messages
messages = [UserMessage("What is the capital of France?")]

# Get a response
response = chatbot.get_response(messages)
print(response.choices[0].message.content)
```

### Streaming Responses

```python
from deepseek_chatbot.core import DeepSeekChatbot
from azure.ai.inference.models import UserMessage

token = "your_github_token_or_azure_key"
chatbot = DeepSeekChatbot(token)
messages = [UserMessage("Write a short poem about AI")]

# Stream the response
for chunk in chatbot.get_response(messages, stream=True):
    if chunk.choices and chunk.choices[0].delta:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
```

## 🔧 Development

This package includes a Makefile to help with common development tasks:

```bash
# Install development dependencies
make dev

# Run formatting
make format

# Run linting
make lint

# Clean build artifacts
make clean
```

## 📝 Project Structure

```
deepseek_chatbot/
├── deepseek_chatbot/        # Main package directory
│   ├── __init__.py          # Package initialization
│   ├── app.py               # Streamlit application
│   ├── cli.py               # Command-line interface
│   └── core.py              # Core functionality
├── streamlit_app.py         # Entry point for Streamlit app
├── cli_app.py               # Entry point for CLI
├── LICENSE                  # MIT License
├── Makefile                 # Development commands
├── README.md                # This documentation
├── requirements.txt         # Package dependencies
├── setup.py                 # Package installation
└── env_example             # Example environment variables
```

## ⚠️ Limitations

- Free tier usage with GitHub tokens has rate limits
- For production use, Azure Key authentication is recommended
- The application does not store conversation history between sessions

## 📚 Additional Resources

- [DeepSeek-V3 Documentation](https://github.com/marketplace/models/azureml-deepseek/DeepSeek-V3)
- [Azure AI Inference SDK Documentation](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-inference-readme)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 📄 License

[MIT License](LICENSE)
