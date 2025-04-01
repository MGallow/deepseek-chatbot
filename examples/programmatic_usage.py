"""
Example script demonstrating how to use the DeepSeek-V3 model programmatically.

This script shows how to interact with the DeepSeek-V3 model using the
DeepSeek Chatbot package without the Streamlit interface.
"""

import sys
from dotenv import load_dotenv
from azure.ai.inference.models import UserMessage, SystemMessage

from deepseek_chatbot.core import DeepSeekChatbot, get_token_from_env

# Load environment variables from .env file
load_dotenv()


def main() -> None:
    """Demonstrate usage of the DeepSeek chatbot."""
    # Get token from environment variables
    token = get_token_from_env()

    if not token:
        print(
            "Error: No authentication token found. Please set GITHUB_TOKEN or AZURE_KEY "
            "environment variable."
        )
        print("You can also create a .env file based on env_example")
        sys.exit(1)

    # Initialize the chatbot
    chatbot = DeepSeekChatbot(token)

    # Example 1: Simple question with a single message
    print("\n=== Example 1: Simple Question ===\n")
    messages = [UserMessage("What is the capital of France?")]

    response = chatbot.get_response(messages)
    if (
        hasattr(response, "choices")
        and response.choices
        and response.choices[0].message
    ):
        print("Response:", response.choices[0].message.content)
    else:
        print("Error: Unable to get response from the model")

    # Example 2: Using a system message to set context
    print("\n=== Example 2: With System Message ===\n")
    messages = [
        SystemMessage("You are a helpful assistant specializing in geography."),
        UserMessage("Tell me about the geography of Japan."),
    ]

    response = chatbot.get_response(messages)
    if (
        hasattr(response, "choices")
        and response.choices
        and response.choices[0].message
    ):
        print("Response:", response.choices[0].message.content)
    else:
        print("Error: Unable to get response from the model")

    # Example 3: Streaming response
    print("\n=== Example 3: Streaming Response ===\n")
    messages = [UserMessage("Write a short poem about artificial intelligence.")]

    print("Response: ", end="", flush=True)
    for chunk in chatbot.get_response(messages, stream=True):
        if hasattr(chunk, "choices") and chunk.choices and chunk.choices[0].delta:
            content = chunk.choices[0].delta.content or ""
            print(content, end="", flush=True)

    print("\n")  # Add a newline at the end


if __name__ == "__main__":
    main()
