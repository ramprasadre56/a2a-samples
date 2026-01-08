import os
import sys
import json
import asyncio
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, BackgroundTasks, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel

# Add python directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../python'))

try:
    from service.server.adk_host_manager import ADKHostManager
    from service.persistence import RedisPersistence
    from a2a.types import Message, Part, TextPart, Role, AgentCard
except ImportError as e:
    print(f"Import Error: {e}")
    # Fallback to local import if structure is flattened in Vercel
    sys.path.append(os.path.dirname(__file__))
    # Retry logic or fail

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

persistence = RedisPersistence()
httpx_client: Optional[httpx.AsyncClient] = None
host_manager: Optional[ADKHostManager] = None

class MessageRequest(BaseModel):
    message: str
    contextId: Optional[str] = None

class AgentRequest(BaseModel):
    url: str

@app.on_event("startup")
async def startup_event():
    global httpx_client, host_manager
    httpx_client = httpx.AsyncClient(timeout=30)
    
    # Initialize Host Manager
    api_key = os.environ.get("GEMINI_API_KEY", "")
    os.environ["GOOGLE_API_KEY"] = api_key
    
    host_manager = ADKHostManager(http_client=httpx_client, api_key=api_key)
    
    # Hydrate Agents
    agents = persistence.load_agents()
    if agents:
        print(f"Hydrating {len(agents)} agents")
        host_manager._agents = agents
        # ADKHostManager registers agents to internal HostAgent in _initialize_host
        # But we might need to manually re-register them if they were not in __init__
        for agent in agents:
             host_manager._host_agent.register_agent_card(agent)
             
    # Hydrate State
    state = persistence.load_state("host_manager")
    if state:
        try:
             host_manager._conversations = state.get('conversations', [])
             host_manager._messages = state.get('messages', [])
             # Reconstruct tasks if possible
             # host_manager._tasks = state.get('tasks', [])
        except Exception as e:
             print(f"State hydration failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    if httpx_client:
        await httpx_client.aclose()

async def save_state_background():
    if not host_manager:
        return
    persistence.save_agents(host_manager.agents)
    
    state = {
        'conversations': host_manager._conversations,
        'messages': host_manager._messages,
        # 'tasks': host_manager._tasks
    }
    persistence.save_state("host_manager", state)

@app.post("/api/message")
async def handle_message(request: MessageRequest, background_tasks: BackgroundTasks):
    if not host_manager:
        raise HTTPException(status_code=500, detail="Host Manager not initialized")

    print(f"Received message: {request.message} context: {request.contextId}")
    
    # Create Message object
    msg = Message(
        parts=[Part(root=TextPart(text=request.message))],
        role=Role.user,
        context_id=request.contextId 
    )
    
    # Process
    try:
        await host_manager.process_message(msg)
    except Exception as e:
        print(f"Error processing message: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
    # Find Response
    # Helper to find last agent message in context
    response_text = "I'm sorry, I couldn't process that."
    new_context_id = request.contextId
    
    # Find the conversation
    if request.contextId:
        conv = host_manager.get_conversation(request.contextId)
    else:
        # If new conversation was created implicitly by process_message?
        # process_message creates session if needed.
        # But we need the context_id from the message we sent? 
        # msg.context_id might be None.
        # ADKHostManager uses context_id to find conversation.
        # If context_id is None, sanitize_message?
        pass

    # Actually `process_message` logic:
    # If context_id is None, it might fail or create new.
    # Check `_messages` for the LAST message associated with this operation.
    
    # Simple heuristic: Get last message in `host_manager._messages`
    if host_manager._messages:
        last_msg = host_manager._messages[-1]
        if last_msg.role != Role.user:
             # Extract text
             parts = host_manager.adk_content_from_message(last_msg).parts
             if parts:
                 response_text = parts[0].text or "Received non-text response"
             new_context_id = last_msg.context_id
    
    # Schedule Save
    background_tasks.add_task(save_state_background)
    
    return {
        "response": response_text,
        "contextId": new_context_id
    }

@app.get("/api/agents")
async def list_agents():
    if not host_manager:
        return {"result": []}
    return {"result": [a.model_dump() for a in host_manager.agents]}

@app.post("/api/agents")
async def register_agent(request: AgentRequest, background_tasks: BackgroundTasks):
    if not host_manager:
         raise HTTPException(status_code=500, detail="Host Manager not initialized")
    
    try:
        host_manager.register_agent(request.url)
        background_tasks.add_task(save_state_background)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Fallback for Vercel if it strips /api prefix differently?
# No, if mapped to /api via `api/index.py`, paths are `/message`, `/agents`.
# But frontend calls `/api/message`.
# If I define `@app.post("/api/message")`, request to `/api/api/message` matches?
# Vercel Function: `api/index.py` handles `/api`.
# Request to `/api/message`:
# SCRIPT_NAME=/api, PATH_INFO=/message.
# FastAPI sees `/message`.
# So I should define paths WITHOUT `/api` prefix.

# REDEFINING PATHS
@app.post("/message")
async def handle_message_root(request: MessageRequest, background_tasks: BackgroundTasks):
    return await handle_message(request, background_tasks)

@app.get("/agents")
async def list_agents_root():
    return await list_agents()

@app.post("/agents")
async def register_agent_root(request: AgentRequest, background_tasks: BackgroundTasks):
    return await register_agent(request, background_tasks)

