import os
import json
import pickle
import base64
from typing import List, Any
import redis

from a2a.types import AgentCard

class RedisPersistence:
    def __init__(self):
        self.redis_url = os.environ.get("KV_URL", os.environ.get("REDIS_URL"))
        self.client = None
        if self.redis_url:
            try:
                self.client = redis.from_url(self.redis_url)
                print(f"Connected to Redis at {self.redis_url}")
            except Exception as e:
                print(f"Failed to connect to Redis: {e}")

    def save_agents(self, agents: List[AgentCard]):
        if not self.client:
            return
        try:
            # Serialize agents list
            data = [agent.model_dump() for agent in agents]
            self.client.set("a2a:agents", json.dumps(data))
        except Exception as e:
            print(f"Failed to save agents to Redis: {e}")

    def load_agents(self) -> List[AgentCard]:
        if not self.client:
            return []
        try:
            data = self.client.get("a2a:agents")
            if data:
                raw_agents = json.loads(data)
                return [AgentCard(**agent) for agent in raw_agents]
        except Exception as e:
            print(f"Failed to load agents from Redis: {e}")
        return []

    # Persistence for conversations is trickier due to complex objects.
    # For now, we will try to pickle the conversations list if meaningful,
    # or just rely on re-creating them.
    # Warning: Pickling complex objects across versions is brittle.
    
    def save_state(self, key: str, value: Any):
        if not self.client:
            return
        try:
            pickled = pickle.dumps(value)
            self.client.set(f"a2a:state:{key}", base64.b64encode(pickled).decode('utf-8'))
        except Exception as e:
             # Be silent often as some things can't be pickled
             pass

    def load_state(self, key: str) -> Any:
        if not self.client:
            return None
        try:
            data = self.client.get(f"a2a:state:{key}")
            if data:
                return pickle.loads(base64.b64decode(data))
        except Exception as e:
            pass
        return None
