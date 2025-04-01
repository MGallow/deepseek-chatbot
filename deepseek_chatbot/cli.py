"""
DeepSeek CLI Module.

This module provides a command-line interface for interacting with the
DeepSeek-V3 language model through Azure AI Inference SDK.
"""

import sys
import argparse
from typing import Optional
from dotenv import load_dotenv
from azure.ai.inference.models import UserMessage

from deepseek_chatbot.core import DeepSeekChatbot, get_token_from_env

# Load environment variables from .env file
load_dotenv()


def query_deepseek(prompt: str, stream: bool = False) -> Optional[str]:
    """
    Send a query to the DeepSeek-V3 model and get a response.

    Args:
        prompt: The user's prompt or question
        stream: Whether to stream the response

    Returns:
        The model's response, or None if there was an error
    """
    token = get_token_from_env()

    if not token:
        print("Error: No authentication token found. Set GITHUB_TOKEN or AZURE_KEY " "environment variable.")
        print("You can also create a .env file based on env_example")
        sys.exit(1)

    chatbot = DeepSeekChatbot(token)
    messages = [UserMessage(prompt)]

    try:
        if stream:
            # Stream response
            full_response = ""
            try:
                for chunk in chatbot.get_response(messages, stream=True):
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
                return None
        else:
            # Get complete response
            response = chatbot.get_response(messages, stream=False)
            if (
                response
                and hasattr(response, "choices")
                and response.choices
                and hasattr(response.choices[0], "message")
                and response.choices[0].message
                and hasattr(response.choices[0].message, "content")
            ):
                content = response.choices[0].message.content
                # Explicitly convert to str or return None to satisfy mypy
                return str(content) if content is not None else None
            return None
    except Exception as e:
        print(f"Error communicating with DeepSeek model: {str(e)}")
        sys.exit(1)


def main() -> None:
    """Run the command-line interface for DeepSeek."""
    parser = argparse.ArgumentParser(description="DeepSeek CLI")
    parser.add_argument("prompt", nargs="?", help="The prompt to send to DeepSeek")
    parser.add_argument("--stream", action="store_true", help="Stream the response")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")

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
