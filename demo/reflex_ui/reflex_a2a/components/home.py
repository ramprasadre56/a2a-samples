"""Landing page component for the A2A Demo."""
import reflex as rx
from ..state import State


def hero_section() -> rx.Component:
    """Hero section with gradient background and main CTA."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "A2A Demo",
                size="9",
                color="white",
                weight="bold",
                style={
                    "text_shadow": "0 2px 20px rgba(0,0,0,0.3)",
                    "letter_spacing": "-0.02em",
                },
            ),
            rx.heading(
                "Experience the Future of AI Agent Communication",
                size="6",
                color="rgba(255,255,255,0.9)",
                weight="medium",
                text_align="center",
                max_width="600px",
            ),
            rx.text(
                "Seamlessly orchestrate multiple AI agents working together. See how agents can communicate, delegate tasks, and collaborate in real-time.",
                color="rgba(255,255,255,0.8)",
                size="4",
                text_align="center",
                max_width="500px",
            ),
            rx.hstack(
                rx.link(
                    rx.button(
                        rx.icon("message-circle", size=20),
                        "Start Chatting",
                        size="4",
                        style={
                            "background": "white",
                            "color": "#667eea",
                            "font_weight": "600",
                            "padding": "12px 32px",
                            "box_shadow": "0 4px 20px rgba(0,0,0,0.2)",
                            "cursor": "pointer",
                            "_hover": {
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 6px 30px rgba(0,0,0,0.3)",
                            },
                            "transition": "all 0.2s ease",
                        },
                    ),
                    href="/chat",
                ),
                rx.link(
                    rx.button(
                        rx.icon("users", size=20),
                        "View Agents",
                        size="4",
                        variant="outline",
                        style={
                            "border": "2px solid rgba(255,255,255,0.5)",
                            "color": "white",
                            "padding": "12px 32px",
                            "_hover": {
                                "background": "rgba(255,255,255,0.1)",
                                "border_color": "white",
                            },
                        },
                    ),
                    href="/agents",
                ),
                spacing="4",
            ),
            spacing="5",
            align="center",
            padding="80px 20px",
        ),
        background="linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)",
        width="100%",
        min_height="500px",
        display="flex",
        align_items="center",
        justify_content="center",
    )


def feature_card(icon: str, title: str, description: str) -> rx.Component:
    """A single feature card."""
    return rx.box(
        rx.vstack(
            rx.box(
                rx.icon(icon, size=32, color="#667eea"),
                padding="16px",
                background="linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%)",
                border_radius="16px",
            ),
            rx.heading(
                title,
                size="5",
                weight="bold",
                color="#333",
            ),
            rx.text(
                description,
                color="#666",
                size="3",
                text_align="center",
            ),
            spacing="3",
            align="center",
            padding="24px",
        ),
        background="white",
        border_radius="20px",
        box_shadow="0 4px 20px rgba(0,0,0,0.08)",
        border="1px solid #f0f0f0",
        flex="1",
        min_width="280px",
        max_width="350px",
        style={
            "_hover": {
                "transform": "translateY(-4px)",
                "box_shadow": "0 8px 30px rgba(102,126,234,0.15)",
            },
            "transition": "all 0.3s ease",
        },
    )


def features_section() -> rx.Component:
    """Features section with 3 cards."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "How It Works",
                size="7",
                weight="bold",
                color="#333",
            ),
            rx.text(
                "A2A (Agent-to-Agent) protocol enables seamless communication between AI agents",
                color="#666",
                size="4",
                text_align="center",
            ),
            rx.hstack(
                feature_card(
                    "network",
                    "Multi-Agent Orchestration",
                    "A host agent intelligently routes requests to specialized agents based on their capabilities.",
                ),
                feature_card(
                    "zap",
                    "Real-time Communication",
                    "Agents communicate instantly using the A2A protocol with JSON-RPC messaging.",
                ),
                feature_card(
                    "puzzle",
                    "Easy Integration",
                    "Register any A2A-compatible agent by simply providing its URL. No complex setup required.",
                ),
                spacing="6",
                wrap="wrap",
                justify="center",
                width="100%",
            ),
            spacing="6",
            align="center",
            width="100%",
            max_width="1200px",
            padding="60px 20px",
        ),
        background="#fafafa",
        width="100%",
        display="flex",
        justify_content="center",
    )


def agents_preview() -> rx.Component:
    """Preview of available agents."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "Pre-Configured Agents",
                size="7",
                weight="bold",
                color="#333",
            ),
            rx.text(
                "These agents are automatically registered and ready to use",
                color="#666",
                size="4",
            ),
            rx.hstack(
                rx.box(
                    rx.hstack(
                        rx.icon("bot", size=24, color="#667eea"),
                        rx.vstack(
                            rx.text("Hello World Agent", weight="bold", color="#333"),
                            rx.text("A simple agent that greets users", size="2", color="#666"),
                            align="start",
                            spacing="1",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    padding="20px",
                    background="white",
                    border_radius="12px",
                    box_shadow="0 2px 10px rgba(0,0,0,0.05)",
                    border="1px solid #eee",
                ),
                rx.box(
                    rx.hstack(
                        rx.icon("coins", size=24, color="#667eea"),
                        rx.vstack(
                            rx.text("Currency Agent", weight="bold", color="#333"),
                            rx.text("Converts currencies using real-time rates", size="2", color="#666"),
                            align="start",
                            spacing="1",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    padding="20px",
                    background="white",
                    border_radius="12px",
                    box_shadow="0 2px 10px rgba(0,0,0,0.05)",
                    border="1px solid #eee",
                ),
                spacing="4",
                wrap="wrap",
                justify="center",
            ),
            spacing="5",
            align="center",
            padding="60px 20px",
        ),
        background="white",
        width="100%",
    )


def footer() -> rx.Component:
    """Footer section."""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.heading("A2A Demo", size="4", color="white"),
                rx.text(
                    "Built with Google ADK & Reflex",
                    color="rgba(255,255,255,0.7)",
                    size="2",
                ),
                align="start",
            ),
            rx.spacer(),
            rx.hstack(
                rx.link(
                    rx.text("GitHub", color="rgba(255,255,255,0.8)"),
                    href="https://github.com/google-a2a/a2a-samples",
                    is_external=True,
                ),
                rx.link(
                    rx.text("Documentation", color="rgba(255,255,255,0.8)"),
                    href="https://google-a2a.github.io/A2A/",
                    is_external=True,
                ),
                spacing="6",
            ),
            width="100%",
            max_width="1200px",
            padding="40px 20px",
        ),
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        width="100%",
        display="flex",
        justify_content="center",
    )


def landing_page() -> rx.Component:
    """Complete landing page component."""
    return rx.box(
        hero_section(),
        features_section(),
        agents_preview(),
        footer(),
        display="flex",
        flex_direction="column",
        min_height="100vh",
        width="100%",
    )
