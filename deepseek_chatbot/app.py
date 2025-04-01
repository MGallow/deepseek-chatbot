"""
DeepSeek Streamlit Application Module.

This module provides a Streamlit-based web interface for interacting with
the DeepSeek-V3 language model through Azure AI Inference SDK.
"""

import os

import streamlit as st
from azure.ai.inference.models import AssistantMessage, UserMessage
from dotenv import load_dotenv

from deepseek_chatbot.core import DeepSeekChatbot, get_token_from_env

# Load environment variables from .env file
load_dotenv()


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

        # Check for token in environment variables
        env_token = get_token_from_env()
        if env_token and not st.session_state.authenticated:
            st.session_state.authenticated = True
            st.session_state.token = env_token

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

        st.header("Settings")
        max_tokens = st.slider(
            "Max response length",
            min_value=100,
            max_value=4000,
            value=1000,
            help="Maximum number of tokens in the model's response",
        )

        streaming_enabled = st.checkbox("Stream response", value=True)

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

                    if streaming_enabled:
                        # Stream the response
                        full_response = ""
                        response = chatbot.get_response(api_messages, stream=True, max_tokens=max_tokens)
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
                        response = chatbot.get_response(api_messages, stream=False, max_tokens=max_tokens)
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


def run_app() -> None:
    """Start the Streamlit app from command line."""
    import sys
    import os

    # Add the current directory to sys.path to ensure proper imports
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

    # Pass command to streamlit
    import streamlit.web.cli as stcli

    sys.argv = ["streamlit", "run", __file__, "--global.developmentMode=false"]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
