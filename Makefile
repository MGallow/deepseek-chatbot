.PHONY: clean install dev test lint format help conda-env conda-activate pre-commit pre-commit-install

# Python executable to use
PYTHON = python
CONDA = conda
ENV_NAME = deepseek_chatbot

help:
	@echo "Available commands:"
	@echo "  make conda-env   - Create the conda environment"
	@echo "  make install     - Install the package for production"
	@echo "  make dev         - Install the package for development"
	@echo "  make clean       - Remove build artifacts"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linting checks"
	@echo "  make format      - Format code with black"
	@echo "  make run-cli     - Run the CLI application"
	@echo "  make run-app     - Run the Streamlit application"
	@echo "  make pre-commit  - Run pre-commit checks on all files"
	@echo "  make pre-commit-install - Install pre-commit hooks"

conda-env:
	$(CONDA) env create -f environment.yml --force

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
	$(PYTHON) -m flake8 deepseek_chatbot
	$(PYTHON) -m mypy deepseek_chatbot

format:
	$(PYTHON) -m black deepseek_chatbot

pre-commit:
	$(PYTHON) -m pre_commit run --all-files

pre-commit-install:
	$(PYTHON) -m pre_commit install

run-cli:
	$(PYTHON) cli_app.py --interactive

run-app:
	$(PYTHON) -m streamlit run streamlit_app.py
