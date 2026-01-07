"""Copilot-style sidebar component for A2A Demo."""
import reflex as rx
from ..state import State, Agent


def nav_item(icon: str, label: str, nav_key: str, href: str) -> rx.Component:
    """A single navigation item with active state styling."""
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=20, color="inherit"),
            rx.cond(
                ~State.sidebar_collapsed,
                rx.text(label, size="3", weight="medium"),
                rx.fragment(),
            ),
            spacing="3",
            align="center",
            width="100%",
            padding="12px 16px",
            border_radius="10px",
            background=rx.cond(
                State.active_nav == nav_key,
                "rgba(102, 126, 234, 0.15)",
                "transparent",
            ),
            color=rx.cond(
                State.active_nav == nav_key,
                "#667eea",
                "#64748b",
            ),
            _hover={
                "background": "rgba(102, 126, 234, 0.1)",
                "color": "#667eea",
            },
            transition="all 0.2s ease",
        ),
        href=href,
        on_click=State.set_active_nav(nav_key),
        style={"text_decoration": "none", "width": "100%"},
    )


def agent_mini_card(agent: Agent) -> rx.Component:
    """Mini agent card for sidebar."""
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon("bot", size=16, color="white"),
                background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                padding="6px",
                border_radius="8px",
            ),
            rx.cond(
                ~State.sidebar_collapsed,
                rx.vstack(
                    rx.text(
                        agent.name,
                        size="2",
                        weight="medium",
                        color="#334155",
                        style={"white_space": "nowrap", "overflow": "hidden", "text_overflow": "ellipsis"},
                    ),
                    rx.hstack(
                        rx.box(
                            width="6px",
                            height="6px",
                            border_radius="50%",
                            background="#22c55e",
                        ),
                        rx.text("Connected", size="1", color="#94a3b8"),
                        spacing="1",
                        align="center",
                    ),
                    align="start",
                    spacing="0",
                    flex="1",
                    overflow="hidden",
                ),
                rx.fragment(),
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        padding="10px 12px",
        background="white",
        border_radius="10px",
        border="1px solid #e2e8f0",
        width="100%",
        style={
            "_hover": {
                "border_color": "#667eea",
                "box_shadow": "0 2px 8px rgba(102, 126, 234, 0.15)",
            },
            "transition": "all 0.2s ease",
            "cursor": "pointer",
        },
    )


def agents_section() -> rx.Component:
    """Sidebar section showing connected agents."""
    return rx.cond(
        ~State.sidebar_collapsed,
        rx.box(
            rx.hstack(
                rx.text("AGENTS", size="1", weight="bold", color="#94a3b8"),
                rx.spacer(),
                rx.text(
                    State.agents.length(),
                    size="1",
                    color="#667eea",
                    weight="bold",
                ),
                width="100%",
                padding_x="16px",
            ),
            rx.cond(
                State.agents.length() > 0,
                rx.vstack(
                    rx.foreach(State.agents, agent_mini_card),
                    spacing="2",
                    width="100%",
                    padding="8px 12px",
                ),
                rx.center(
                    rx.text("No agents connected", size="1", color="#94a3b8"),
                    padding="20px",
                ),
            ),
            width="100%",
            margin_top="16px",
        ),
        rx.fragment(),
    )


def user_profile() -> rx.Component:
    """User profile section at bottom of sidebar."""
    return rx.box(
        rx.hstack(
            rx.avatar(
                fallback=rx.cond(State.is_logged_in, State.user_avatar, "U"),
                size="2",
                radius="full",
                style={
                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                },
            ),
            rx.cond(
                ~State.sidebar_collapsed,
                rx.vstack(
                    rx.text(
                        rx.cond(State.is_logged_in, State.user_name, "Guest User"),
                        size="2",
                        weight="medium",
                        color="#334155",
                    ),
                    rx.text(
                        rx.cond(State.is_logged_in, State.user_email, "Not signed in"),
                        size="1",
                        color="#94a3b8",
                    ),
                    align="start",
                    spacing="0",
                ),
                rx.fragment(),
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        padding="16px",
        border_top="1px solid #e2e8f0",
        width="100%",
    )


def copilot_sidebar() -> rx.Component:
    """Main Copilot-style sidebar component."""
    return rx.box(
        rx.vstack(
            # Logo and collapse button
            rx.hstack(
                rx.link(
                    rx.hstack(
                        rx.box(
                            rx.icon("sparkles", size=24, color="white"),
                            background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                            padding="8px",
                            border_radius="12px",
                        ),
                        rx.cond(
                            ~State.sidebar_collapsed,
                            rx.heading(
                                "A2A Copilot",
                                size="4",
                                weight="bold",
                                color="#1e293b",
                            ),
                            rx.fragment(),
                        ),
                        spacing="3",
                        align="center",
                    ),
                    href="/",
                    on_click=State.set_active_nav("chat"),
                    style={"text_decoration": "none", "cursor": "pointer"},
                ),
                rx.cond(
                    ~State.sidebar_collapsed,
                    rx.spacer(),
                    rx.fragment(),
                ),
                rx.icon_button(
                    rx.cond(
                        State.sidebar_collapsed,
                        rx.icon("panel-left", size=18),
                        rx.icon("panel-left-close", size=18),
                    ),
                    on_click=State.toggle_sidebar,
                    variant="ghost",
                    size="2",
                    color_scheme="gray",
                ),
                width="100%",
                align="center",
                padding="16px",
                justify=rx.cond(State.sidebar_collapsed, "center", "start"),
            ),
            
            # Search input (when expanded)
            rx.cond(
                ~State.sidebar_collapsed,
                rx.box(
                    rx.input(
                        rx.input.slot(
                            rx.icon("search", size=16, color="#94a3b8"),
                        ),
                        placeholder="Search...",
                        size="2",
                        radius="large",
                        width="100%",
                        style={
                            "background": "#f8fafc",
                            "border": "1px solid #e2e8f0",
                            "color": "#1e293b",
                        },
                    ),
                    padding_x="16px",
                    width="100%",
                ),
                rx.fragment(),
            ),
            
            # Navigation items
            rx.vstack(
                nav_item("message-circle", "Chat", "chat", "/chat"),
                nav_item("users", "Agents", "agents", "/agents"),
                nav_item("settings", "Settings", "settings", "/settings"),
                spacing="1",
                width="100%",
                padding="16px 12px",
            ),
            
            # Connected agents section
            agents_section(),
            
            rx.spacer(),
            
            # User profile at bottom
            user_profile(),
            
            height="100%",
            width="100%",
            align="start",
            spacing="0",
        ),
        width=rx.cond(State.sidebar_collapsed, "72px", "260px"),
        min_width=rx.cond(State.sidebar_collapsed, "72px", "260px"),
        height="100vh",
        background="white",
        border_right="1px solid #e2e8f0",
        box_shadow="2px 0 8px rgba(0, 0, 0, 0.03)",
        flex_shrink="0",
        transition="width 0.3s ease, min-width 0.3s ease",
        overflow="hidden",
        on_mount=State.refresh_agents,
    )
