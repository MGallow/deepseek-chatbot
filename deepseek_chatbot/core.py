"""
DeepSeek Chatbot Core Module.

This module provides the core functionality for interacting with
the DeepSeek-V3 language model through Azure AI Inference SDK.
"""

import os
from typing import List, Optional, Union, Generator

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    AssistantMessage,
    SystemMessage,
    UserMessage,
    ChatCompletionsResponse,
    ChatCompletionsStreamResponse,
)
from azure.core.credentials import AzureKeyCredential

from deepseek_chatbot import ENDPOINT, MODEL_NAME


class DeepSeekChatbot:
    """
    A class that handles interactions with the DeepSeek-V3 model.

    This class manages the connection to Azure AI Inference services and provides
    methods for sending messages and receiving responses from the DeepSeek model.
    """

    def __init__(self, token: str) -> None:
        """
        Initialize the DeepSeek chatbot with authentication credentials.

        Args:
            token (str): GitHub token or Azure key for authentication
        """
        self.client = ChatCompletionsClient(
            endpoint=ENDPOINT,
            credential=AzureKeyCredential(token),
        )
        self.model_name = MODEL_NAME

    def get_response(
        self,
        messages: List[Union[UserMessage, AssistantMessage, SystemMessage]],
        stream: bool = False,
        max_tokens: int = 1000,
    ) -> Union[ChatCompletionsResponse, Generator[ChatCompletionsStreamResponse, None, None]]:
        """
        Get a response from the DeepSeek model based on the provided messages.

        Args:
            messages: List of message objects (UserMessage, AssistantMessage)
            stream: Whether to stream the response or not
            max_tokens: Maximum number of tokens to generate

        Returns:
            If stream=False, returns the complete response
            If stream=True, returns a stream of response chunks

        Raises:
            Exception: If there's an error communicating with the DeepSeek model
        """
        return self.client.complete(
            stream=stream,
            messages=messages,
            model=self.model_name,
            max_tokens=max_tokens,
        )


def get_token_from_env() -> Optional[str]:
    """
    Get authentication token from environment variables.

    Checks for GITHUB_TOKEN or AZURE_KEY environment variables.

    Returns:
        Optional[str]: The token if found, None otherwise
    """
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("AZURE_KEY")
