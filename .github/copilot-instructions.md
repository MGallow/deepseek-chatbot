# DeepSeek Chatbot - AI Coding Agent Instructions

## Architecture Overview
This is a Python package providing dual interfaces to DeepSeek-V3 via Azure AI Inference:
- **Streamlit web UI** (`deepseek_chatbot/app.py`) for interactive chat
- **CLI tool** (`deepseek_chatbot/cli.py`) for programmatic/script usage
- **Core engine** (`deepseek_chatbot/core.py`) handling Azure AI Inference client

## Key Patterns & Conventions

### Authentication Flow
- Supports dual auth: GitHub tokens (free tier) OR Azure keys (pay-per-use)
- Token precedence: env variables (`GITHUB_TOKEN`/`AZURE_KEY`) → `.env` file → user input
- Both interfaces check `get_token_from_env()` first, fall back to prompts

### Package Structure & Entry Points
```
deepseek_chatbot/          # Core package
├── core.py               # DeepSeekChatbot class + Azure client
├── app.py               # Streamlit interface logic
└── cli.py               # CLI interface logic
streamlit_app.py         # Streamlit entry point
cli_app.py              # CLI entry point
```
**Key insight**: Top-level entry files are thin wrappers importing from package modules.

### Development Environment Strategy
- **Primary**: UV-based workflow (modern, fast)
- **Secondary**: Traditional conda/pip (for compatibility)
- Use `make help` for command overview
- UV commands prefixed: `make uv-run-app`, `make uv-test`, etc.

### Response Handling Pattern
Both interfaces handle streaming vs. non-streaming with defensive attribute checking:
```python
# Always check hasattr() before accessing response attributes
if (hasattr(response, "choices") and response.choices
    and response.choices[0].message):
    content = response.choices[0].message.content
```

### Error Handling Philosophy
- Graceful degradation: show error messages, don't crash
- Token validation happens at runtime, not import time
- CLI exits with sys.exit(1) on auth failure; Streamlit shows UI prompts

## Critical Developer Workflows

### Environment Setup
```bash
# Modern approach (preferred)
./setup-uv.sh              # Auto-installs UV + syncs deps
make uv-dev                 # Dev dependencies

# Traditional approach
source activate-env.sh      # Creates/activates conda env
make dev                    # Install with pip
```

### Running Applications
```bash
# UV-based (recommended)
make uv-run-app            # Streamlit web interface
make uv-run-cli            # Interactive CLI mode

# Direct commands
uv run streamlit run streamlit_app.py
uv run python cli_app.py --interactive
```

### Testing & Quality
```bash
make uv-test               # pytest with coverage
make uv-lint               # ruff + mypy
make uv-format             # ruff formatting
```

## Integration Points

### Azure AI Inference SDK
- Uses `ChatCompletionsClient` with `AzureKeyCredential`
- Endpoint: `https://models.inference.ai.azure.com`
- Model: `DeepSeek-V3`
- Message types: `UserMessage`, `AssistantMessage`, `SystemMessage`

### Configuration Sources
1. Constants in `__init__.py` (ENDPOINT, MODEL_NAME)
2. Environment variables via `python-dotenv`
3. pyproject.toml for package metadata + tool configs

### Session State Management (Streamlit)
- `st.session_state.messages` stores conversation history
- `st.session_state.authenticated` + `st.session_state.token` for auth
- Messages converted between Streamlit format and Azure AI message objects

## Project-Specific Conventions

### Import Style
```python
# Azure imports grouped together
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage, AssistantMessage
```

### CLI vs App Code Sharing
- Both interfaces import same core functions
- CLI handles streaming by printing chunks immediately
- Streamlit uses `st.empty()` container + progressive updates

### Package Distribution
- Console scripts defined in pyproject.toml:
  - `deepseek-cli` → `deepseek_chatbot.cli:main`
  - `deepseek-chat` → `deepseek_chatbot.app:run_app`

## Development Notes

### Code Quality Tools
- **Ruff**: Linting + formatting (replaces Black, isort, flake8)
- **MyPy**: Type checking with strict settings
- **pytest**: Testing with coverage reporting
- Line length: 88 characters (Black-compatible)

### File Modification Guidelines
- When editing core.py: Update type hints, maintain defensive checks
- When editing app.py: Test both streaming and non-streaming modes
- When editing CLI: Ensure both interactive and single-query modes work
- Always run `make uv-lint` before commits

### Example Usage Patterns
See `examples/programmatic_usage.py` for:
- Basic question/response
- System message usage
- Streaming response handling

## Common Gotchas
- Streamlit sessions persist; authentication state carries over
- Azure response objects may have None attributes; always check with hasattr()
- UV vs traditional pip: commands differ (`uv run` prefix vs direct execution)
- Environment activation: conda env named `deepseek_chatbot` (underscore, not hyphen)

- @azure Rule - Use Azure Best Practices: When generating code for Azure, running terminal commands for Azure, or performing operations related to Azure, invoke your `get_azure_best_practices` tool if available.
