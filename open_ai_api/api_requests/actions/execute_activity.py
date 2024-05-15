from open_ai_api import *
from open_ai_api.api_requests.actions.generic_action import GenericAction
from open_ai_api.api_requests.actions.tools.execute_action import ExecuteAction
from open_ai_api.api_requests.actions.tools.interact_action import InteractAction
from open_ai_api.api_requests.actions.tools.move_to_location import MoveToLocation


class ExecuteActivity:

    @staticmethod
    async def request(action: str, agent_name: str, agent_summary: str, world_nodes: str, current_location: str, duration: int, action_type: str):
        response = await GenericAction.request(
            messages=[
                SystemMessage(f'The world is represented as a tree and it contains the following, where the first '
                              f'element is the root: {world_nodes}'),
                UserMessage(f'You are controlling agent: {agent_name}'),
                UserMessage(f'Summary of the controlled agent: {agent_summary}'),
                UserMessage(f'Current location: {current_location}'),
                UserMessage(f'Call the most appropriate functions to execute the following action: {action} with the duration '
                            f'of {duration} minutes')
            ],
            tools=[
                ExecuteAction,
            ],
        )
        return response


# class ExecuteActivity:
#
#     @staticmethod
#     async def request(action: str, agent_name: str, agent_summary: str, world_nodes: str, current_location: str, duration: int):
#         response = await GenericAction.request(
#             messages=[
#                 SystemMessage(f'The world is represented as a tree and it contains the following, where the first '
#                               f'element is the root: {world_nodes}'),
#                 UserMessage(f'You are controlling agent: {agent_name}'),
#                 UserMessage(f'Summary of the controlled agent: {agent_summary}'),
#                 UserMessage(f'Current location: {current_location}'),
#                 UserMessage(f'Call the most appropriate functions to execute the following action: {action} with the duration '
#                             f'of {duration} minutes')
#             ],
#             tools=[
#                 MoveToLocation,
#                 InteractAction,
#             ],
#         )
#         return response
