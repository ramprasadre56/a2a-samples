"""Copilot-style Agent list component for the A2A demo with Microsoft 365-style grid layout."""
import reflex as rx
from ..state import State, Agent


def agent_tile(agent: Agent) -> rx.Component:
    """Render a single agent tile in Microsoft 365 style."""
    return rx.box(
        rx.vstack(
            # Top row - Icon and action buttons
            rx.hstack(
                # Agent icon with gradient background
                rx.box(
                    rx.icon("bot", size=20, color="white"),
                    background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    padding="10px",
                    border_radius="12px",
                    box_shadow="0 4px 12px rgba(102, 126, 234, 0.25)",
                ),
                rx.spacer(),
                # Action buttons (visible on hover via CSS)
                rx.hstack(
                    rx.icon_button(
                        rx.icon("message-circle", size=14),
                        size="1",
                        variant="ghost",
                        color_scheme="gray",
                        radius="full",
                        class_name="action-btn",
                    ),
                    rx.icon_button(
                        rx.icon("trash-2", size=14),
                        size="1",
                        variant="ghost",
                        color_scheme="red",
                        radius="full",
                        on_click=State.remove_agent(agent.url),
                        class_name="action-btn",
                    ),
                    spacing="1",
                    class_name="action-buttons",
                ),
                width="100%",
                align="start",
            ),
            # Agent name
            rx.text(
                agent.name,
                weight="bold",
                size="3",
                color="#1e293b",
                style={
                    "white_space": "nowrap",
                    "overflow": "hidden",
                    "text_overflow": "ellipsis",
                    "max_width": "100%",
                },
            ),
            # Status indicator
            rx.hstack(
                rx.box(
                    width="6px",
                    height="6px",
                    border_radius="50%",
                    background="#22c55e",
                ),
                rx.text("Connected", size="1", color="#22c55e", weight="medium"),
                spacing="1",
                align="center",
            ),
            # Description
            rx.text(
                agent.description,
                color="#64748b",
                size="1",
                line_height="1.5",
                style={
                    "display": "-webkit-box",
                    "-webkit-line-clamp": "2",
                    "-webkit-box-orient": "vertical",
                    "overflow": "hidden",
                    "min_height": "36px",
                },
            ),
            # URL/Link row
            rx.hstack(
                rx.icon("link", size=12, color="#94a3b8"),
                spacing="1",
                align="center",
                style={"margin_top": "auto"},
            ),
            align="start",
            spacing="2",
            width="100%",
            height="100%",
        ),
        padding="16px",
        background="white",
        border_radius="12px",
        border="1px solid #e2e8f0",
        min_height="180px",
        style={
            "_hover": {
                "border_color": "#cbd5e1",
                "box_shadow": "0 4px 16px rgba(0, 0, 0, 0.08)",
                "& .action-buttons": {
                    "opacity": "1",
                },
            },
            "transition": "all 0.2s ease",
            "& .action-buttons": {
                "opacity": "0.4",
                "transition": "opacity 0.2s ease",
            },
        },
    )


def add_agent_dialog() -> rx.Component:
    """Dialog for adding a new agent with improved styling."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=16),
                "Add Agent",
                size="2",
                style={
                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    "box_shadow": "0 4px 12px rgba(102, 126, 234, 0.3)",
                },
            ),
        ),
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.icon("plus-circle", size=20, color="white"),
                        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        padding="10px",
                        border_radius="12px",
                    ),
                    rx.dialog.title("Add Remote Agent", size="5"),
                    spacing="3",
                    align="center",
                ),
                rx.dialog.description(
                    "Enter the URL of the A2A-compatible agent you want to register. The agent must be running and accessible.",
                    size="2",
                    color="#64748b",
                ),
                rx.box(
                    rx.input(
                        placeholder="http://localhost:9999",
                        value=State.new_agent_url,
                        on_change=State.set_new_agent_url,
                        width="100%",
                        size="3",
                        style={
                            "background": "#f8fafc",
                            "border": "1px solid #e2e8f0",
                        },
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            color_scheme="gray",
                            size="2",
                        ),
                    ),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("check", size=16),
                            "Register Agent",
                            on_click=State.register_agent,
                            size="2",
                            style={
                                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                            },
                        ),
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                ),
                spacing="5",
                width="100%",
            ),
            style={"max_width": "480px", "padding": "28px"},
        ),
    )


def agents_header() -> rx.Component:
    """Header for the agents page in Microsoft 365 style."""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.heading(
                    "Remote Agents",
                    size="6",
                    weight="bold",
                    color="#1e293b",
                ),
                rx.text(
                    "Manage your connected A2A agents",
                    size="2",
                    color="#64748b",
                ),
                align="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.hstack(
                rx.button(
                    rx.icon("refresh-cw", size=16),
                    "Refresh",
                    on_click=State.refresh_agents,
                    size="2",
                    variant="soft",
                    color_scheme="gray",
                ),
                add_agent_dialog(),
                spacing="3",
            ),
            width="100%",
            align="center",
        ),
        padding="24px",
        background="white",
        border_bottom="1px solid #e2e8f0",
    )


def empty_agents_state() -> rx.Component:
    """Empty state when no agents are registered."""
    return rx.center(
        rx.vstack(
            rx.box(
                rx.icon("users", size=40, color="white"),
                background="linear-gradient(135deg, #94a3b8 0%, #64748b 100%)",
                padding="20px",
                border_radius="20px",
                box_shadow="0 8px 24px rgba(100, 116, 139, 0.2)",
            ),
            rx.heading(
                "No agents connected",
                size="5",
                color="#64748b",
            ),
            rx.text(
                "Add your first remote agent to get started.",
                color="#94a3b8",
                size="3",
            ),
            rx.box(height="8px"),
            add_agent_dialog(),
            spacing="4",
            align="center",
        ),
        flex="1",
        padding="60px",
    )


def agent_grid() -> rx.Component:
    """Grid of agent tiles in Microsoft 365 style."""
    return rx.box(
        rx.cond(
            State.agents.length() > 0,
            rx.box(
                rx.foreach(State.agents, agent_tile),
                display="grid",
                grid_template_columns="repeat(auto-fill, minmax(240px, 1fr))",
                gap="16px",
                width="100%",
                max_width="1200px",
            ),
            empty_agents_state(),
        ),
        flex="1",
        overflow_y="auto",
        padding="24px",
        background="linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%)",
    )


def agent_list_container() -> rx.Component:
    """Main container for the agent list page."""
    return rx.box(
        agents_header(),
        agent_grid(),
        display="flex",
        flex_direction="column",
        height="100vh",
        width="100%",
        background="#f8fafc",
        on_mount=State.refresh_agents,
    )
