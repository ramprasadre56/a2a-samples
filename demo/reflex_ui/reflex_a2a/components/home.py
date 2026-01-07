"""Copilot-style landing page component for the A2A Demo."""
import reflex as rx
from reflex_google_auth import google_login
from ..state import State


def nav_link(text: str, href: str) -> rx.Component:
    """Navigation link item."""
    return rx.link(
        rx.text(
            text,
            size="2",
            color="#64748b",
            weight="medium",
        ),
        href=href,
        style={
            "text_decoration": "none",
            "_hover": {
                "color": "#667eea",
            },
            "transition": "color 0.2s ease",
        },
    )


def dropdown_nav(text: str) -> rx.Component:
    """Dropdown navigation item with chevron."""
    return rx.hstack(
        rx.text(
            text,
            size="2",
            color="#64748b",
            weight="medium",
        ),
        rx.icon("chevron-down", size=14, color="#94a3b8"),
        spacing="1",
        align="center",
        cursor="pointer",
        style={
            "_hover": {
                "color": "#667eea",
            },
            "transition": "color 0.2s ease",
        },
    )


def google_sign_in_button() -> rx.Component:
    """Google Sign-in button using real OAuth via reflex-google-auth."""
    return rx.box(
        google_login(
            on_success=State.on_success,
        ),
        # Style wrapper to match the design
    )


def header_navigation() -> rx.Component:
    """Website-style header navigation like Microsoft Copilot."""
    return rx.box(
        rx.hstack(
            # Left side - Logo and brand
            rx.hstack(
                rx.hstack(
                    rx.icon("sparkles", size=20, color="#667eea"),
                    spacing="0",
                ),
                rx.box(
                    width="1px",
                    height="24px",
                    background="#e2e8f0",
                    margin_x="16px",
                ),
                rx.heading(
                    "A2A Copilot",
                    size="4",
                    weight="bold",
                    color="#1e293b",
                ),
                spacing="3",
                align="center",
            ),
            
            # Center - Navigation links
            rx.hstack(
                dropdown_nav("How it works"),
                nav_link("Features", "#features"),
                dropdown_nav("Learn how to use it"),
                nav_link("Documentation", "https://a2a-protocol.org/latest/"),
                dropdown_nav("More"),
                spacing="6",
                align="center",
                display=rx.breakpoints({"0px": "none", "768px": "flex"}),
            ),
            
            rx.spacer(),
            
            # Right side - CTA buttons and Auth
            rx.hstack(
                rx.link(
                    rx.button(
                        "Open Copilot Chat",
                        size="2",
                        style={
                            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                            "color": "white",
                            "font_weight": "600",
                            "cursor": "pointer",
                        },
                    ),
                    href="/chat",
                ),
                rx.link(
                    rx.button(
                        "View Agents",
                        size="2",
                        variant="outline",
                        style={
                            "border_color": "#667eea",
                            "color": "#667eea",
                        },
                    ),
                    href="/agents",
                ),
                rx.box(
                    width="1px",
                    height="24px",
                    background="#e2e8f0",
                    margin_x="8px",
                    display=rx.breakpoints({"0px": "none", "768px": "block"}),
                ),
                # Auth section - Shows login button or user menu
                rx.cond(
                    State.is_logged_in,
                    # Logged in - show user menu with avatar
                    rx.popover.root(
                        rx.popover.trigger(
                            rx.hstack(
                                rx.cond(
                                    State.user_picture != "",
                                    rx.avatar(
                                        src=State.user_picture,
                                        size="2",
                                        radius="full",
                                        style={
                                            "cursor": "pointer",
                                        },
                                    ),
                                    rx.avatar(
                                        fallback=State.user_avatar,
                                        size="2",
                                        radius="full",
                                        style={
                                            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                            "cursor": "pointer",
                                        },
                                    ),
                                ),
                                rx.icon("chevron-down", size=14, color="#64748b"),
                                spacing="1",
                                align="center",
                                cursor="pointer",
                            ),
                        ),
                        rx.popover.content(
                            rx.vstack(
                                rx.hstack(
                                    rx.cond(
                                        State.user_picture != "",
                                        rx.avatar(
                                            src=State.user_picture,
                                            size="3",
                                        ),
                                        rx.avatar(
                                            fallback=State.user_avatar,
                                            size="3",
                                            style={
                                                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                            },
                                        ),
                                    ),
                                    rx.vstack(
                                        rx.text(State.user_name, weight="bold", size="2"),
                                        rx.text(State.user_email, color="#64748b", size="1"),
                                        align="start",
                                        spacing="0",
                                    ),
                                    spacing="3",
                                    align="center",
                                    width="100%",
                                ),
                                rx.divider(),
                                rx.button(
                                    rx.icon("log-out", size=16),
                                    "Sign out",
                                    variant="ghost",
                                    color_scheme="gray",
                                    width="100%",
                                    size="2",
                                    on_click=State.sign_out,
                                ),
                                spacing="3",
                                padding="4px",
                                width="200px",
                            ),
                        ),
                    ),
                    # Not logged in - show real Google sign-in button
                    google_sign_in_button(),
                ),
                spacing="3",
                align="center",
            ),
            
            width="100%",
            max_width="1400px",
            margin="0 auto",
            padding_x="24px",
            align="center",
        ),
        width="100%",
        padding_y="12px",
        background="rgba(255, 255, 255, 0.95)",
        backdrop_filter="blur(10px)",
        border_bottom="1px solid #e2e8f0",
        position="sticky",
        top="0",
        z_index="100",
    )


def feature_card(icon: str, title: str, description: str, gradient: str) -> rx.Component:
    """A feature card in Copilot style with gradient icon background."""
    return rx.box(
        rx.vstack(
            # Icon with gradient background
            rx.box(
                rx.center(
                    rx.icon(icon, size=32, color="white"),
                    width="64px",
                    height="64px",
                    border_radius="16px",
                    background=gradient,
                    box_shadow=f"0 8px 24px {gradient.split()[0].replace('linear-gradient(135deg,', '')}40",
                ),
            ),
            rx.heading(
                title,
                size="5",
                weight="bold",
                color="#1e293b",
                text_align="center",
            ),
            rx.text(
                description,
                color="#64748b",
                size="3",
                text_align="center",
                line_height="1.6",
            ),
            spacing="4",
            align="center",
            padding="32px 24px",
            width="100%",
        ),
        background="white",
        border_radius="20px",
        border="1px solid #e2e8f0",
        box_shadow="0 4px 20px rgba(0, 0, 0, 0.04)",
        flex="1",
        min_width="280px",
        max_width="340px",
        style={
            "_hover": {
                "transform": "translateY(-6px)",
                "box_shadow": "0 12px 40px rgba(102, 126, 234, 0.12)",
                "border_color": "#667eea",
            },
            "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        },
    )


def hero_section() -> rx.Component:
    """Hero section with Copilot-style design."""
    return rx.center(
        rx.vstack(
            # Badge
            rx.box(
                rx.hstack(
                    rx.icon("sparkles", size=14, color="#667eea"),
                    rx.text("Powered by A2A Protocol", size="2", weight="medium", color="#667eea"),
                    spacing="2",
                    align="center",
                ),
                background="rgba(102, 126, 234, 0.1)",
                padding="8px 16px",
                border_radius="full",
            ),
            # Main heading
            rx.heading(
                "Welcome to ",
                rx.text.span("A2A Copilot", color="#667eea"),
                size="9",
                weight="bold",
                color="#1e293b",
                text_align="center",
                style={
                    "letter_spacing": "-0.02em",
                    "line_height": "1.1",
                },
            ),
            # Subtitle
            rx.text(
                "Your AI-powered assistant for orchestrating multiple agents. Chat naturally and let the host agent route your requests to specialized agents.",
                color="#64748b",
                size="4",
                text_align="center",
                max_width="600px",
                line_height="1.7",
            ),
            # CTA Buttons
            rx.hstack(
                rx.link(
                    rx.button(
                        rx.icon("message-circle", size=20),
                        "Start Chatting",
                        size="4",
                        style={
                            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                            "color": "white",
                            "font_weight": "600",
                            "padding": "14px 32px",
                            "box_shadow": "0 8px 24px rgba(102, 126, 234, 0.35)",
                            "cursor": "pointer",
                            "_hover": {
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 12px 32px rgba(102, 126, 234, 0.45)",
                            },
                            "transition": "all 0.2s ease",
                        },
                    ),
                    href="/chat",
                ),
                rx.link(
                    rx.button(
                        rx.icon("users", size=20),
                        "Manage Agents",
                        size="4",
                        variant="outline",
                        style={
                            "border": "2px solid #e2e8f0",
                            "color": "#64748b",
                            "padding": "14px 32px",
                            "_hover": {
                                "background": "#f8fafc",
                                "border_color": "#667eea",
                                "color": "#667eea",
                            },
                        },
                    ),
                    href="/agents",
                ),
                spacing="4",
            ),
            spacing="6",
            align="center",
            padding="60px 24px",
            max_width="800px",
        ),
        width="100%",
        min_height="60vh",
        background="linear-gradient(180deg, #f8fafc 0%, #ffffff 100%)",
    )


def features_section() -> rx.Component:
    """Features section with Copilot-style cards."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "How It Works",
                size="7",
                weight="bold",
                color="#1e293b",
            ),
            rx.text(
                "A2A enables seamless AI agent collaboration",
                color="#64748b",
                size="4",
            ),
            rx.hstack(
                feature_card(
                    "network",
                    "Orchestrate Agents",
                    "From quick tasks to complex workflows—your host agent intelligently routes requests to the right specialized agents.",
                    "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                ),
                feature_card(
                    "zap",
                    "Skip the Busywork",
                    "Agents can summarize, analyze, and automate, so you can focus on what matters most.",
                    "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
                ),
                feature_card(
                    "lightbulb",
                    "Smart Suggestions",
                    "Not sure what to ask? The system offers helpful prompts to guide your next move and spark ideas.",
                    "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
                ),
                spacing="6",
                wrap="wrap",
                justify="center",
                width="100%",
            ),
            spacing="8",
            align="center",
            width="100%",
            max_width="1100px",
            padding="80px 24px",
        ),
        background="#fafafa",
        width="100%",
        display="flex",
        justify_content="center",
    )


def language_badge(lang: str, color: str) -> rx.Component:
    """A badge showing a supported programming language."""
    return rx.box(
        rx.text(lang, size="2", weight="bold", color="white"),
        background=color,
        padding="8px 16px",
        border_radius="full",
        box_shadow=f"0 4px 12px {color}40",
    )


def multi_language_section() -> rx.Component:
    """Section explaining multi-language agent support."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("globe", size=32, color="#667eea"),
                rx.heading(
                    "Multi-Language Agent Support",
                    size="7",
                    weight="bold",
                    color="#1e293b",
                ),
                spacing="3",
                align="center",
            ),
            rx.text(
                "The A2A protocol is language-agnostic. Connect agents written in any programming language!",
                color="#64748b",
                size="4",
                text_align="center",
                max_width="700px",
            ),
            rx.hstack(
                language_badge("Python", "#3776ab"),
                language_badge("JavaScript", "#f7df1e"),
                language_badge("Go", "#00add8"),
                language_badge("Java", "#ed8b00"),
                language_badge(".NET", "#512bd4"),
                spacing="3",
                wrap="wrap",
                justify="center",
            ),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon("check-circle", size=20, color="#22c55e"),
                        rx.text(
                            "Any agent implementing A2A can connect",
                            color="#334155",
                            size="3",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.hstack(
                        rx.icon("check-circle", size=20, color="#22c55e"),
                        rx.text(
                            "Mix Python, JavaScript, Go agents in one system",
                            color="#334155",
                            size="3",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.hstack(
                        rx.icon("check-circle", size=20, color="#22c55e"),
                        rx.text(
                            "Protocol-based communication over HTTP",
                            color="#334155",
                            size="3",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.hstack(
                        rx.icon("check-circle", size=20, color="#22c55e"),
                        rx.text(
                            "Register remote agents by URL",
                            color="#334155",
                            size="3",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    spacing="3",
                    align="start",
                ),
                background="white",
                padding="24px 32px",
                border_radius="16px",
                border="1px solid #e2e8f0",
                box_shadow="0 4px 16px rgba(0, 0, 0, 0.04)",
                margin_top="20px",
            ),
            rx.link(
                rx.box(
                    rx.hstack(
                        rx.icon("plus-circle", size=20, color="#667eea"),
                        rx.text(
                            "Register your remote agent and start testing with the host agent",
                            color="#667eea",
                            size="3",
                            weight="medium",
                        ),
                        rx.icon("arrow-right", size=16, color="#667eea"),
                        spacing="2",
                        align="center",
                        justify="center",
                    ),
                    background="rgba(102, 126, 234, 0.1)",
                    padding="16px 24px",
                    border_radius="12px",
                    margin_top="16px",
                    cursor="pointer",
                    style={
                        "_hover": {
                            "background": "rgba(102, 126, 234, 0.2)",
                        },
                        "transition": "all 0.2s ease",
                    },
                ),
                href="/agents",
            ),
            spacing="6",
            align="center",
            width="100%",
            max_width="800px",
            padding="80px 24px",
        ),
        background="white",
        width="100%",
        display="flex",
        justify_content="center",
    )


def quick_actions() -> rx.Component:
    """Quick action buttons section."""
    return rx.box(
        rx.vstack(
            rx.heading(
                "Quick Actions",
                size="6",
                weight="bold",
                color="#1e293b",
            ),
            rx.grid(
                rx.box(
                    rx.hstack(
                        rx.icon("message-square-plus", size=24, color="#667eea"),
                        rx.vstack(
                            rx.text("New Conversation", weight="bold", color="#1e293b"),
                            rx.text("Start chatting with your agents", size="2", color="#64748b"),
                            align="start",
                            spacing="0",
                        ),
                        spacing="4",
                        align="center",
                    ),
                    padding="20px",
                    background="white",
                    border_radius="16px",
                    border="1px solid #e2e8f0",
                    cursor="pointer",
                    style={
                        "_hover": {
                            "border_color": "#667eea",
                            "box_shadow": "0 4px 16px rgba(102, 126, 234, 0.1)",
                        },
                        "transition": "all 0.2s ease",
                    },
                ),
                rx.box(
                    rx.hstack(
                        rx.icon("plus-circle", size=24, color="#10b981"),
                        rx.vstack(
                            rx.text("Add Agent", weight="bold", color="#1e293b"),
                            rx.text("Register a new remote agent", size="2", color="#64748b"),
                            align="start",
                            spacing="0",
                        ),
                        spacing="4",
                        align="center",
                    ),
                    padding="20px",
                    background="white",
                    border_radius="16px",
                    border="1px solid #e2e8f0",
                    cursor="pointer",
                    style={
                        "_hover": {
                            "border_color": "#10b981",
                            "box_shadow": "0 4px 16px rgba(16, 185, 129, 0.1)",
                        },
                        "transition": "all 0.2s ease",
                    },
                ),
                rx.link(
                    rx.box(
                        rx.hstack(
                            rx.icon("book-open", size=24, color="#f59e0b"),
                            rx.vstack(
                                rx.text("Documentation", weight="bold", color="#1e293b"),
                                rx.text("Learn about A2A protocol", size="2", color="#64748b"),
                                align="start",
                                spacing="0",
                            ),
                            spacing="4",
                            align="center",
                        ),
                        padding="20px",
                        background="white",
                        border_radius="16px",
                        border="1px solid #e2e8f0",
                        cursor="pointer",
                        style={
                            "_hover": {
                                "border_color": "#f59e0b",
                                "box_shadow": "0 4px 16px rgba(245, 158, 11, 0.1)",
                            },
                            "transition": "all 0.2s ease",
                        },
                    ),
                    href="https://a2a-protocol.org/latest/",
                    is_external=True,
                    style={"text_decoration": "none"},
                ),
                columns="3",
                spacing="4",
                width="100%",
            ),
            spacing="6",
            align="center",
            width="100%",
            max_width="900px",
            padding="60px 24px",
        ),
        background="white",
        width="100%",
        display="flex",
        justify_content="center",
    )


def footer() -> rx.Component:
    """Footer section with gradient background."""
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.icon("sparkles", size=20, color="white"),
                rx.heading("A2A Copilot", size="4", color="white"),
                spacing="2",
                align="center",
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
                    href="https://a2a-protocol.org/latest/",
                    is_external=True,
                ),
                spacing="6",
            ),
            width="100%",
            max_width="1100px",
            padding="32px 24px",
        ),
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        width="100%",
        display="flex",
        justify_content="center",
    )


def landing_page() -> rx.Component:
    """Complete Copilot-style landing page component."""
    return rx.box(
        header_navigation(),
        hero_section(),
        features_section(),
        multi_language_section(),
        quick_actions(),
        footer(),
        display="flex",
        flex_direction="column",
        min_height="100vh",
        width="100%",
    )

