"""Chat UI component for the A2A demo with enhanced UX."""
import reflex as rx
from ..state import State, Message


def message_bubble(message: Message) -> rx.Component:
    """Render a single message bubble with improved styling."""
    is_user = message.role == "user"
    
    return rx.box(
        rx.box(
            rx.text(
                message.content,
                size="3",
                white_space="pre-wrap",
            ),
            padding="12px 16px",
            background=rx.cond(
                is_user,
                "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "white",
            ),
            color=rx.cond(is_user, "white", "#333"),
            border_radius="18px",
            max_width="70%",
            box_shadow="0 2px 8px rgba(0,0,0,0.1)",
            border=rx.cond(is_user, "none", "1px solid #e0e0e0"),
            # Smooth animation on new messages
            animation="fadeInUp 0.3s ease-out",
        ),
        display="flex",
        justify_content=rx.cond(is_user, "flex-end", "flex-start"),
        width="100%",
        margin_bottom="12px",
    )


def typing_indicator() -> rx.Component:
    """Show a typing indicator when processing."""
    return rx.cond(
        State.is_processing,
        rx.box(
            rx.box(
                rx.hstack(
                    rx.box(
                        width="8px",
                        height="8px",
                        border_radius="50%",
                        background="#667eea",
                        animation="bounce 1.4s infinite ease-in-out both",
                        animation_delay="0s",
                    ),
                    rx.box(
                        width="8px",
                        height="8px",
                        border_radius="50%",
                        background="#667eea",
                        animation="bounce 1.4s infinite ease-in-out both",
                        animation_delay="0.2s",
                    ),
                    rx.box(
                        width="8px",
                        height="8px",
                        border_radius="50%",
                        background="#667eea",
                        animation="bounce 1.4s infinite ease-in-out both",
                        animation_delay="0.4s",
                    ),
                    spacing="1",
                ),
                padding="12px 16px",
                background="white",
                border_radius="18px",
                box_shadow="0 2px 8px rgba(0,0,0,0.1)",
                border="1px solid #e0e0e0",
            ),
            display="flex",
            justify_content="flex-start",
            width="100%",
            margin_bottom="12px",
        ),
        rx.fragment(),
    )


def error_banner() -> rx.Component:
    """Show error banner with improved styling and dismiss button."""
    return rx.cond(
        State.error_message != "",
        rx.box(
            rx.hstack(
                rx.icon("alert-circle", size=18, color="#dc2626"),
                rx.text(State.error_message, color="#dc2626", weight="medium"),
                rx.spacer(),
                rx.button(
                    rx.icon("x", size=16),
                    on_click=State.clear_error,
                    size="1",
                    variant="ghost",
                    color_scheme="red",
                ),
                width="100%",
                align="center",
            ),
            padding="12px 16px",
            background="linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)",
            border_bottom="1px solid #fecaca",
        ),
        rx.fragment(),
    )


def chat_input() -> rx.Component:
    """Render the chat input area with improved styling."""
    return rx.box(
        rx.hstack(
            rx.input(
                placeholder="Type your message...",
                value=State.current_input,
                on_change=State.set_current_input,
                flex="1",
                size="3",
                radius="full",
                disabled=State.is_processing,
                style={
                    "box_shadow": "0 2px 8px rgba(0,0,0,0.05)",
                    "border": "1px solid #e0e0e0",
                },
            ),
            rx.button(
                rx.cond(
                    State.is_processing,
                    rx.spinner(size="3"),
                    rx.icon("send", size=20),
                ),
                on_click=State.send_message,
                size="3",
                radius="full",
                disabled=State.is_processing,
                style={
                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    "cursor": "pointer",
                    "box_shadow": "0 2px 8px rgba(102,126,234,0.4)",
                    "transition": "all 0.2s ease",
                },
            ),
            width="100%",
            spacing="3",
        ),
        padding="16px",
        background="white",
        border_top="1px solid #eee",
        box_shadow="0 -2px 10px rgba(0,0,0,0.05)",
    )


def api_key_setup() -> rx.Component:
    """Show API key setup card."""
    return rx.center(
        rx.box(
            rx.vstack(
                rx.icon("key", size=48, color="#667eea"),
                rx.heading("Configure API Key", size="5", color="#333"),
                rx.text(
                    "Enter your Google Gemini API key to start chatting with AI agents.",
                    color="#666",
                    size="3",
                    text_align="center",
                ),
                rx.input(
                    placeholder="Enter your Gemini API key...",
                    value=State.api_key,
                    on_change=State.set_api_key,
                    type="password",
                    width="100%",
                    size="3",
                ),
                rx.button(
                    rx.icon("check", size=18),
                    "Save API Key",
                    on_click=State.save_api_key,
                    size="3",
                    style={
                        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        "width": "100%",
                    },
                ),
                rx.link(
                    rx.text(
                        "Get a free API key from Google AI Studio →",
                        size="2",
                        color="#667eea",
                    ),
                    href="https://aistudio.google.com/app/apikey",
                    is_external=True,
                ),
                spacing="4",
                align="center",
                padding="32px",
                width="100%",
            ),
            background="white",
            border_radius="16px",
            box_shadow="0 4px 20px rgba(0,0,0,0.1)",
            max_width="400px",
            width="100%",
        ),
        flex="1",
        padding="20px",
    )


def empty_chat_state() -> rx.Component:
    """Show a friendly empty state when no messages or API key setup."""
    return rx.cond(
        State.has_api_key,
        # Has API key - show chat prompt
        rx.center(
            rx.vstack(
                rx.icon("message-circle", size=64, color="#ccc"),
                rx.heading("Start a conversation", size="5", color="#999"),
                rx.text(
                    "Ask me anything! I can help you interact with remote agents.",
                    color="#bbb",
                    size="3",
                    text_align="center",
                ),
                spacing="3",
                align="center",
                padding="40px",
            ),
            flex="1",
        ),
        # No API key - show setup
        api_key_setup(),
    )



def chat_messages() -> rx.Component:
    """Render the chat message list with typing indicator."""
    return rx.box(
        rx.cond(
            State.messages.length() > 0,
            rx.box(
                rx.foreach(
                    State.messages,
                    message_bubble,
                ),
                typing_indicator(),
                width="100%",
            ),
            empty_chat_state(),
        ),
        flex="1",
        overflow_y="auto",
        padding="20px",
        background="linear-gradient(180deg, #fafafa 0%, #f5f5f5 100%)",
    )


def chat_header() -> rx.Component:
    """Render the chat header with improved styling."""
    return rx.box(
        rx.hstack(
            rx.heading(
                "A2A Chat",
                size="5",
                color="white",
            ),
            rx.spacer(),
            rx.button(
                rx.icon("plus", size=16),
                "New Chat",
                on_click=State.new_conversation,
                size="2",
                variant="ghost",
                color="white",
                style={
                    "opacity": "0.9",
                    "_hover": {"opacity": "1", "background": "rgba(255,255,255,0.1)"},
                },
            ),
            width="100%",
            align="center",
        ),
        padding="16px 20px",
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        box_shadow="0 2px 10px rgba(102,126,234,0.3)",
    )


def chat_container() -> rx.Component:
    """Main chat container component with all improvements."""
    return rx.box(
        # CSS for animations
        rx.html("""
            <style>
                @keyframes fadeInUp {
                    from {
                        opacity: 0;
                        transform: translateY(10px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                @keyframes bounce {
                    0%, 80%, 100% {
                        transform: scale(0);
                    }
                    40% {
                        transform: scale(1);
                    }
                }
            </style>
        """),
        error_banner(),
        chat_header(),
        chat_messages(),
        chat_input(),
        display="flex",
        flex_direction="column",
        height="100vh",
        width="100%",
        on_mount=State.load_from_storage,  # Load messages from localStorage
    )
