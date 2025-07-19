#!/usr/bin/env bash
# UV Setup Script for deepseek-chatbot
set -e

echo "🚀 Setting up uv for deepseek-chatbot..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "⚠️  uv is not installed. Installing uv..."

    # Install uv using the installer script
    if command -v brew &> /dev/null; then
        echo "📦 Installing uv via Homebrew..."
        brew install uv
    else
        echo "📦 Installing uv via curl..."
        curl -LsSf https://astral.sh/uv/install.sh | sh

        # Add uv to PATH for current session
        export PATH="$HOME/.local/bin:$PATH"

        echo "🔧 Please restart your shell or run: source ~/.bashrc (or ~/.zshrc)"
    fi
else
    echo "✅ uv is already installed: $(uv --version)"
fi

# Verify uv installation
if command -v uv &> /dev/null; then
    echo "✅ uv is ready to use!"

    # Create virtual environment and sync dependencies
    echo "🔄 Creating virtual environment and syncing dependencies..."
    uv sync

    echo ""
    echo "🎉 Setup complete! You can now use:"
    echo "   make uv-install    # Install production dependencies"
    echo "   make uv-dev        # Install development dependencies"
    echo "   make uv-run-app    # Run the Streamlit app"
    echo "   make uv-run-cli    # Run the CLI app"
    echo "   make uv-test       # Run tests"
    echo "   make uv-format     # Format code"
    echo "   make uv-lint       # Run linting"
else
    echo "❌ uv installation failed. Please install manually:"
    echo "   Visit: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi
