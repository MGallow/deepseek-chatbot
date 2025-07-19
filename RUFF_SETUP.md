# Ruff Configuration

This project uses [Ruff](https://docs.astral.sh/ruff/) for fast Python linting and formatting. Ruff replaces both Black and Flake8 with a single, much faster tool.

## Quick Start

### Install dependencies
```bash
# With uv (recommended)
uv sync

# Or with pip
pip install -e ".[dev]"
```

### Run Ruff commands

```bash
# Lint and auto-fix issues
uv run ruff check . --fix

# Format code
uv run ruff format .

# Check without fixing
uv run ruff check .

# Or use make commands
make lint    # Run ruff check + mypy
make format  # Run ruff format
```

### Pre-commit hooks

Install pre-commit hooks to automatically run Ruff on commits:

```bash
pre-commit install
```

## Configuration

Ruff is configured in `pyproject.toml` under the `[tool.ruff]` section. Key settings:

- **Line length**: 88 characters (Black compatible)
- **Target Python version**: 3.9+
- **Selected rules**: Pycodestyle (E, W), Pyflakes (F), isort (I), flake8-bugbear (B), comprehensions (C4), pyupgrade (UP), pydocstyle (D)
- **Ignored rules**: Common docstring rules that conflict with project style

## Migration from Black + Flake8

Ruff has replaced both Black and Flake8 in this project:
- **Formatting**: Ruff format (replaces Black)
- **Linting**: Ruff check (replaces Flake8)
- **Import sorting**: Built into Ruff (replaces isort)

The configuration maintains compatibility with previous Black formatting.
