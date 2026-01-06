"""Copilot-style Chat UI component for the A2A demo."""
import reflex as rx
from ..state import State, Message


def message_bubble(message: Message) -> rx.Component:
    """Render a single message bubble in Copilot style."""
    is_user = message.role == "user"
    
    return rx.box(
        rx.hstack(
            # Avatar for agent messages
            rx.cond(
                ~is_user,
                rx.box(
                    rx.icon("sparkles", size=16, color="white"),
                    background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    padding="8px",
                    border_radius="10px",
                    flex_shrink="0",
                ),
                rx.fragment(),
            ),
            rx.box(
                rx.text(
                    message.content,
                    size="3",
                    white_space="pre-wrap",
                    line_height="1.6",
                ),
                padding="14px 18px",
                background=rx.cond(
                    is_user,
                    "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    "#f8fafc",
                ),
                color=rx.cond(is_user, "white", "#1e293b"),
                border_radius=rx.cond(
                    is_user,
                    "20px 20px 4px 20px",
                    "4px 20px 20px 20px",
                ),
                max_width="75%",
                box_shadow=rx.cond(
                    is_user,
                    "0 4px 16px rgba(102, 126, 234, 0.25)",
                    "0 2px 8px rgba(0, 0, 0, 0.04)",
                ),
                border=rx.cond(is_user, "none", "1px solid #e2e8f0"),
            ),
            # Avatar for user messages
            rx.cond(
                is_user,
                rx.avatar(
                    fallback="U",
                    size="2",
                    radius="full",
                    style={
                        "background": "#e2e8f0",
                        "color": "#64748b",
                    },
                    flex_shrink="0",
                ),
                rx.fragment(),
            ),
            spacing="3",
            justify=rx.cond(is_user, "end", "start"),
            align="end",
            width="100%",
        ),
        width="100%",
        margin_bottom="16px",
        animation="fadeInUp 0.3s ease-out",
    )


def typing_indicator() -> rx.Component:
    """Copilot-style typing indicator."""
    return rx.cond(
        State.is_processing,
        rx.box(
            rx.hstack(
                rx.box(
                    rx.icon("sparkles", size=16, color="white"),
                    background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    padding="8px",
                    border_radius="10px",
                ),
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
                        spacing="2",
                    ),
                    padding="14px 18px",
                    background="#f8fafc",
                    border_radius="4px 20px 20px 20px",
                    border="1px solid #e2e8f0",
                ),
                spacing="3",
                align="end",
            ),
            width="100%",
            margin_bottom="16px",
        ),
        rx.fragment(),
    )


def suggestion_chip(text: str, prompt: str) -> rx.Component:
    """Suggestion chip for quick prompts."""
    return rx.box(
        rx.hstack(
            rx.icon("sparkles", size=14, color="#667eea"),
            rx.text(text, size="2", color="#667eea", weight="medium"),
            spacing="2",
            align="center",
        ),
        padding="10px 16px",
        background="rgba(102, 126, 234, 0.08)",
        border="1px solid rgba(102, 126, 234, 0.2)",
        border_radius="full",
        cursor="pointer",
        on_click=lambda: State.set_current_input(prompt),
        style={
            "_hover": {
                "background": "rgba(102, 126, 234, 0.15)",
                "border_color": "#667eea",
            },
            "transition": "all 0.2s ease",
        },
    )


def empty_chat_state() -> rx.Component:
    """Copilot-style empty state with suggestions."""
    return rx.cond(
        State.has_api_key,
        rx.center(
            rx.vstack(
                rx.box(
                    rx.icon("sparkles", size=48, color="white"),
                    background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    padding="20px",
                    border_radius="24px",
                    box_shadow="0 12px 32px rgba(102, 126, 234, 0.3)",
                ),
                rx.heading(
                    "How can I help you today?",
                    size="6",
                    weight="bold",
                    color="#1e293b",
                ),
                rx.text(
                    "I can route your requests to specialized agents. Try asking me something!",
                    color="#64748b",
                    size="3",
                    text_align="center",
                    max_width="400px",
                ),
                rx.box(height="20px"),
                rx.text("Try these suggestions:", size="2", color="#94a3b8"),
                rx.hstack(
                    suggestion_chip("Convert currency", "Convert 100 USD to EUR"),
                    suggestion_chip("Say hello", "Hello, how are you?"),
                    suggestion_chip("List agents", "What agents are available?"),
                    spacing="3",
                    wrap="wrap",
                    justify="center",
                ),
                spacing="4",
                align="center",
                padding="60px 20px",
            ),
            flex="1",
        ),
        # API key setup
        rx.center(
            rx.box(
                rx.vstack(
                    rx.box(
                        rx.icon("key", size=32, color="white"),
                        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        padding="16px",
                        border_radius="16px",
                    ),
                    rx.heading("Configure API Key", size="5", color="#1e293b"),
                    rx.text(
                        "Enter your Google Gemini API key to start chatting with AI agents.",
                        color="#64748b",
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
                        style={
                            "background": "#f8fafc",
                            "border": "1px solid #e2e8f0",
                        },
                    ),
                    rx.button(
                        rx.icon("check", size=18),
                        "Save API Key",
                        on_click=State.save_api_key,
                        size="3",
                        width="100%",
                        style={
                            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
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
                    padding="40px",
                    width="100%",
                ),
                background="white",
                border_radius="20px",
                box_shadow="0 8px 32px rgba(0, 0, 0, 0.08)",
                border="1px solid #e2e8f0",
                max_width="420px",
                width="100%",
            ),
            flex="1",
            padding="20px",
        ),
    )


def chat_messages() -> rx.Component:
    """Render the chat message list."""
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
                max_width="800px",
                margin="0 auto",
            ),
            empty_chat_state(),
        ),
        flex="1",
        overflow_y="auto",
        padding="24px",
        background="linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)",
    )


def chat_input() -> rx.Component:
    """Copilot-style chat input area."""
    return rx.box(
        rx.box(
            rx.hstack(
                rx.input(
                    placeholder="Ask me anything...",
                    value=State.current_input,
                    on_change=State.set_current_input,
                    flex="1",
                    size="3",
                    radius="full",
                    disabled=State.is_processing,
                    style={
                        "background": "#f8fafc",
                        "border": "1px solid #e2e8f0",
                        "padding_left": "20px",
                        "_focus": {
                            "border_color": "#667eea",
                            "box_shadow": "0 0 0 3px rgba(102, 126, 234, 0.1)",
                        },
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
                        "box_shadow": "0 4px 12px rgba(102, 126, 234, 0.35)",
                        "_hover": {
                            "transform": "scale(1.05)",
                        },
                        "transition": "all 0.2s ease",
                    },
                ),
                width="100%",
                max_width="800px",
                spacing="3",
                margin="0 auto",
            ),
            padding="20px 24px",
            background="white",
            border_top="1px solid #e2e8f0",
        ),
    )


def error_banner() -> rx.Component:
    """Error banner with dismiss button."""
    return rx.cond(
        State.error_message != "",
        rx.box(
            rx.hstack(
                rx.icon("alert-circle", size=18, color="#dc2626"),
                rx.text(State.error_message, color="#dc2626", weight="medium", size="2"),
                rx.spacer(),
                rx.icon_button(
                    rx.icon("x", size=14),
                    on_click=State.clear_error,
                    size="1",
                    variant="ghost",
                    color_scheme="red",
                ),
                width="100%",
                max_width="800px",
                align="center",
                margin="0 auto",
            ),
            padding="12px 24px",
            background="linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)",
            border_bottom="1px solid #fecaca",
        ),
        rx.fragment(),
    )


def chat_container() -> rx.Component:
    """Main Copilot-style chat container."""
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
        chat_messages(),
        chat_input(),
        display="flex",
        flex_direction="column",
        height="100vh",
        width="100%",
        background="#ffffff",
        on_mount=State.load_from_storage,
    )
