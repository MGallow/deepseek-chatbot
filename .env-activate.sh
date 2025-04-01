#!/bin/bash
# This script activates the conda environment for the deepseek-chatbot project
# Usage: source .env-activate.sh

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed or not in PATH"
    return 1
fi

# Check if the environment exists, create if it doesn't
if ! conda env list | grep -q "^$ENV_NAME"; then
    echo "Creating conda environment: $ENV_NAME"
    conda env create -f environment.yml
fi

# Activate the environment
echo "Activating conda environment: deepseek_chatbot"
conda activate deepseek_chatbot

# Set environment variables
echo "Environment is ready to use!"
echo "Run 'make help' to see available commands"
