from typing import List


class Memory:
    def __init__(self, description: str, last_access_in_game_time: int, importance: int, embeddings: List[float]):
        self.description = description  # some kind of natural language description for the memory
        self.last_access_in_game_time = last_access_in_game_time  # seconds since game started
        self.importance = importance  # on a scale from 1 to 10, should be determined by GPT model.
        self.embeddings = embeddings  # Text embeddings from OpenAI API

    def __str__(self):
        return (f"Memory(description={self.description}, "
                f"last_access_in_game_time={self.last_access_in_game_time}, "
                f"importance={self.importance}, embeddings={self.embeddings})")
