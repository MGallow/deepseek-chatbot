"""
DeepSeek API Utility.

This script provides a command-line interface for interacting with the
DeepSeek-V3 language model through Azure AI Inference SDK.
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential

# Load environment variables from .env file
load_dotenv()

# Configuration
ENDPOINT = "https://models.inference.ai.azure.com"
MODEL_NAME = "DeepSeek-V3"


def get_credentials() -> str:
    """
    Get authentication credentials from environment variables or command line.

    Returns:
        str: Authentication token
    """
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("AZURE_KEY")

    if not token:
        print(
            "Error: No authentication token found. Set GITHUB_TOKEN or AZURE_KEY "
            "environment variable."
        )
        print("You can also create a .env file based on env_example")
        sys.exit(1)

    return token


def query_deepseek(prompt: str, stream: bool = False) -> str:
    """
    Send a query to the DeepSeek-V3 model and get a response.

    Args:
        prompt (str): The user's prompt or question
        stream (bool): Whether to stream the response

    Returns:
        str: The model's response
    """
    token = get_credentials()

    client = ChatCompletionsClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(token),
    )

    messages = [UserMessage(prompt)]

    try:
        if stream:
            # Stream response
            full_response = ""
            try:
                for chunk in client.complete(
                    stream=True,
                    messages=messages,
                    model=MODEL_NAME,
                    max_tokens=1000,
                ):
                    content = ""
                    if (
                        hasattr(chunk, "choices")
                        and chunk.choices
                        and hasattr(chunk.choices[0], "delta")
                        and chunk.choices[0].delta
                        and hasattr(chunk.choices[0].delta, "content")
                    ):
                        content = chunk.choices[0].delta.content or ""
                        full_response += content
                        print(content, end="", flush=True)

                print()  # Add a newline at the end
                return full_response
            except Exception as e:
                print(f"Error streaming response: {str(e)}")
                return "Error getting response from the model."
        else:
            # Get complete response
            response = client.complete(
                stream=False,
                messages=messages,
                model=MODEL_NAME,
                max_tokens=1000,
            )

            if (
                hasattr(response, "choices")
                and response.choices
                and hasattr(response.choices[0], "message")
                and response.choices[0].message
                and hasattr(response.choices[0].message, "content")
            ):
                # Explicitly cast to string to avoid mypy error
                content = response.choices[0].message.content
                return str(content)
            return "No response from the model."
    except Exception as e:
        print(f"Error communicating with DeepSeek model: {str(e)}")
        sys.exit(1)


def main() -> None:
    """Run the command-line interface for DeepSeek."""
    parser = argparse.ArgumentParser(description="DeepSeek API Utility")
    parser.add_argument("prompt", nargs="?", help="The prompt to send to DeepSeek")
    parser.add_argument("--stream", action="store_true", help="Stream the response")
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive mode"
    )

    args = parser.parse_args()

    if args.interactive:
        print("DeepSeek-V3 Interactive Mode (Type 'exit' to quit)")
        print("-" * 50)

        while True:
            try:
                user_input = input("\nYou: ")
                if user_input.lower() in ["exit", "quit"]:
                    break

                print("\nDeepSeek: ", end="")
                query_deepseek(user_input, stream=True)
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                print("\nExiting...")
                break
    elif args.prompt:
        response = query_deepseek(args.prompt, stream=args.stream)
        if not args.stream:
            print(response)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
