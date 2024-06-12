from open_ai_api import OpenAIClient, SystemMessage, UserMessage


class RelevantMemorySummary:

    @staticmethod
    async def request(agent_name: str, agent_summary: str, relevant_memories: str, world_nodes: str, query: str, current_time:str):

        response = await OpenAIClient.ask(
            messages=[
                SystemMessage('You are controlling an NPC inside a video game simulation.'),
                SystemMessage('Use a 24 hour format.'),
                SystemMessage(f'The world is represented as a tree and it contains the following, where the first '
                              f'element is the root: {world_nodes}'),
                SystemMessage(f'Give only the answer and avoid giving any extra explanations or dialogue.'),
                SystemMessage(f'The memories belong to {agent_name}.'),
                SystemMessage(f'The time now is: {current_time}.'),
                UserMessage(f'Generate a summary of these memories {relevant_memories}. The summary must retain'
                            f'the original information, as best as possible. Try not to repeat yourself.'
                            f'The summary extracted must be relevant for the following topic: {query}')
            ],
        )
        return response.content
