import sys
import asyncio
import os
import uuid
from typing import Any
import logging

# Add the multiagent host path
current_dir = os.getcwd()
host_agent_path = os.path.abspath(os.path.join(current_dir, "../../samples/python/hosts/multiagent"))
sys.path.append(host_agent_path)

print(f"Added to path: {host_agent_path}")

try:
    from host_agent import HostAgent
    from google.adk import Agent, Runner
    from google.adk.agents.callback_context import CallbackContext
    from a2a.types import Message, Part, TextPart, Role
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Mock HTTPX Client
class MockHttpxClient:
    pass

class MockService:
    async def create_session(self, *args, **kwargs): return type('obj', (object,), {'id': 'mock_session_id'})
    async def get_session(self, *args, **kwargs): return 'mock_session'
    async def append_event(self, *args, **kwargs): pass
    async def load_artifact(self, *args, **kwargs): pass

class MockContext:
    def __init__(self):
        self.state = {}
        self.history = []

async def main():
    print("[TestRunner] Starting reproduction script with Runner...")
    
    # 1. Initialize HostAgent
    try:
        host_agent = HostAgent(
            remote_agent_addresses=[],
            http_client=MockHttpxClient(),
        )
    except Exception as e:
        print(f"[TestRunner] Failed to init HostAgent: {e}")
        return

    # 2. Create Agent
    try:
        agent = host_agent.create_agent()
    except Exception as e:
        print(f"[TestRunner] Failed to create_agent: {e}")
        return

    # 3. Create Runner (Mock services)
    print("[TestRunner] Creating Runner...")
    runner = Runner(
        app_name="TestApp",
        agent=agent,
        artifact_service=MockService(),
        session_service=MockService(),
        memory_service=MockService(),
    )

    # 4. Create Mock Messages
    message = Message(
        role=Role.user,
        parts=[Part(root=TextPart(text="Hello world"))],
        message_id=str(uuid.uuid4()),
        context_id=str(uuid.uuid4())
    )

    # Create a dummy session object
    session = type('Session', (object,), {'id': 'mock_session_id', 'state': {}, 'history': []})()

    # 5. Run Async via Runner
    print("[TestRunner] Calling runner.run_async...")
    
    try:
        # Use asyncio.wait_for to detect hang
        async def run_loop():
            async for event in runner.run_async(
                message,
                session=session,
            ):
                print(f"[TestRunner] Received event: {event}")
        
        await asyncio.wait_for(run_loop(), timeout=10.0)
        
    except asyncio.TimeoutError:
        print("[TestRunner] CRITICAL: runner.run_async TIMED OUT (Hung)!")
    except TypeError as te:
        print(f"[TestRunner] TypeError: {te}")
    except Exception as e:
        print(f"[TestRunner] Error in run_async: {e}")
        import traceback
        traceback.print_exc()

    print("[TestRunner] Finished.")

if __name__ == "__main__":
    # Force Gemini model for this test to match current server state
    os.environ['SELECTED_MODEL'] = 'gemini'
    asyncio.run(main())
