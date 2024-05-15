from scipy import spatial
from typing import List

from memory.memory import Memory
from open_ai_api import EmbeddingClient


def cosine_similarity(v1, v2):
    return 1 - spatial.distance.cosine(v1, v2)


def decay_over_time(rate, minutes_passed):
    return (1 - rate) ** minutes_passed

max_memories = 10

class MemoryStorage:

    def __init__(self):
        self.memories = []

    async def add_memory(self, description: str, importance: int, seconds_since_game_started: int):
        embeddings = await EmbeddingClient.encode(description)
        memory = Memory(description, seconds_since_game_started, importance, embeddings)
        self.memories.append(memory)

    async def retrieve_relevant_memories(self, context: str) -> List[Memory]:
        result = []
        context_embeddings = await EmbeddingClient.encode(context)
        for memory in self.memories:
            cosine_sim = cosine_similarity(context_embeddings, memory.embeddings)
            if cosine_sim > 0:
                result.append(memory)
                print(f"Similarity: {cosine_sim}")
        return result

    async def retrieve_relevant_memories_str(self, context: str, seconds_from_start: int, min_score: int) -> str:
        result = ''
        context_embeddings = await EmbeddingClient.encode(context)

        result += ''

        for memory in self.memories:
            cosine_sim = cosine_similarity(context_embeddings, memory.embeddings)
            minutes_passed = (seconds_from_start//60 - memory.last_access_in_game_time//60)# // 60
            decay_value = decay_over_time(rate=0.995, minutes_passed=minutes_passed)

            score = decay_value * 0.2 + memory.importance // 10 + cosine_sim
            if score > min_score:
                result += memory.description

                message = (f'Memory: {memory.description}\n'
                           f'Cosine sim: {cosine_sim}\n'
                           f'Decay value: {decay_value}\n'
                           f'Importance: {memory.importance}\n'
                           f'Score: {score}\n\n')
                print(message)

        return result[:max_memories]

    async def retrieve_relevant_memories_debug(self, context: str, seconds_from_start: int) -> str:
        result = ''
        context_embeddings = await EmbeddingClient.encode(context)

        result += f'Context: {context}\n\n'

        for memory in self.memories:
            cosine_sim = cosine_similarity(context_embeddings, memory.embeddings)
            minutes_passed = (seconds_from_start - memory.last_access_in_game_time) // 60
            decay_value = decay_over_time(rate=0.995, minutes_passed=minutes_passed)

            score = decay_value * 0.3 + memory.importance // 10 + cosine_sim

            message = (f'Memory: {memory.description}\n'
                       f'Cosine sim: {cosine_sim}\n'
                       f'Decay value: {decay_value}\n'
                       f'Score: {score}\n\n')

            result += message
        print(result)
        return result
