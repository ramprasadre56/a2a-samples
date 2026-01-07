"""Host Agent Service for unified Reflex A2A application.

This module integrates the ADK HostAgent and Runner directly into the Reflex app,
eliminating the need for a separate FastAPI backend server.

Note: This is a simplified embedded version to avoid import path issues.
"""
import os
import uuid
import asyncio
import httpx
from typing import Optional, Dict, List, Any, Callable
from dataclasses import dataclass

# ADK imports
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.tools import ToolContext
from google.genai import types

# A2A imports
from a2a.client import A2AClient
from a2a.types import (
    AgentCard, 
    Message as A2AMessage, 
    Part, 
    TextPart, 
    Role, 
    Task, 
    TaskState,
    SendMessageRequest,
    MessageSendParams,
    SendMessageResponse,
)


@dataclass
class Conversation:
    """Represents a conversation with message history."""
    id: str
    messages: List[Dict[str, Any]]


class EmbeddedHostAgent:
    """Simplified embedded Host Agent for Reflex integration."""
    
    def __init__(self):
        self.remote_agents: Dict[str, AgentCard] = {}
        self.remote_agent_connections: Dict[str, A2AClient] = {}
        self.agent_urls: Dict[str, str] = {}  # agent_name -> url for raw HTTP fallback
        self._agents_info: str = "No agents registered yet."
        # Track active task IDs per agent for multi-turn conversations
        self.active_tasks: Dict[str, str] = {}  # agent_name -> task_id
    
    def register_agent_card(self, card: AgentCard, url: str):
        """Register a remote agent."""
        self.remote_agents[card.name] = card
        self.remote_agent_connections[card.name] = A2AClient(httpx_client=httpx.AsyncClient(), url=url)
        self.agent_urls[card.name] = url  # Store URL for fallback
        self._update_agents_info()
    
    def _update_agents_info(self):
        """Update the agents info string."""
        if not self.remote_agents:
            self._agents_info = "No agents registered."
            return
        
        lines = []
        for name, card in self.remote_agents.items():
            lines.append(f"- {name}: {card.description or 'No description'}")
        self._agents_info = "\n".join(lines)
    
    def list_remote_agents(self) -> Dict[str, Any]:
        """List all registered remote agents."""
        return {
            "result": [
                {"name": name, "description": card.description or ""}
                for name, card in self.remote_agents.items()
            ]
        }
    
    async def send_message(self, agent_name: str, message: str) -> str:
        """Send a message to a remote agent, maintaining task continuity."""
        print(f"[EmbeddedHostAgent] send_message called: agent='{agent_name}', message='{message}'")
        
        if agent_name not in self.remote_agent_connections:
            available = list(self.remote_agents.keys())
            print(f"[EmbeddedHostAgent] Agent not found! Available: {available}")
            return f"Agent '{agent_name}' not found. Available agents: {available}"
        
        client = self.remote_agent_connections[agent_name]
        print(f"[EmbeddedHostAgent] Found client for {agent_name}: {client}")
        
        # Check if we have an active task with this agent
        active_task_id = self.active_tasks.get(agent_name)
        if active_task_id:
            print(f"[EmbeddedHostAgent] Continuing task: {active_task_id}")
        
        try:
            # Create the message
            a2a_message = A2AMessage(
                role=Role.user,
                parts=[Part(root=TextPart(text=message))],
                message_id=str(uuid.uuid4()),
            )
            # Wrap in SendMessageRequest with MessageSendParams
            # Include task_id if we have an active task
            params = MessageSendParams(message=a2a_message)
            if active_task_id:
                # Set task_id to continue the conversation
                params = MessageSendParams(
                    message=a2a_message,
                    configuration={"task_id": active_task_id}  # Some agents use configuration
                )
            
            request = SendMessageRequest(
                id=str(uuid.uuid4()),
                params=params
            )
            print(f"[EmbeddedHostAgent] Sending message to {agent_name}...")
            
            # Try using SDK first
            try:
                response = await client.send_message(request)
                print(f"[EmbeddedHostAgent] Got response type: {type(response)}")
            except Exception as sdk_error:
                # SDK validation failed - try raw HTTP request for JS agent compatibility
                print(f"[EmbeddedHostAgent] SDK error, trying raw HTTP: {sdk_error}")
                agent_url = self.agent_urls.get(agent_name, "http://localhost:41242")
                
                async with httpx.AsyncClient() as http_client:
                    raw_response = await http_client.post(
                        f"{agent_url}",
                        json=request.model_dump(mode='json', exclude_none=True),
                        headers={"Content-Type": "application/json"},
                        timeout=60.0
                    )
                    if raw_response.status_code == 200:
                        data = raw_response.json()
                        print(f"[EmbeddedHostAgent] Raw response keys: {data.keys() if isinstance(data, dict) else type(data)}")
                        
                        # Extract from response
                        if isinstance(data, dict):
                            result_data = data.get('result', data)
                            
                            # Get task ID for polling if present
                            task_id = result_data.get('id') if isinstance(result_data, dict) else None
                            
                            # Check for artifacts in the response
                            artifacts = result_data.get('artifacts', []) if isinstance(result_data, dict) else []
                            if artifacts:
                                artifact_texts = []
                                for artifact in artifacts:
                                    if isinstance(artifact, dict) and 'parts' in artifact:
                                        for part in artifact['parts']:
                                            if isinstance(part, dict) and 'text' in part:
                                                artifact_texts.append(f"**File: {artifact.get('name', 'unknown')}**\n```\n{part['text']}\n```")
                                if artifact_texts:
                                    return "\n\n".join(artifact_texts)
                            
                            # If task_id present, poll for completed task with artifacts
                            if task_id:
                                import asyncio
                                for _ in range(10):  # Poll up to 10 times
                                    await asyncio.sleep(1)
                                    try:
                                        task_response = await http_client.get(
                                            f"{agent_url}/tasks/{task_id}",
                                            timeout=10.0
                                        )
                                        if task_response.status_code == 200:
                                            task_data = task_response.json()
                                            print(f"[EmbeddedHostAgent] Task poll response: {str(task_data)[:300]}...")
                                            task_result = task_data.get('result', task_data)
                                            
                                            # Check task status
                                            status = task_result.get('status', {}) if isinstance(task_result, dict) else {}
                                            state = status.get('state', '')
                                            
                                            # Get artifacts
                                            task_artifacts = task_result.get('artifacts', []) if isinstance(task_result, dict) else []
                                            if task_artifacts:
                                                artifact_texts = []
                                                for artifact in task_artifacts:
                                                    if isinstance(artifact, dict) and 'parts' in artifact:
                                                        for part in artifact['parts']:
                                                            if isinstance(part, dict) and 'text' in part:
                                                                artifact_texts.append(f"**File: {artifact.get('name', 'unknown')}**\n```\n{part['text']}\n```")
                                                if artifact_texts:
                                                    return "\n\n".join(artifact_texts)
                                            
                                            # Check status message
                                            if status.get('message'):
                                                msg = status['message']
                                                parts = msg.get('parts', [])
                                                for part in parts:
                                                    if isinstance(part, dict) and 'text' in part:
                                                        return part['text']
                                            
                                            if state == 'completed':
                                                return f"Task completed. Files generated: Check the Coder Agent output."
                                    except Exception as poll_err:
                                        print(f"[EmbeddedHostAgent] Poll error: {poll_err}")
                            
                            # Check for status.message.parts
                            if isinstance(result_data, dict):
                                status = result_data.get('status', {})
                                if isinstance(status, dict) and 'message' in status:
                                    msg = status['message']
                                    if isinstance(msg, dict):
                                        parts = msg.get('parts', [])
                                        for part in parts:
                                            if isinstance(part, dict) and 'text' in part:
                                                return part['text']
                            
                        return f"Agent task submitted. Check agent logs for generated files."
                    else:
                        return f"Agent returned error: {raw_response.status_code}"
            
            # Handle SendMessageResponse wrapper
            if isinstance(response, SendMessageResponse):
                print(f"[EmbeddedHostAgent] SendMessageResponse received, extracting root...")
                actual_result = response.root  # Use 'root' not 'result'
                print(f"[EmbeddedHostAgent] Root type: {type(actual_result)}")
            else:
                actual_result = response
            
            # Process the actual result (Task or Message)
            if isinstance(actual_result, A2AMessage):
                # Direct message response - no task tracking needed
                result = ""
                for part in actual_result.parts:
                    if hasattr(part, 'root') and hasattr(part.root, 'text'):
                        result += part.root.text
                print(f"[EmbeddedHostAgent] Message result: {result[:100] if result else 'empty'}...")
                return result or "Agent responded with no text."
            elif isinstance(actual_result, Task):
                # Task response - track the task ID for continuity
                task_id = actual_result.id
                task_state = actual_result.status.state if actual_result.status else None
                print(f"[EmbeddedHostAgent] Task response: id={task_id}, state={task_state}")
                
                # Store or clear task ID based on state
                if task_state in [TaskState.completed, TaskState.failed, TaskState.canceled]:
                    # Task is done, clear it
                    if agent_name in self.active_tasks:
                        del self.active_tasks[agent_name]
                    print(f"[EmbeddedHostAgent] Task completed, cleared active task")
                else:
                    # Task is ongoing, save for continuity
                    self.active_tasks[agent_name] = task_id
                    print(f"[EmbeddedHostAgent] Task ongoing, saved for continuity: {task_id}")
                
                if actual_result.status and actual_result.status.message:
                    content = ""
                    for part in actual_result.status.message.parts:
                        if hasattr(part, 'root') and hasattr(part.root, 'text'):
                            content += part.root.text
                    return content or f"Task {task_id} - {task_state}"
                return f"Task created: {task_id}"
            else:
                # Try to extract text from unknown response types
                print(f"[EmbeddedHostAgent] Unknown result type: {type(actual_result)}, trying to stringify...")
                return str(actual_result)
        except Exception as e:
            import traceback
            print(f"[EmbeddedHostAgent] ERROR calling {agent_name}: {e}")
            traceback.print_exc()
            return f"Error calling agent '{agent_name}': {str(e)}"
    
    @property
    def root_instruction(self) -> str:
        """Get the root instruction for the agent."""
        return f"""You are a helpful host agent that coordinates with remote agents to help users.

Available remote agents:
{self._agents_info}

IMPORTANT GUIDELINES:
1. When a user asks about available agents, use the list_remote_agents tool.
2. When delegating tasks to remote agents, use the send_message tool.
3. BE DIRECT - Don't ask for confirmation. If the user says "convert 100 USD to INR", 
   immediately delegate to the Currency Agent with the full request.
4. INCLUDE FULL CONTEXT - When sending messages to remote agents, include all necessary 
   details in one message. Example: "Please convert 100 USD to INR and return the result"
5. If a remote agent asks for clarification but you already have the information, 
   resend the complete request with all details.
6. For simple greetings like "hello world agent", just send "hello" or "greet me".
7. Always try to complete the user's request in as few steps as possible.
8. Return the final result directly to the user without asking if they need anything else.
"""
    
    def create_agent(self) -> Agent:
        """Create the ADK Agent."""
        model = os.getenv('SELECTED_MODEL', 'gemini')
        if model == 'gemini':
            model_name = 'gemini-2.0-flash-001'
        else:
            # Use LiteLLM for other models
            from google.adk.models import LiteLlm
            model_name = LiteLlm(model=f'ollama_chat/{model}')
        
        return Agent(
            model=model_name if isinstance(model_name, str) else model_name,
            name='host_agent',
            instruction=self.root_instruction,
            description='Host agent that orchestrates interactions with remote agents.',
            tools=[
                self.list_remote_agents,
                self.send_message,
            ],
        )


class HostAgentService:
    """Service that manages the ADK HostAgent and Runner."""
    
    _instance: Optional['HostAgentService'] = None
    
    # Default agents to register on startup
    DEFAULT_AGENTS = [
        "http://localhost:9999",   # HelloWorld agent
        "http://localhost:10000",  # LangGraph Currency agent
    ]
    
    def __init__(self):
        self._host_agent: Optional[EmbeddedHostAgent] = None
        self._runner: Optional[Runner] = None
        self._session_service: Optional[InMemorySessionService] = None
        self._artifact_service: Optional[InMemoryArtifactService] = None
        self._conversations: Dict[str, Conversation] = {}
        self._initialized = False
    
    @classmethod
    def get_instance(cls) -> 'HostAgentService':
        """Get or create the singleton instance."""
        if cls._instance is None:
            cls._instance = HostAgentService()
        return cls._instance
    
    async def initialize(self):
        """Initialize the host agent and runner."""
        if self._initialized:
            return
        
        print("[HostAgentService] Initializing...")
        
        # Initialize services
        self._session_service = InMemorySessionService()
        self._artifact_service = InMemoryArtifactService()
        
        # Create embedded host agent
        self._host_agent = EmbeddedHostAgent()
        agent = self._host_agent.create_agent()
        
        # Create runner
        self._runner = Runner(
            app_name='A2A',
            agent=agent,
            session_service=self._session_service,
            artifact_service=self._artifact_service,
        )
        
        self._initialized = True
        print("[HostAgentService] Initialized successfully")
        
        # Auto-register default agents
        await self._auto_register_default_agents()
    
    async def _auto_register_default_agents(self):
        """Auto-register default agents on startup."""
        print(f"[HostAgentService] Auto-registering {len(self.DEFAULT_AGENTS)} default agents...")
        for agent_url in self.DEFAULT_AGENTS:
            try:
                result = await self.register_agent(agent_url)
                if result.get("success"):
                    print(f"[HostAgentService] ✓ Registered: {result.get('agent')} ({agent_url})")
                else:
                    print(f"[HostAgentService] ✗ Failed to register {agent_url}: {result.get('error')}")
            except Exception as e:
                print(f"[HostAgentService] ✗ Error registering {agent_url}: {e}")
        print("[HostAgentService] Initialized successfully")
    
    def get_or_create_conversation(self, context_id: Optional[str] = None) -> Conversation:
        """Get or create a conversation."""
        if not context_id:
            context_id = str(uuid.uuid4())
        
        if context_id not in self._conversations:
            self._conversations[context_id] = Conversation(
                id=context_id,
                messages=[],
            )
        
        return self._conversations[context_id]
    
    async def process_message(
        self,
        message_text: str,
        context_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Process a user message and return the response."""
        if not self._initialized:
            await self.initialize()
        
        # Get or create conversation
        conversation = self.get_or_create_conversation(context_id)
        context_id = conversation.id
        
        # Store user message
        message_id = str(uuid.uuid4())
        conversation.messages.append({
            "message_id": message_id,
            "role": "user",
            "parts": [{"text": message_text}],
            "context_id": context_id,
        })
        
        # Create/get session
        session = await self._session_service.get_session(
            app_name='A2A',
            user_id='reflex_user',
            session_id=context_id,
        )
        if session is None:
            session = await self._session_service.create_session(
                app_name='A2A',
                user_id='reflex_user',
                session_id=context_id,
            )
        
        # Convert message to ADK format
        content = types.Content(
            role='user',
            parts=[types.Part.from_text(text=message_text)],
        )
        
        # Run agent
        response_text = ""
        try:
            async for event in self._runner.run_async(
                user_id='reflex_user',
                session_id=context_id,
                new_message=content,
            ):
                # Extract response from events
                if hasattr(event, 'content') and event.content:
                    if hasattr(event.content, 'parts'):
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                response_text += part.text
        except Exception as e:
            print(f"[HostAgentService] Error processing message: {e}")
            import traceback
            traceback.print_exc()
            response_text = f"Error: {str(e)}"
        
        # Store agent response
        if response_text:
            conversation.messages.append({
                "message_id": str(uuid.uuid4()),
                "role": "agent",
                "parts": [{"text": response_text}],
                "context_id": context_id,
            })
        
        return {
            "context_id": context_id,
            "message_id": message_id,
            "response": response_text,
        }
    
    def list_messages(self, context_id: str) -> List[Dict[str, Any]]:
        """Get messages for a conversation."""
        if context_id not in self._conversations:
            return []
        return self._conversations[context_id].messages
    
    async def register_agent(self, agent_url: str) -> Dict[str, Any]:
        """Register a remote agent."""
        if not self._initialized:
            await self.initialize()
        
        try:
            # Try using the A2A SDK first
            client = A2AClient(httpx_client=httpx.AsyncClient(), url=agent_url)
            try:
                agent_card = await client.get_card()
            except Exception as sdk_error:
                # SDK failed - try alternative agent card URLs for cross-SDK compatibility
                # Different SDKs use different endpoints:
                # - Python SDK: /.well-known/agent-card.json
                # - .NET SDK: /.well-known/agent.json
                # - JS SDK: /.well-known/agent-card.json or /.well-known/agent.json
                print(f"[HostAgentService] SDK get_card failed: {sdk_error}")
                print("[HostAgentService] Trying alternative agent card endpoints...")
                
                agent_card = None
                agent_card_urls = [
                    f"{agent_url.rstrip('/')}/.well-known/agent.json",
                    f"{agent_url.rstrip('/')}/.well-known/agent-card.json",
                ]
                
                async with httpx.AsyncClient() as http_client:
                    for card_url in agent_card_urls:
                        try:
                            response = await http_client.get(card_url, timeout=10.0)
                            if response.status_code == 200:
                                card_data = response.json()
                                print(f"[HostAgentService] Got agent card from {card_url}")
                                # Create AgentCard from dict
                                agent_card = AgentCard.model_validate(card_data)
                                break
                        except Exception as e:
                            print(f"[HostAgentService] Failed to fetch from {card_url}: {e}")
                            continue
                
                if not agent_card:
                    return {"success": False, "error": f"Could not fetch agent card from {agent_url}. Tried: {agent_card_urls}"}
            
            # Register with host agent
            self._host_agent.register_agent_card(agent_card, agent_url)
            
            # Recreate agent with updated tools
            agent = self._host_agent.create_agent()
            self._runner = Runner(
                app_name='A2A',
                agent=agent,
                session_service=self._session_service,
                artifact_service=self._artifact_service,
            )
            
            return {"success": True, "agent": agent_card.name}
        except Exception as e:
            print(f"[HostAgentService] Error registering agent: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List registered remote agents."""
        if not self._host_agent:
            return []
        
        result = self._host_agent.list_remote_agents()
        return result.get("result", [])


# Convenience function
def get_host_agent_service() -> HostAgentService:
    """Get the host agent service singleton."""
    return HostAgentService.get_instance()
