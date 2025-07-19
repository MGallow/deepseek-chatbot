# DeepSeek Chatbot

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Azure AI](https://img.shields.io/badge/Azure-AI%20Inference-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)

A Python package providing a Streamlit-based conversational interface and command-line tool for interacting with the DeepSeek-V3 language model through Azure AI Inference services.

![DeepSeek Chatbot](https://models.inference.ai.azure.com/static/ai/model-images/azure-deepseek.jpg)

## 📑 Table of Contents

- [Overview](#-overview)
- [Installation](#-installation)
  - [Prerequisites](#prerequisites)
  - [Quick Setup with uv (Recommended)](#quick-setup-with-uv-recommended)
  - [Setup with Conda](#setup-with-conda)
  - [Auto-Activate Environment (Optional)](#auto-activate-environment-optional)
  - [Installation via pip](#installation-via-pip)
- [Authentication](#-authentication)
- [Running the Application](#️-running-the-application)
- [Usage Examples](#-usage-examples)
- [Development](#-development)
- [Project Structure](#-project-structure)
- [Technical Details](#-technical-details)
- [Troubleshooting](#-troubleshooting)
- [Additional Resources](#-additional-resources)
- [License](#-license)

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

- **Python**: 3.9 or higher (3.10+ recommended)
- **Operating System**: Windows, macOS, or Linux
- **Authentication**: GitHub token with `models:read` permission or Azure API key
- **Network**: Internet connection for Azure AI Inference services

### Quick Setup with uv (Recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package manager. Use our setup script for the easiest installation:

```bash
# Clone the repository
git clone https://github.com/MGallow/deepseek-chatbot.git
cd deepseek-chatbot

# Run the setup script (installs uv if needed and sets up the project)
./setup-uv.sh
```

Or manually with uv:

```bash
# Install uv (if not already installed)
# macOS with Homebrew
brew install uv
# macOS/Linux with curl
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows with PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Clone and set up the project
git clone https://github.com/MGallow/deepseek-chatbot.git
cd deepseek-chatbot

# Create virtual environment and install dependencies
uv sync
```

### Setup with Conda

1. Clone this repository:

   ```bash
   git clone https://github.com/MGallow/deepseek-chatbot.git
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
pip install git+https://github.com/MGallow/deepseek-chatbot.git
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
# With uv (recommended)
uv run streamlit run streamlit_app.py
# or
make uv-run-app

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
# With uv (recommended)
uv run python cli_app.py "What is the capital of France?"
# or
make uv-run-cli "What is the capital of France?"

# If installed with pip
deepseek-cli "What is the capital of France?"

# If running from cloned repository
python cli_app.py "What is the capital of France?"
```

For interactive mode:

```bash
# With uv (recommended)
make uv-run-cli

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

#### Basic Usage

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
if (hasattr(response, "choices") and response.choices 
    and response.choices[0].message):
    print(response.choices[0].message.content)
```

#### Using System Messages

```python
from deepseek_chatbot.core import DeepSeekChatbot
from azure.ai.inference.models import UserMessage, SystemMessage

token = "your_github_token_or_azure_key"
chatbot = DeepSeekChatbot(token)

# Set context with a system message
messages = [
    SystemMessage("You are a helpful assistant specializing in geography."),
    UserMessage("Tell me about the geography of Japan.")
]

response = chatbot.get_response(messages)
if (hasattr(response, "choices") and response.choices 
    and response.choices[0].message):
    print(response.choices[0].message.content)
```

#### Multi-turn Conversations

```python
from deepseek_chatbot.core import DeepSeekChatbot
from azure.ai.inference.models import UserMessage, AssistantMessage, SystemMessage

token = "your_github_token_or_azure_key"
chatbot = DeepSeekChatbot(token)

# Start with system message and conversation history
messages = [
    SystemMessage("You are a helpful programming assistant."),
    UserMessage("How do I create a list in Python?"),
    AssistantMessage("You can create a list in Python using square brackets: my_list = [1, 2, 3]"),
    UserMessage("How do I add items to it?")
]

response = chatbot.get_response(messages)
if (hasattr(response, "choices") and response.choices 
    and response.choices[0].message):
    print(response.choices[0].message.content)
```

### Streaming Responses

```python
from deepseek_chatbot.core import DeepSeekChatbot
from azure.ai.inference.models import UserMessage

token = "your_github_token_or_azure_key"
chatbot = DeepSeekChatbot(token)
messages = [UserMessage("Write a short poem about artificial intelligence")]

# Stream the response
print("Response: ", end="", flush=True)
for chunk in chatbot.get_response(messages, stream=True):
    if hasattr(chunk, "choices") and chunk.choices and chunk.choices[0].delta:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
print()  # Add newline at the end
```

### Error Handling

```python
from deepseek_chatbot.core import DeepSeekChatbot, get_token_from_env
from azure.ai.inference.models import UserMessage
import sys

# Get token with error handling
token = get_token_from_env()
if not token:
    print("Error: No authentication token found.")
    print("Please set GITHUB_TOKEN or AZURE_KEY environment variable.")
    sys.exit(1)

try:
    chatbot = DeepSeekChatbot(token)
    messages = [UserMessage("Hello, how are you?")]
    response = chatbot.get_response(messages)
    
    if (hasattr(response, "choices") and response.choices 
        and response.choices[0].message):
        print("Response:", response.choices[0].message.content)
    else:
        print("Error: No valid response received")
        
except Exception as e:
    print(f"Error communicating with the model: {e}")
```

## 🔧 Development

This package uses modern Python tooling and includes comprehensive development commands.

### Dependency Management

The project uses dependency groups defined in `pyproject.toml`:

- **Production dependencies**: Core runtime requirements
- **Development dependencies (`[dev]`)**: Testing, linting, formatting tools

#### UV Configuration

The project includes `uv.toml` configuration for:
- Faster dependency resolution (`resolution = "highest"`)
- Centralized cache management (`.uv-cache` directory)
- System Python preference for better compatibility

### With uv (Recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package manager that's recommended for development:

```bash
# Install production dependencies only
make uv-install

# Install development dependencies
make uv-dev

# Sync dependencies with uv.lock file
make uv-sync

# Update lock file
make uv-lock

# Run applications
make uv-run-app    # Streamlit web interface
make uv-run-cli    # CLI application

# Code quality
make uv-format     # Format code with Ruff
make uv-lint       # Lint with Ruff and type-check with MyPy
make uv-test       # Run pytest with coverage
```

### Traditional pip/conda

For compatibility with traditional workflows:

```bash
# Install development dependencies
make dev

# Code quality
make format        # Format code with Ruff
make lint          # Lint with Ruff and MyPy
make test          # Run pytest

# Applications
make run-app       # Streamlit web interface
make run-cli       # CLI application

# Clean build artifacts
make clean
```

### Code Quality Tools

The project uses modern Python tooling:

- **[Ruff](https://docs.astral.sh/ruff/)**: Fast linting and formatting (replaces Black, isort, flake8)
- **[MyPy](https://mypy.readthedocs.io/)**: Static type checking
- **[pytest](https://docs.pytest.org/)**: Testing framework with coverage reporting
- **[pre-commit](https://pre-commit.com/)**: Git hooks for code quality

#### Ruff Configuration

The project is configured with:
- Line length: 88 characters (Black-compatible)
- Target: Python 3.9+
- Rules: pycodestyle, Pyflakes, isort, flake8-bugbear, pyupgrade, pydocstyle
- Google-style docstrings

#### Pre-commit Hooks

Install pre-commit hooks to automatically check code quality:

```bash
make pre-commit-install
# or
pre-commit install
```

## 📝 Project Structure

```
deepseek-chatbot/
├── deepseek_chatbot/          # Main package directory
│   ├── __init__.py            # Package initialization and constants
│   ├── app.py                 # Streamlit application logic
│   ├── cli.py                 # Command-line interface logic
│   └── core.py                # Core DeepSeek chatbot functionality
├── examples/                  # Usage examples
│   ├── __init__.py
│   └── programmatic_usage.py  # Python API examples
├── tests/                     # Test suite
│   ├── __init__.py
│   └── test_core.py          # Core functionality tests
├── streamlit_app.py          # Streamlit entry point
├── cli_app.py                # CLI entry point
├── deepseek_cli.py           # Legacy CLI entry point
├── app.py                    # Legacy app entry point
├── setup-uv.sh               # UV setup script
├── activate-env.sh           # Conda environment activation script
├── pyproject.toml            # Modern Python project configuration
├── uv.toml                   # UV package manager configuration
├── uv.lock                   # UV dependency lock file
├── environment.yml           # Conda environment specification
├── requirements.txt          # Traditional pip requirements
├── Makefile                  # Development commands
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
├── .ruffignore              # Ruff linter ignore patterns
├── .flake8                  # Flake8 configuration
├── .envrc                   # Direnv configuration
├── env_example              # Example environment variables
├── LICENSE                  # MIT License
└── README.md                # This documentation
```

## ⚡ Technical Details

### Azure AI Inference Integration

- **Endpoint**: `https://models.inference.ai.azure.com`
- **Model**: `DeepSeek-V3`
- **SDK Version**: `azure-ai-inference>=1.0.0b9`
- **Authentication**: GitHub token (free tier) or Azure API key (pay-per-use)

### Environment Variable Precedence

The application checks for authentication tokens in this order:

1. `GITHUB_TOKEN` environment variable
2. `AZURE_KEY` environment variable  
3. Values from `.env` file
4. Interactive prompts (CLI/Streamlit interface)

### Rate Limits and Usage

#### GitHub Token (Free Tier)
- Limited requests per hour
- Suitable for development and testing
- No cost but has usage restrictions

#### Azure API Key (Pay-per-use)
- Higher rate limits
- Recommended for production use
- Costs based on token usage

### Performance Considerations

- **Streaming**: Use `stream=True` for real-time response display
- **Context Length**: DeepSeek-V3 supports long context windows
- **Error Handling**: Always check response attributes with `hasattr()` for defensive programming
- **Session Management**: Streamlit maintains conversation history in session state

## 🐛 Troubleshooting

### Common Authentication Issues

**Problem**: "No authentication token found"
```bash
Error: No authentication token found. Please set GITHUB_TOKEN or AZURE_KEY environment variable.
```

**Solutions**:
1. Set environment variable:
   ```bash
   export GITHUB_TOKEN="your_token_here"
   # or
   export AZURE_KEY="your_azure_key_here"
   ```

2. Create `.env` file:
   ```bash
   cp env_example .env
   # Edit .env with your credentials
   ```

3. Check token permissions:
   - GitHub tokens need `models:read` permission
   - Azure keys must have access to AI services

**Problem**: "Invalid token" or authentication errors

**Solutions**:
1. Verify token format and permissions
2. Check if token has expired
3. Ensure proper scopes are granted

### Installation Issues

**Problem**: UV not found
```bash
make: uv: No such file or directory
```

**Solutions**:
1. Install uv:
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows PowerShell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # macOS with Homebrew
   brew install uv
   ```

2. Use traditional pip commands instead:
   ```bash
   make dev  # Instead of make uv-dev
   ```

**Problem**: Dependency conflicts

**Solutions**:
1. Use virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate  # Windows
   ```

2. Clean install:
   ```bash
   make clean
   make dev
   ```

### Runtime Issues

**Problem**: "No module named 'deepseek_chatbot'"

**Solutions**:
1. Install in development mode:
   ```bash
   pip install -e .
   ```

2. Check PYTHONPATH:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

**Problem**: Streamlit app won't start

**Solutions**:
1. Check if port 8501 is available
2. Try different port:
   ```bash
   streamlit run streamlit_app.py --server.port 8502
   ```

**Problem**: SSL/Network errors

**Solutions**:
1. Check internet connection
2. Try with different network (corporate firewalls may block Azure endpoints)
3. Check proxy settings if applicable

## ⚠️ Limitations

### Free Tier (GitHub Token)
- Limited requests per hour
- Rate limiting during peak usage
- Suitable for development and testing only

### General Limitations
- Conversation history not persisted between application restarts
- Requires active internet connection
- Subject to Azure AI Inference service availability
- DeepSeek-V3 model limitations apply (context length, response quality, etc.)

### Recommended for Production
- Use Azure API key for production deployments
- Implement proper error handling and retry logic
- Consider conversation persistence if needed
- Monitor usage and costs

## 📚 Additional Resources

### Documentation
- [DeepSeek-V3 Model Documentation](https://github.com/marketplace/models/azureml-deepseek/DeepSeek-V3)
- [Azure AI Inference SDK Documentation](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-inference-readme)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [UV Package Manager Documentation](https://docs.astral.sh/uv/)

### Development Tools
- [Ruff - Fast Python Linter](https://docs.astral.sh/ruff/)
- [MyPy - Static Type Checker](https://mypy.readthedocs.io/)
- [pytest - Testing Framework](https://docs.pytest.org/)
- [Pre-commit - Git Hooks](https://pre-commit.com/)

### Related Projects
- [Azure AI Inference Samples](https://github.com/Azure/azure-ai-inference)
- [Streamlit Components](https://docs.streamlit.io/develop/concepts/custom-components)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors
1. Fork the repository
2. Set up development environment: `./setup-uv.sh`
3. Install pre-commit hooks: `make pre-commit-install`
4. Create a feature branch
5. Make your changes and test them
6. Submit a pull request

## 📈 Changelog

See [GitHub Releases](https://github.com/MGallow/deepseek-chatbot/releases) for version history and changes.

## 📄 License

[MIT License](LICENSE)
