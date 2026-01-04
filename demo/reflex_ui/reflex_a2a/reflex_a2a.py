"""Main Reflex app for A2A Demo."""
import reflex as rx
from .state import State
from .components.chat import chat_container
from .components.agent_list import agent_list_container
from .components.home import landing_page


def sidebar() -> rx.Component:
    """Navigation sidebar."""
    return rx.box(
        rx.vstack(
            rx.link(
                rx.heading(
                    "A2A Demo",
                    size="4",
                    color="white",
                ),
                href="/",
                style={"text_decoration": "none"},
            ),
            rx.box(height="24px"),
            rx.link(
                rx.hstack(
                    rx.icon("message-circle", size=20),
                    rx.text("Chat", size="3"),
                    spacing="3",
                    align="center",
                    width="100%",
                    padding="12px 16px",
                    border_radius="8px",
                    _hover={"background": "rgba(255,255,255,0.1)"},
                ),
                href="/chat",
                style={"text_decoration": "none", "color": "white"},
            ),
            rx.link(
                rx.hstack(
                    rx.icon("users", size=20),
                    rx.text("Agents", size="3"),
                    spacing="3",
                    align="center",
                    width="100%",
                    padding="12px 16px",
                    border_radius="8px",
                    _hover={"background": "rgba(255,255,255,0.1)"},
                ),
                href="/agents",
                style={"text_decoration": "none", "color": "white"},
            ),
            rx.spacer(),
            rx.text(
                "Powered by Reflex",
                color="rgba(255,255,255,0.5)",
                font_size="12px",
            ),
            height="100%",
            padding="20px",
            align="start",
        ),
        width="220px",
        background="linear-gradient(180deg, #667eea 0%, #764ba2 100%)",
        height="100vh",
        flex_shrink="0",
    )


def index() -> rx.Component:
    """Landing page (home)."""
    return landing_page()


def chat_page() -> rx.Component:
    """Chat page."""
    return rx.hstack(
        sidebar(),
        chat_container(),
        spacing="0",
        width="100%",
        height="100vh",
    )


def agents_page() -> rx.Component:
    """Agents management page."""
    return rx.hstack(
        sidebar(),
        agent_list_container(),
        spacing="0",
        width="100%",
        height="100vh",
    )


# Create the app
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="violet",
        radius="medium",
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
    ],
    style={
        "font_family": "'Inter', sans-serif",
    },
)

# Add pages
app.add_page(index, route="/", title="A2A Demo - AI Agent Communication")
app.add_page(chat_page, route="/chat", title="A2A Chat")
app.add_page(agents_page, route="/agents", title="Remote Agents")
