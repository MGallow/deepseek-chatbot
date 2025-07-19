.PHONY: clean install dev test lint format help conda-env conda-activate pre-commit pre-commit-install

# Python executable to use
PYTHON = python
CONDA = conda
ENV_NAME = deepseek_chatbot

.PHONY: clean install dev test lint format help conda-env conda-activate pre-commit pre-commit-install uv-install uv-dev uv-sync uv-lock uv-run-cli uv-run-app uv-test uv-lint uv-format

# Python executable to use
PYTHON = python
CONDA = conda
UV = uv
ENV_NAME = deepseek_chatbot

help:
	@echo "Available commands:"
	@echo ""
	@echo "📦 Package Management:"
	@echo "  make install     - Install the package for production"
	@echo "  make dev         - Install the package for development"
	@echo "  make clean       - Remove build artifacts"
	@echo ""
	@echo "🐍 Conda Environment:"
	@echo "  make conda-env   - Create the conda environment"
	@echo ""
	@echo "⚡ UV Commands (Recommended):"
	@echo "  make uv-install  - Install package with uv"
	@echo "  make uv-dev      - Install package in dev mode with uv"
	@echo "  make uv-sync     - Sync dependencies with uv"
	@echo "  make uv-lock     - Generate/update uv.lock file"
	@echo "  make uv-run-cli  - Run CLI app with uv"
	@echo "  make uv-run-app  - Run Streamlit app with uv"
	@echo "  make uv-test     - Run tests with uv"
	@echo "  make uv-lint     - Run linting with ruff and mypy using uv"
	@echo "  make uv-format   - Format code with ruff using uv"
	@echo ""
	@echo "🧪 Testing & Quality:"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linting checks with ruff"
	@echo "  make format      - Format code with ruff"
	@echo "  make pre-commit  - Run pre-commit checks on all files"
	@echo "  make pre-commit-install - Install pre-commit hooks"
	@echo ""
	@echo "🚀 Run Applications:"
	@echo "  make run-cli     - Run the CLI application"
	@echo "  make run-app     - Run the Streamlit application"

conda-env:
	$(CONDA) env create -f environment.yml --force

# UV Commands
uv-install:
	$(UV) sync --no-dev

uv-dev:
	$(UV) sync

uv-sync:
	$(UV) sync

uv-lock:
	$(UV) lock

uv-run-cli:
	$(UV) run python cli_app.py --interactive

uv-run-app:
	$(UV) run streamlit run streamlit_app.py

uv-test:
	$(UV) run pytest tests

uv-lint:
	$(UV) run ruff check deepseek_chatbot
	$(UV) run mypy deepseek_chatbot

uv-format:
	$(UV) run ruff format deepseek_chatbot

# Traditional pip commands
install:
	$(PYTHON) -m pip install .

dev:
	$(PYTHON) -m pip install -e ".[dev]"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test:
	$(PYTHON) -m pytest tests

lint:
	$(PYTHON) -m ruff check deepseek_chatbot
	$(PYTHON) -m mypy deepseek_chatbot

format:
	$(PYTHON) -m ruff format deepseek_chatbot

pre-commit:
	$(PYTHON) -m pre_commit run --all-files

pre-commit-install:
	$(PYTHON) -m pre_commit install

run-cli:
	$(PYTHON) cli_app.py --interactive

run-app:
	$(PYTHON) -m streamlit run streamlit_app.py
