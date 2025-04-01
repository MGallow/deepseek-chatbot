# Contributing to DeepSeek Chatbot

Thank you for considering contributing to the DeepSeek Chatbot project! This document outlines the process for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by the following guidelines:

- Be respectful and inclusive in your communication
- Accept constructive criticism gracefully
- Focus on the best possible outcome for the project

## How to Contribute

### Reporting Issues

If you encounter a bug or have a feature request:

1. Check if the issue already exists in the [issue tracker](https://github.com/yourusername/deepseek_chatbot/issues)
2. If not, create a new issue with a clear, descriptive title
3. Include steps to reproduce (for bugs) or detailed descriptions (for features)
4. Add relevant labels to the issue

### Submitting Changes

1. Fork the repository
2. Create a new branch for your changes (`git checkout -b fix/issue-description` or `feature/feature-description`)
3. Make your changes, adhering to the coding conventions
4. Add tests for any new functionality
5. Ensure all tests pass with `make test`
6. Commit your changes with clear, descriptive commit messages
7. Push your branch to your fork
8. Submit a pull request

### Pull Request Process

1. Ensure your PR includes tests if adding new features
2. Update the README.md or documentation with details of changes if applicable
3. The PR will be merged once it receives approval from maintainers

## Development Environment

Set up your development environment:

```bash
# Create and activate the conda environment
conda create -n deepseek_chatbot python=3.10 -y
conda activate deepseek_chatbot

# Install development dependencies
make dev

# Install pre-commit hooks
make pre-commit-install
```

## Testing

Run tests with:

```bash
make test
```

## Code Style

This project follows the [Black](https://black.readthedocs.io/) code style. Format your code with:

```bash
make format
```

Run linting checks with:

```bash
make lint
```

## Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. The hooks are automatically run when you commit changes.

To install the pre-commit hooks:

```bash
make pre-commit-install
```

To manually run all pre-commit hooks on all files:

```bash
make pre-commit
```

The pre-commit configuration includes:

- Code formatting with Black
- Linting with Flake8
- Type checking with MyPy
- Various file checks (trailing whitespace, YAML validation, etc.)

## License

By contributing to this project, you agree that your contributions will be licensed under the same [MIT License](LICENSE) that covers the project.
