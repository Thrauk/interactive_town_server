from open_ai_api import OpenAIClient, SystemMessage, UserMessage


class RecentActionSummary:

    @staticmethod
    async def request(agent_name: str, agent_summary: str, recent_actions: str, world_nodes: str, current_time:str,):
        response = await OpenAIClient.ask(
            messages=[
                UserMessage('You are controlling an NPC inside a video game simulation.'),
                UserMessage('Use a 24 hour format.'),
                UserMessage(f'The world is represented as a tree and it contains the following, where the first '
                            f'element is the root: {world_nodes}'),
                UserMessage(f'Give only the answer and avoid giving any extra explanations or dialogue.'),
                UserMessage(f'The recent actions belong to {agent_name}. Quick summary for this person: {agent_summary}'),
                UserMessage(f'The time now is: {current_time}.'),
                UserMessage(f'Generate a summary of what has he done so far, from this list of recent activities: {recent_actions}.')
            ],
        )
        return response.content
