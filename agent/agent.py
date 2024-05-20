from memory.memory import Memory
from memory.memory_storage import MemoryStorage
from typing import List


class Agent:
    def __init__(self, agent_id: str, name: str, summary: str, wake_up_hour: int, world_nodes: str, current_location: str):
        self.id = agent_id
        self.name = name
        self.summary = summary
        self.wake_up_hour = wake_up_hour,
        self.world_nodes = world_nodes
        self.current_location = current_location
        self.memory_storage = MemoryStorage()
        self.current_plan = {}
        self.current_tasks = []
        self.action_history = []
        self.daily_schedule = ''

    async def add_memory(self, description: str, importance: int, seconds_since_game_started: int, embeddings: List[float]):
        """Asynchronously add a memory to the agent's memory storage."""
        await self.memory_storage.add_memory(description, importance, seconds_since_game_started, embeddings)

    async def retrieve_memories_by_context(self, context: str, context_embeddings: List[float]) -> List[Memory]:
        """Asynchronously retrieve memories by context from the memory storage."""
        return await self.memory_storage.retrieval_by_context(context, context_embeddings)

    def __str__(self):
        return f"Agent Name: {self.name}, Summary: {self.summary}, Stored Memories: {len(self.memory_storage.memories)}"
