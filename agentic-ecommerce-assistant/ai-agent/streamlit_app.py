"""Streamlit chat UI for the ecommerce assistant."""

import streamlit as st

from agent import ask_agent


st.set_page_config(
    page_title="Agentic Ecommerce Assistant",
    page_icon=":speech_balloon:",
    layout="centered",
)


def _init_session_state() -> None:
    """Ensure chat state exists before rendering the app."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi, I can help with ecommerce FAQs, coupons, orders, and user-related"
                    " requests. Ask me something to get started."
                ),
            }
        ]


def _render_sidebar() -> None:
    """Render helper content and simple chat actions."""
    with st.sidebar:
        st.header("Chat Guide")
        st.markdown(
            "\n".join(
                [
                    "- Ask knowledge questions such as `What is your return policy?`",
                    "- Ask tool-style questions such as `What is my order status?`",
                    "- Try `Tell me about payment methods` or `Show coupon details`",
                ]
            )
        )

        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": (
                        "Chat cleared. Ask a new question whenever you're ready."
                    ),
                }
            ]
            st.rerun()


def _render_messages() -> None:
    """Render the conversation history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def _handle_user_prompt(prompt: str) -> None:
    """Add the user prompt, run the agent, and append the answer."""
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = ask_agent(prompt)
            except Exception as exc:
                response = (
                    "I hit an error while processing that request.\n\n"
                    f"Details: `{exc}`"
                )

        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})


def main() -> None:
    """Run the Streamlit app."""
    _init_session_state()

    st.title("Agentic Ecommerce Assistant")
    st.caption("Chat with the assistant instead of using the command line.")

    _render_sidebar()
    _render_messages()

    prompt = st.chat_input("Ask about orders, coupons, users, returns, or payments...")
    if prompt:
        _handle_user_prompt(prompt)


if __name__ == "__main__":
    main()
