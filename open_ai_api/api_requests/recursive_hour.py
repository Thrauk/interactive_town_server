from open_ai_api.api_requests.actions.tools.execute_action import availableActions
from open_ai_api.chat_message import *
from open_ai_api.open_ai_client import OpenAIClient


class RecursiveHour:

    @staticmethod
    async def request(agent_name: str, agent_summary: str, agent_wake_up_hour: int, day_number: int, current_hour: int,
                      world_nodes: str, relevant_memories: str, recent_actions: str, ):
        actions = str.join(', ', availableActions)
        response = await OpenAIClient.ask(
            messages=[
                SystemMessage('You are controlling an NPC inside a video game simulation.'),
                SystemMessage('Use a 24 hour format.'),
                SystemMessage(f'The world is represented as a tree and it contains the following, where the first '
                              f'element is the root: {world_nodes}'),
                SystemMessage(f'Keep the answer simple and precise, using only one sentence.'),
                SystemMessage(
                    f'Everything the agent plans to do, should be able to be decomposed into a single or a combination of '
                    f'actions from this collection: {actions}'),
                SystemMessage(
                    f'Try not to repeat the recent actions in a short period of time. Make actions seem believable for their specified hour.'
                ),
                SystemMessage(
                    f'Actions should reflect a realistic human behaviour based on the memories and the previous actions. For example, a human would not repeat the exact same action again after one hour.'
                ),
                SystemMessage(f'A summary of relevant memories for the agent: {relevant_memories}') if len(
                    relevant_memories) > 0 else None,
                SystemMessage(f'Most recent actions: {recent_actions}'),
                SystemMessage(f'{agent_name} usually wakes up at {agent_wake_up_hour} and starts the morning routine.'),
                SystemMessage(f'A brief summary of the controlled agent: {agent_summary}'),
                UserMessage(f"It is day {day_number} and hour {current_hour}. Describe in a few words what is the agent planning to do "
                            f"until next hour, taking into account his memories. Mention the time interval for the plan. The agent can do one or multiple tasks in an hour."),
            ],
        )
        return response.content
