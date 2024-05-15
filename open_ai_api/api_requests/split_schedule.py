from open_ai_api.api_requests.actions.tools.execute_action import availableActions
from open_ai_api.chat_message import *
from open_ai_api.open_ai_client import OpenAIClient


class SplitSchedule:

    @staticmethod
    async def request(action_description: str, agent_name: str, agent_summary: str, world_nodes: str):
        actions = str.join(', ', availableActions)
        response = await OpenAIClient.ask(
            messages=[
                SystemMessage('You are controlling an NPC inside a video game simulation.'),
                SystemMessage('Use a 24 hour format.'),
                SystemMessage(f'The world is represented as a tree and it contains the following, where the first '
                              f'element is the root: {world_nodes}'),
                UserMessage(f'A brief summary of the controlled agent: {agent_summary}'),
                UserMessage(f"The agent planned to {action_description} for the next hour. If possible, split this task into "
                            f"x minute chunks, that added, make a full 60 min hour. Format the output like this: [['chunk "
                            f"description', 10], ['chunk 2 description', 15], ...]"),
            ],
        )
        return response.content
