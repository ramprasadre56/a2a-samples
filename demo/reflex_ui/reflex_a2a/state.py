"""Reflex state management for A2A demo with integrated Host Agent."""
import reflex as rx
from typing import List, Optional
import asyncio
import uuid
import json
from pydantic import BaseModel as PydanticBaseModel

from .host_agent_service import get_host_agent_service


class Message(PydanticBaseModel):
    """Model for a chat message."""
    id: str
    role: str  # "user" or "agent"
    content: str
    context_id: Optional[str] = None


class Agent(PydanticBaseModel):
    """Model for a registered agent."""
    name: str
    description: str
    url: str


class State(rx.State):
    """The main application state with integrated Host Agent."""
    
    # Chat state
    messages: List[Message] = []
    current_input: str = ""
    is_processing: bool = False
    context_id: Optional[str] = None
    
    # Agent state
    agents: List[Agent] = []
    new_agent_url: str = ""
    new_agent_auth_type: str = "none"  # "none", "api_key", "bearer_token"
    new_agent_auth_value: str = ""
    new_agent_custom_headers: str = ""  # JSON string
    show_agent_dialog: bool = False
    show_advanced_options: bool = False
    
    # UI state - Copilot style
    sidebar_collapsed: bool = False
    selected_agent_id: Optional[str] = None
    active_nav: str = "chat"  # "chat", "agents", "settings"
    
    # Auth state - Google Sign-in
    is_logged_in: bool = False
    user_name: str = ""
    user_email: str = ""
    user_avatar: str = ""
    show_login_dialog: bool = False
    show_user_menu: bool = False
    
    # API Key for Gemini
    api_key: str = ""
    show_api_key_dialog: bool = False
    
    # Error handling
    error_message: str = ""
    
    @rx.var
    def has_api_key(self) -> bool:
        """Check if API key is configured."""
        return len(self.api_key) > 10
    
    @rx.event
    async def send_message(self):
        """Send a message to the integrated host agent."""
        if not self.current_input.strip():
            return
        
        self.is_processing = True
        self.error_message = ""
        user_message = self.current_input
        self.current_input = ""
        
        # Add user message to display immediately
        user_msg = Message(
            id=str(uuid.uuid4()),
            role="user",
            content=user_message,
            context_id=self.context_id,
        )
        self.messages = self.messages + [user_msg]
        yield
        
        try:
            # Ensure API key is set in environment before processing
            import os
            if self.api_key.strip():
                os.environ["GOOGLE_API_KEY"] = self.api_key.strip()
            
            # Process message directly via host agent service
            service = get_host_agent_service()
            result = await service.process_message(
                message_text=user_message,
                context_id=self.context_id,
            )
            
            # Update context_id if new
            if result.get("context_id"):
                self.context_id = result["context_id"]
            
            # Add agent response
            response_text = result.get("response", "")
            if response_text:
                agent_msg = Message(
                    id=str(uuid.uuid4()),
                    role="agent",
                    content=response_text,
                    context_id=self.context_id,
                )
                self.messages = self.messages + [agent_msg]
            
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
            # Add error message to chat
            error_msg = Message(
                id=str(uuid.uuid4()),
                role="agent",
                content=f"Sorry, an error occurred: {str(e)}",
                context_id=self.context_id,
            )
            self.messages = self.messages + [error_msg]
        finally:
            self.is_processing = False
            # Save messages to localStorage
            self._save_to_storage()
    
    @rx.event
    async def refresh_messages(self):
        """Refresh message list from host agent service."""
        if not self.context_id:
            return
        
        try:
            service = get_host_agent_service()
            raw_messages = service.list_messages(self.context_id)
            
            if not raw_messages:
                return
            
            new_messages = []
            for msg in raw_messages:
                content = ""
                parts = msg.get("parts", [])
                for part in parts:
                    if isinstance(part, dict) and "text" in part:
                        content += part["text"]
                
                new_messages.append(
                    Message(
                        id=msg.get("message_id", str(uuid.uuid4())),
                        role=msg.get("role", "agent"),
                        content=content or str(msg),
                        context_id=msg.get("context_id"),
                    )
                )
            
            self.messages = new_messages
        except Exception as e:
            self.error_message = f"Failed to refresh: {str(e)}"
    
    @rx.event
    async def refresh_agents(self):
        """Refresh agent list from host agent service."""
        try:
            service = get_host_agent_service()
            # Ensure service is initialized (triggers auto-registration)
            await service.initialize()
            raw_agents = service.list_agents()
            
            new_agents = []
            for agent in raw_agents:
                new_agents.append(
                    Agent(
                        name=agent.get("name", "Unknown"),
                        description=agent.get("description", ""),
                        url=agent.get("url", ""),
                    )
                )
            
            self.agents = new_agents
        except Exception as e:
            self.error_message = f"Failed to refresh agents: {str(e)}"
    
    @rx.event
    async def register_agent(self):
        """Register a new remote agent."""
        if not self.new_agent_url.strip():
            return
        
        try:
            service = get_host_agent_service()
            result = await service.register_agent(self.new_agent_url)
            
            if result.get("success"):
                # Reset all form fields
                self.new_agent_url = ""
                self.new_agent_auth_type = "none"
                self.new_agent_auth_value = ""
                self.new_agent_custom_headers = ""
                self.show_agent_dialog = False
                self.show_advanced_options = False
                await self.refresh_agents()
            else:
                self.error_message = f"Failed to register: {result.get('error', 'Unknown error')}"
        except Exception as e:
            self.error_message = f"Failed to register agent: {str(e)}"
    
    @rx.event
    def toggle_agent_dialog(self):
        """Toggle the add agent dialog."""
        self.show_agent_dialog = not self.show_agent_dialog
        if not self.show_agent_dialog:
            # Reset form when closing
            self.new_agent_url = ""
            self.new_agent_auth_type = "none"
            self.new_agent_auth_value = ""
            self.new_agent_custom_headers = ""
            self.show_advanced_options = False
    
    @rx.event
    def toggle_advanced_options(self):
        """Toggle advanced options visibility."""
        self.show_advanced_options = not self.show_advanced_options
    
    @rx.event
    def clear_error(self):
        """Clear the error message."""
        self.error_message = ""
    
    @rx.event
    def new_conversation(self):
        """Start a new conversation."""
        self.messages = []
        self.context_id = None
        self.error_message = ""
    
    @rx.event
    def load_from_storage(self):
        """Placeholder for loading messages - persistence disabled for now."""
        pass
    
    def _save_to_storage(self):
        """Placeholder for saving messages - persistence disabled for now."""
        pass
    
    @rx.event
    async def save_api_key(self):
        """Save the API key and reinitialize the host agent."""
        if not self.api_key.strip():
            self.error_message = "Please enter a valid API key"
            return
        
        import os
        os.environ["GOOGLE_API_KEY"] = self.api_key.strip()
        
        # Reset the host agent service to use new key
        from .host_agent_service import HostAgentService
        HostAgentService._instance = None  # Reset singleton
        
        self.show_api_key_dialog = False
        self.error_message = ""
        
        # Re-initialize with new key
        service = get_host_agent_service()
        await service.initialize()
    
    @rx.event
    def toggle_api_key_dialog(self):
        """Toggle the API key dialog."""
        self.show_api_key_dialog = not self.show_api_key_dialog
    
    @rx.event
    def toggle_sidebar(self):
        """Toggle the sidebar collapsed state."""
        self.sidebar_collapsed = not self.sidebar_collapsed
    
    @rx.event
    def set_active_nav(self, nav: str):
        """Set the active navigation item."""
        self.active_nav = nav
    
    @rx.event
    async def remove_agent(self, agent_url: str):
        """Remove a registered agent by URL."""
        self.agents = [a for a in self.agents if a.url != agent_url]
        # Note: In a real implementation, you'd also unregister from the host agent service
    
    @rx.event
    def toggle_login_dialog(self):
        """Toggle the login dialog visibility."""
        self.show_login_dialog = not self.show_login_dialog
    
    @rx.event
    def toggle_user_menu(self):
        """Toggle the user dropdown menu."""
        self.show_user_menu = not self.show_user_menu
    
    @rx.event
    async def google_sign_in(self):
        """Mock Google Sign-in - simulates successful login.
        In production, this would redirect to Google OAuth flow.
        """
        self.is_logged_in = True
        self.user_name = "RamPrasad"
        self.user_email = "ramprasade66@gmail.com"
        self.user_avatar = "RP"
        self.show_login_dialog = False
        self.show_user_menu = False
    
    @rx.event
    def sign_out(self):
        """Sign out the current user."""
        self.is_logged_in = False
        self.user_name = ""
        self.user_email = ""
        self.user_avatar = ""
        self.show_user_menu = False
