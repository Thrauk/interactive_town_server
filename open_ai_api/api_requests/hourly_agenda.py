from open_ai_api.chat_message import *
from open_ai_api.open_ai_client import OpenAIClient


class HourlyAgenda:

    @staticmethod
    async def request(daily_agenda: str, agent_name: str, agent_summary: str, world_nodes: str):
        response = await OpenAIClient.ask(
            messages=[
                SystemMessage('You are controlling an NPC inside a video game simulation.'),
                SystemMessage('Use a 24 hour format.'),
                SystemMessage(f'The world is represented as a tree and it contains the following, where the first '
                              f'element is the root: {world_nodes}'),
                UserMessage(f'A brief summary of the controlled agent: {agent_summary}'),
                UserMessage(f"Make a 24 hour daily action description, by splitting this daily agenda that represents a rough "
                            f"planning of the agent's day: {daily_agenda}."
                            # f"Sleeping hours should be described as: Sleeping in ..."
                            # f"The output is a list containing EXACTLY 24 elements where the hour is always UNIQUE and its "
                            f"format looks like this: [["
                            f"'Description of the daily schedule for 9-10', 9], ['Description of the daily "
                            f"schedule for 10-11', 10], ...]"),
            ],
        )
        return response.content
