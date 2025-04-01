"""
Test module for the core functionality of DeepSeek Chatbot.

This module contains tests for the DeepSeekChatbot class and utility functions.
"""

import os
from unittest.mock import patch, MagicMock

from deepseek_chatbot.core import DeepSeekChatbot, get_token_from_env
from azure.ai.inference.models import UserMessage


class TestDeepSeekChatbot:
    """Tests for the DeepSeekChatbot class."""

    @patch("deepseek_chatbot.core.ChatCompletionsClient")
    def test_init(self, mock_client):
        """Test the initialization of DeepSeekChatbot."""
        # Arrange
        token = "test_token"

        # Act
        chatbot = DeepSeekChatbot(token)

        # Assert
        assert chatbot.model_name == "DeepSeek-V3"
        mock_client.assert_called_once()

    @patch("deepseek_chatbot.core.ChatCompletionsClient")
    def test_get_response(self, mock_client):
        """Test the get_response method."""
        # Arrange
        token = "test_token"
        messages = [UserMessage("test message")]
        mock_instance = mock_client.return_value
        mock_response = MagicMock()
        mock_instance.complete.return_value = mock_response

        # Act
        chatbot = DeepSeekChatbot(token)
        result = chatbot.get_response(messages, stream=False)

        # Assert
        assert result == mock_response
        mock_instance.complete.assert_called_once_with(
            stream=False, messages=messages, model="DeepSeek-V3", max_tokens=1000
        )


class TestUtilities:
    """Tests for utility functions."""

    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_github_token"})
    def test_get_token_from_env_github(self):
        """Test getting GitHub token from environment variables."""
        token = get_token_from_env()
        assert token == "test_github_token"

    @patch.dict(os.environ, {"AZURE_KEY": "test_azure_key", "GITHUB_TOKEN": ""})
    def test_get_token_from_env_azure(self):
        """Test getting Azure key from environment variables."""
        token = get_token_from_env()
        assert token == "test_azure_key"

    @patch.dict(os.environ, {"GITHUB_TOKEN": "", "AZURE_KEY": ""})
    def test_get_token_from_env_none(self):
        """Test getting token when none exists in environment variables."""
        token = get_token_from_env()
        assert token is None
