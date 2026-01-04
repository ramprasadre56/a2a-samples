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
    show_agent_dialog: bool = False
    
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
                self.new_agent_url = ""
                self.show_agent_dialog = False
                await self.refresh_agents()
            else:
                self.error_message = f"Failed to register: {result.get('error', 'Unknown error')}"
        except Exception as e:
            self.error_message = f"Failed to register agent: {str(e)}"
    
    @rx.event
    def toggle_agent_dialog(self):
        """Toggle the add agent dialog."""
        self.show_agent_dialog = not self.show_agent_dialog
    
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
