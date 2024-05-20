from open_ai_api.chat_message import *
from open_ai_api.open_ai_client import OpenAIClient


class DailyAgenda:

    @staticmethod
    async def request(agent_name: str, agent_summary: str, agent_wake_up_hour: int, world_nodes: str, relevant_memories: str):
        response = await OpenAIClient.ask(
            messages=[
                UserMessage('You are controlling an NPC inside a video game simulation.'),
                UserMessage('Use a 24 hour format.'),
                UserMessage(f'The world is represented as a tree and it contains the following, where the first '
                              f'element is the root: {world_nodes}'),
                UserMessage(f'A summary of relevant memories for the agent: {relevant_memories}') if len(
                    relevant_memories) > 0 else None,
                UserMessage(f'A brief summary of the controlled agent: {agent_summary}'),
                UserMessage(f'{agent_name} usually wakes up at {agent_wake_up_hour} and starts the morning routine.'),
                UserMessage(f"Create a daily agenda for {agent_name} that will represent a rough sketch of the agent's "
                            "plan for the day, divided into five to eight chunks. The daily agenda must cover the "
                            "whole day, from the time of waking up until the time of sleep and must specify the time of day"),
            ],
        )
        return response.content


# class DailyAgenda:
#
#     @staticmethod
#     async def request(agent_name: str, agent_summary: str, agent_wake_up_hour: int, world_nodes: str, relevant_memories: str):
#         response = await OpenAIClient.ask(
#             messages=[
#                 SystemMessage('You are controlling an NPC inside a video game simulation.'),
#                 SystemMessage('Use a 24 hour format.'),
#                 SystemMessage(f'The world is represented as a tree and it contains the following, where the first '
#                               f'element is the root: {world_nodes}'),
#                 UserMessage(f'A summary of relevant memories for the agent: {relevant_memories}') if len(
#                     relevant_memories) > 0 else None,
#                 UserMessage(f'A brief summary of the controlled agent: {agent_summary}'),
#                 UserMessage(f'{agent_name} usually wakes up at {agent_wake_up_hour} and starts the morning routine.'),
#                 UserMessage(f"Create a daily agenda for {agent_name} that will represent a rough sketch of the agent's "
#                             "plan for the day, divided into five to eight chunks. The daily agenda must cover the "
#                             "whole day, from the time of waking up until the time of sleep and must specify the time of day"),
#             ],
#         )
#         return response.content
