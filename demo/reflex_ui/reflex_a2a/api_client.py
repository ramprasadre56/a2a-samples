"""API client for communicating with the A2A backend server."""
import httpx
from typing import Optional
import uuid


class A2AClient:
    """HTTP client for the A2A demo backend."""
    
    def __init__(self, base_url: str = "http://localhost:12002"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def send_message(
        self,
        message: str,
        context_id: Optional[str] = None,
    ) -> dict:
        """Send a message to the host agent."""
        message_id = str(uuid.uuid4())
        # Backend expects JSONRPC format with 'params' containing Message fields
        parts = [{"kind": "text", "text": message}]
        params = {
            "message_id": message_id,
            "role": "user",
            "parts": parts,
        }
        if context_id:
            params["context_id"] = context_id
        
        payload = {"params": params}
        
        response = await self.client.post(
            f"{self.base_url}/message/send",
            json=payload,
        )
        response.raise_for_status()
        return response.json()
    
    async def list_messages(self, context_id: Optional[str] = None) -> list:
        """Get message history."""
        # Backend expects conversation_id in 'params'
        payload = {"params": context_id or ""}
        
        response = await self.client.post(
            f"{self.base_url}/message/list",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("result", [])
    
    async def list_conversations(self) -> list:
        """Get all conversations."""
        response = await self.client.post(
            f"{self.base_url}/conversation/list",
            json={},
        )
        response.raise_for_status()
        data = response.json()
        return data.get("result", [])
    
    async def list_agents(self) -> list:
        """Get registered remote agents."""
        response = await self.client.post(
            f"{self.base_url}/agent/list",
            json={},
        )
        response.raise_for_status()
        data = response.json()
        return data.get("result", [])
    
    async def register_agent(self, agent_url: str) -> dict:
        """Register a remote agent."""
        # Backend expects URL in 'params'
        response = await self.client.post(
            f"{self.base_url}/agent/register",
            json={"params": agent_url},
        )
        response.raise_for_status()
        return response.json()
    
    async def get_pending_messages(self) -> dict:
        """Get messages currently being processed."""
        response = await self.client.post(
            f"{self.base_url}/message/pending",
            json={},
        )
        response.raise_for_status()
        data = response.json()
        return data.get("result", {})


# Singleton instance
_client: Optional[A2AClient] = None


def get_client(base_url: str = "http://localhost:12002") -> A2AClient:
    """Get or create the A2A client instance."""
    global _client
    if _client is None:
        _client = A2AClient(base_url)
    return _client
