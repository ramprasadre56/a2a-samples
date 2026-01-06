"""Main Reflex app for A2A Copilot Demo."""
import reflex as rx
from .state import State
from .components.chat import chat_container
from .components.agent_list import agent_list_container
from .components.home import landing_page
from .components.sidebar import copilot_sidebar


def index() -> rx.Component:
    """Landing page (home)."""
    return landing_page()


def chat_page() -> rx.Component:
    """Chat page with Copilot sidebar."""
    return rx.hstack(
        copilot_sidebar(),
        chat_container(),
        spacing="0",
        width="100%",
        height="100vh",
    )


def agents_page() -> rx.Component:
    """Agents management page with Copilot sidebar."""
    return rx.hstack(
        copilot_sidebar(),
        agent_list_container(),
        spacing="0",
        width="100%",
        height="100vh",
    )


def settings_page() -> rx.Component:
    """Settings page placeholder."""
    return rx.hstack(
        copilot_sidebar(),
        rx.center(
            rx.vstack(
                rx.box(
                    rx.icon("settings", size=48, color="white"),
                    background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    padding="20px",
                    border_radius="24px",
                    box_shadow="0 12px 32px rgba(102, 126, 234, 0.3)",
                ),
                rx.heading(
                    "Settings",
                    size="6",
                    weight="bold",
                    color="#1e293b",
                ),
                rx.text(
                    "Settings page coming soon...",
                    color="#64748b",
                    size="3",
                ),
                spacing="4",
                align="center",
            ),
            flex="1",
            height="100vh",
            background="linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)",
        ),
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
app.add_page(index, route="/", title="A2A Copilot - AI Agent Communication")
app.add_page(chat_page, route="/chat", title="A2A Copilot - Chat")
app.add_page(agents_page, route="/agents", title="A2A Copilot - Agents")
app.add_page(settings_page, route="/settings", title="A2A Copilot - Settings")
