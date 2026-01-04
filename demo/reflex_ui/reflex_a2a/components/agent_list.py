"""Agent list component for the A2A demo."""
import reflex as rx
from ..state import State, Agent


def agent_card(agent: Agent) -> rx.Component:
    """Render a single agent card."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("bot", size=24, color="#667eea"),
                rx.text(
                    agent.name,
                    font_weight="bold",
                    size="4",
                ),
                align="center",
                spacing="2",
            ),
            rx.text(
                agent.description,
                color="#666",
                size="2",
            ),
            rx.text(
                agent.url,
                font_family="monospace",
                font_size="12px",
                color="#999",
            ),
            align="start",
            spacing="2",
            width="100%",
        ),
        padding="16px",
        background="white",
        border_radius="12px",
        box_shadow="0 2px 8px rgba(0,0,0,0.08)",
        border="1px solid #eee",
        width="100%",
    )


def add_agent_dialog() -> rx.Component:
    """Dialog for adding a new agent."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=16),
                "Add Agent",
                size="2",
                style={
                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                },
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("Add Remote Agent"),
            rx.dialog.description(
                "Enter the URL of the remote agent to register.",
                size="2",
                margin_bottom="16px",
            ),
            rx.input(
                placeholder="http://localhost:9999",
                value=State.new_agent_url,
                on_change=State.set_new_agent_url,
                width="100%",
                size="3",
            ),
            rx.hstack(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        color_scheme="gray",
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Register",
                        on_click=State.register_agent,
                        style={
                            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        },
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
                width="100%",
            ),
            style={"max_width": "450px"},
        ),
    )


def agents_header() -> rx.Component:
    """Header for the agents page."""
    return rx.box(
        rx.hstack(
            rx.heading(
                "Remote Agents",
                size="5",
                color="white",
            ),
            rx.spacer(),
            add_agent_dialog(),
            width="100%",
            align="center",
        ),
        padding="16px 20px",
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    )


def agent_list_container() -> rx.Component:
    """Container for the agent list."""
    return rx.box(
        agents_header(),
        rx.box(
            rx.cond(
                State.agents.length() > 0,
                rx.vstack(
                    rx.foreach(State.agents, agent_card),
                    spacing="4",
                    width="100%",
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("users", size=48, color="#ccc"),
                        rx.text(
                            "No agents registered",
                            color="#999",
                            size="3",
                        ),
                        rx.text(
                            "Click 'Add Agent' to register a remote agent",
                            color="#bbb",
                            size="2",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    padding="60px",
                ),
            ),
            padding="20px",
            flex="1",
            overflow_y="auto",
            background="#fafafa",
        ),
        display="flex",
        flex_direction="column",
        height="100vh",
        width="100%",
        on_mount=State.refresh_agents,
    )
