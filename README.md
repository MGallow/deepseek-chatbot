# DeepSeek Chatbot

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python package providing a Streamlit-based conversational interface and command-line tool for interacting with the DeepSeek-V3 language model through Azure AI Inference services.

![DeepSeek Chatbot](https://models.inference.ai.azure.com/static/ai/model-images/azure-deepseek.jpg)

## 📑 Table of Contents

- [Overview](#-overview)
- [Installation](#-installation)
  - [Prerequisites](#prerequisites)
  - [Quick Setup with uv (Recommended)](#quick-setup-with-uv-recommended)
  - [Setup with Conda](#setup-with-conda)
  - [Auto-Activate Environment](#auto-activate-environment-optional)
  - [Installation via pip](#installation-via-pip)
- [Authentication](#-authentication)
- [Running the Application](#-running-the-application)
- [Usage Examples](#-usage-examples)
- [Development](#-development)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Performance & Best Practices](#-performance--best-practices)
- [Limitations](#-limitations)
- [Additional Resources](#-additional-resources)
- [License](#-license)

## 📋 Overview

This package provides comprehensive tools to interact with DeepSeek-V3, a powerful large language model available through Azure AI Inference services. Features include:

- **🌐 Streamlit web interface** for interactive conversations with real-time streaming
- **⚡ Command-line interface** for quick queries, scripts, and automation
- **🔐 Flexible authentication** via GitHub token (free tier) or Azure key (production)
- **📱 Multiple interfaces** - Web UI, CLI, and Python API
- **🔄 Response streaming** for real-time feedback and better user experience
- **💬 Multi-turn conversations** with context retention and history management
- **📦 Easy installation** as a Python package with entry point commands
- **🛠️ Developer-friendly** with comprehensive development tools and automation
- **⚙️ Modern tooling** with uv support, pre-commit hooks, and automated formatting

## 🚀 Installation

### Prerequisites

- **Python**: 3.9 or higher (tested with 3.9, 3.10, 3.11, 3.12)
- **Authentication**: A GitHub token with `models:read` permission or an Azure AI Inference key
- **Network**: Internet connectivity for Azure AI Inference services
- **Package Manager**: pip (included with Python) or [uv](https://docs.astral.sh/uv/) (recommended)

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

# Windows with winget
winget install --id=astral-sh.uv  -e

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

# Or set environment variables directly
export GITHUB_TOKEN="your_github_token_here"
# or
export AZURE_AI_INFERENCE_KEY="your_azure_key_here"
```

**Environment Variable Precedence:**
1. `AZURE_AI_INFERENCE_KEY` (checked first)
2. `GITHUB_TOKEN` (checked second)
3. Interactive prompt (if neither is set)

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
print(response.choices[0].message.content)
```

#### Using System Messages

```python
from deepseek_chatbot.core import DeepSeekChatbot
from azure.ai.inference.models import SystemMessage, UserMessage

token = "your_github_token_or_azure_key"
chatbot = DeepSeekChatbot(token)

# Set up a conversation with system context
messages = [
    SystemMessage("You are a helpful Python programming assistant. Provide clear, concise code examples."),
    UserMessage("How do I read a CSV file with pandas?")
]

response = chatbot.get_response(messages)
print(response.choices[0].message.content)
```

#### Multi-turn Conversations

```python
from deepseek_chatbot.core import DeepSeekChatbot
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage

token = "your_github_token_or_azure_key"
chatbot = DeepSeekChatbot(token)

# Start a conversation
messages = [
    SystemMessage("You are a knowledgeable data scientist."),
    UserMessage("What is machine learning?")
]

# Get first response
response = chatbot.get_response(messages)
ai_response = response.choices[0].message.content

# Continue the conversation
messages.append(AssistantMessage(ai_response))
messages.append(UserMessage("Can you give me a simple example?"))

# Get follow-up response
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

This package includes comprehensive development tooling and automation:

### Dependency Management

The project supports both modern (`uv`) and traditional (`pip`/`conda`) dependency management:

#### Dependency Groups (pyproject.toml)
- **Production**: Core dependencies for running the application
- **Development**: Additional tools for development (black, flake8, mypy, pytest, pre-commit)

### With uv (Recommended)

```bash
# Install production dependencies only
make uv-install

# Install development dependencies
make uv-dev

# Sync dependencies with uv.lock (ensures reproducible builds)
make uv-sync

# Update lock file
make uv-lock

# Run formatting (black)
make uv-format

# Run linting (flake8 + mypy)
make uv-lint

# Run tests
make uv-test
```

### Traditional pip/conda

```bash
# Install development dependencies
make dev

# Run formatting
make format

# Run linting
make lint

# Run tests
make test

# Clean build artifacts
make clean
```

### Code Quality Tools

The project includes several code quality tools:

#### Pre-commit Hooks
```bash
# Install pre-commit hooks (runs automatically on git commit)
make pre-commit-install

# Run pre-commit checks on all files manually
make pre-commit
```

Configured hooks include:
- **black**: Code formatting
- **flake8**: Linting and style checking
- **mypy**: Static type checking
- **trailing-whitespace**: Remove trailing whitespace
- **end-of-file-fixer**: Ensure files end with newline
- **check-yaml/json/toml**: Validate file formats

#### Linting Configuration
- **Flake8**: Configured in `.flake8` with line length 88
- **MyPy**: Configured in `pyproject.toml` with strict type checking
- **Black**: Configured for 88 character line length

### UV Configuration

The `uv.toml` file configures the UV package manager:
- Uses highest resolution strategy for faster dependency resolution
- Caches dependencies for improved performance
- Prefers system Python installation

## 📝 Project Structure

```
deepseek-chatbot/
├── .github/                  # GitHub workflows and configurations
├── deepseek_chatbot/        # Main package directory
│   ├── __init__.py          # Package initialization and configuration
│   ├── app.py               # Streamlit application core
│   ├── cli.py               # Command-line interface
│   └── core.py              # Core functionality and DeepSeek client
├── examples/                # Usage examples
│   ├── __init__.py          
│   └── programmatic_usage.py # Python API examples
├── tests/                   # Test suite
│   ├── __init__.py          
│   └── test_core.py         # Core functionality tests
├── streamlit_app.py         # Streamlit app entry point
├── cli_app.py               # CLI app entry point
├── deepseek_cli.py          # Alternative CLI entry point
├── app.py                   # Alternative Streamlit entry point
├── pyproject.toml           # Project configuration and dependencies
├── uv.toml                  # UV package manager configuration
├── uv.lock                  # UV lock file for reproducible builds
├── requirements.txt         # Package dependencies (pip compatible)
├── environment.yml          # Conda environment specification
├── Makefile                 # Development automation commands
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── .flake8                  # Flake8 linting configuration
├── setup-uv.sh              # UV setup automation script
├── activate-env.sh          # Environment activation script
├── .envrc                   # direnv configuration
├── env_example              # Example environment variables
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE                  # MIT License
└── README.md                # This documentation
```

## 🔧 Troubleshooting

### Common Authentication Issues

#### "Authentication failed" error
- **GitHub Token**: Ensure your token has the `models:read` permission
- **Azure Key**: Verify your Azure subscription has access to AI Inference services
- **Environment Variables**: Check that your token is properly set in environment variables or `.env` file

#### Token not found
```bash
# Check if environment variable is set
echo $GITHUB_TOKEN
# or
echo $AZURE_AI_INFERENCE_KEY

# If using .env file, ensure it's in the project root
ls -la .env
```

#### Rate limiting issues
- **GitHub Free Tier**: Has usage limits; consider upgrading to Azure for production
- **Azure**: Monitor your usage in the Azure portal
- **Solution**: Implement exponential backoff in your application

### Installation Issues

#### UV installation fails
```bash
# Try alternative installation methods
pip install uv
# or use the project without uv
make dev  # Use traditional pip installation
```

#### Package installation fails
```bash
# Clear pip cache
pip cache purge

# Try installing with --no-cache-dir
pip install --no-cache-dir -e .

# For conda users
conda clean --all
```

#### Import errors
```bash
# Ensure the package is properly installed
pip list | grep deepseek-chatbot

# Reinstall in development mode
pip install -e .
```

### Runtime Issues

#### Streamlit app won't start
```bash
# Check if streamlit is installed
streamlit --version

# Try running with explicit python path
python -m streamlit run streamlit_app.py

# Check for port conflicts
lsof -i :8501
```

#### CLI commands not found
```bash
# Check if CLI scripts are installed
which deepseek-cli
which deepseek-chat

# If not found, reinstall the package
pip install -e .
```

## 🚀 Performance & Best Practices

### Authentication Best Practices

#### Environment Variable Precedence
The application checks for authentication in this order:
1. Environment variable `AZURE_AI_INFERENCE_KEY`
2. Environment variable `GITHUB_TOKEN`
3. Interactive prompt during application startup

#### Secure Token Storage
```bash
# Use .env file for development (never commit to git)
echo "GITHUB_TOKEN=your_token_here" > .env

# For production, use environment variables
export GITHUB_TOKEN="your_token_here"
```

### Performance Considerations

#### Rate Limits
- **GitHub Free Tier**: Limited requests per minute/hour
- **Azure Pay-as-you-go**: Higher limits but usage-based billing
- **Recommendation**: Implement caching for repeated queries

#### Memory Usage
- **Streaming**: Use streaming responses for long conversations to reduce memory usage
- **Message History**: Limit conversation history length for large applications

#### Network Optimization
```python
# Use streaming for better user experience
for chunk in chatbot.get_response(messages, stream=True):
    # Process chunk immediately
    pass
```

### Usage Recommendations

#### For Development
- Use GitHub tokens with the free tier
- Enable streaming for better development experience
- Use the Streamlit interface for interactive testing

#### For Production
- Use Azure keys for higher rate limits and reliability
- Implement proper error handling and retry logic
- Monitor usage and costs through Azure portal
- Consider implementing conversation session management

## ⚠️ Limitations

- **Rate Limits**: Free tier usage with GitHub tokens has rate limits
- **Production Use**: Azure Key authentication is recommended for production environments
- **Session Storage**: The application does not store conversation history between sessions
- **Model Limitations**: Subject to DeepSeek-V3 model capabilities and Azure AI Inference service limitations
- **Network Dependency**: Requires internet connectivity to access Azure AI services

## 📚 Additional Resources

- [DeepSeek-V3 Model Documentation](https://github.com/marketplace/models/azureml-deepseek/DeepSeek-V3)
- [Azure AI Inference SDK Documentation](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-inference-readme)
- [Azure AI Inference REST API](https://learn.microsoft.com/en-us/azure/ai-services/inference/reference)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [UV Package Manager Documentation](https://docs.astral.sh/uv/)
- [GitHub Personal Access Tokens Guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [Azure AI Services Setup Guide](https://learn.microsoft.com/en-us/azure/ai-services/)

## 📄 License

[MIT License](LICENSE)
