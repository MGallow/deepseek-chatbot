#!/bin/bash
# This script activates the conda environment for the deepseek-chatbot project
# Usage: source activate-env.sh

ENV_NAME="deepseek_chatbot"

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed or not in PATH"
    return 1
fi

# Check if the environment exists, create if it doesn't
if ! conda env list | grep -q "^${ENV_NAME} "; then
    echo "Creating conda environment: ${ENV_NAME}"
    conda env create -f environment.yml
fi

# Activate the environment
echo "Activating conda environment: ${ENV_NAME}"
conda activate ${ENV_NAME}

# Set environment variables
echo "Environment is ready to use!"
echo "Run 'make help' to see available commands"
