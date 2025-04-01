"""
DeepSeek Chatbot Application.

This application provides a Streamlit-based interface for interacting with
the DeepSeek-V3 language model through Azure AI Inference SDK.
"""

import os
from typing import Optional, Union, Any, Generator
import streamlit as st
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Configuration
ENDPOINT = "https://models.inference.ai.azure.com"
MODEL_NAME = "DeepSeek-V3"


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

    def get_response(self, messages: list, stream: bool = False) -> Optional[Union[Any, Generator]]:
        """
        Get a response from the DeepSeek model based on the provided messages.

        Args:
            messages (list): List of message objects (UserMessage, AssistantMessage)
            stream (bool): Whether to stream the response or not

        Returns:
            If stream=False, returns the complete response
            If stream=True, returns a stream of response chunks
        """
        try:
            response = self.client.complete(
                stream=stream,
                messages=messages,
                model=self.model_name,
                max_tokens=1000,
            )
            return response
        except Exception as e:
            st.error(f"Error communicating with DeepSeek model: {str(e)}")
            return None


def init_session_state() -> None:
    """Initialize session state variables if they don't exist."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False


def main() -> None:
    """Run the Streamlit application."""
    st.set_page_config(page_title="DeepSeek Chatbot", page_icon="🤖", layout="wide")

    st.title("🤖 DeepSeek Chatbot")
    st.subheader("Chat with DeepSeek-V3 language model")

    init_session_state()

    # Authentication section
    with st.sidebar:
        st.header("Authentication")

        if not st.session_state.authenticated:
            auth_option = st.radio("Select authentication method", options=["GitHub Token", "Azure Key"])

            if auth_option == "GitHub Token":
                token = st.text_input(
                    "Enter your GitHub token",
                    type="password",
                    help="Your GitHub token needs models:read permissions",
                )
                st.markdown(
                    "Learn how to [create a GitHub token]"
                    "(https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/"
                    "managing-your-personal-access-tokens)"
                )
            else:
                token = st.text_input("Enter your Azure key", type="password")

            if st.button("Connect to DeepSeek"):
                if token:
                    # Set the token in environment variable
                    os.environ["GITHUB_TOKEN"] = token
                    st.session_state.authenticated = True
                    st.session_state.token = token
                    st.success("Authentication successful!")
                    st.experimental_rerun()
                else:
                    st.error("Please enter a valid token")
        else:
            st.success("Authenticated ✅")
            if st.button("Disconnect"):
                st.session_state.authenticated = False
                if "token" in st.session_state:
                    del st.session_state.token
                st.experimental_rerun()

        st.header("About")
        st.markdown(
            """
        This chatbot uses the DeepSeek-V3 language model through Azure AI Inference services.

        DeepSeek-V3 is an advanced language model that can handle a variety of natural language tasks.
        """
        )

    # Chat interface
    if st.session_state.authenticated:
        chatbot = DeepSeekChatbot(st.session_state.token)

        # Display chat messages
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            with st.chat_message(role):
                st.write(content)

        # Chat input
        user_input = st.chat_input("Type your message here...")

        if user_input:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Display user message
            with st.chat_message("user"):
                st.write(user_input)

            # Prepare messages for the API
            api_messages = []
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    api_messages.append(UserMessage(msg["content"]))
                elif msg["role"] == "assistant":
                    api_messages.append(AssistantMessage(msg["content"]))

            # Get model response (with spinner)
            with st.spinner("DeepSeek is thinking..."):
                with st.chat_message("assistant"):
                    response_container = st.empty()

                    if st.sidebar.checkbox("Stream response", value=True):
                        # Stream the response
                        full_response = ""
                        response = chatbot.get_response(api_messages, stream=True)
                        if response is not None:  # Check if response exists
                            try:
                                for chunk in response:
                                    # Safely check for attributes
                                    content = ""
                                    if (
                                        hasattr(chunk, "choices")
                                        and chunk.choices
                                        and hasattr(chunk.choices[0], "delta")
                                        and chunk.choices[0].delta is not None
                                        and hasattr(chunk.choices[0].delta, "content")
                                    ):
                                        content = chunk.choices[0].delta.content or ""

                                    full_response += content
                                    response_container.write(full_response)

                                final_response = full_response
                            except Exception as e:
                                st.error(f"Error streaming response: {str(e)}")
                                final_response = "Error getting response from the model."
                        else:
                            final_response = "Error getting response from the model."
                            response_container.error(final_response)
                    else:
                        # Get complete response
                        response = chatbot.get_response(api_messages, stream=False)
                        if response is not None:
                            if (
                                hasattr(response, "choices")
                                and response.choices
                                and hasattr(response.choices[0], "message")
                                and response.choices[0].message
                                and hasattr(response.choices[0].message, "content")
                            ):
                                final_response = response.choices[0].message.content
                                response_container.write(final_response)
                            else:
                                final_response = "Error getting response from the model."
                                response_container.error(final_response)
                        else:
                            final_response = "Error getting response from the model."
                            response_container.error(final_response)

                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": final_response})
    else:
        # Show intro message when not authenticated
        st.info("👈 Please authenticate using your GitHub token or Azure key to start chatting with DeepSeek-V3.")
        st.image(
            "https://models.inference.ai.azure.com/static/ai/model-images/azure-deepseek.jpg",
            width=400,
        )


if __name__ == "__main__":
    main()
