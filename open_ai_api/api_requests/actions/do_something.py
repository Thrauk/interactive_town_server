from open_ai_api import *
from open_ai_api.api_requests.actions.generic_action import GenericAction
from open_ai_api.api_requests.actions.tools.execute_action import ExecuteAction, availableActions
from open_ai_api.api_requests.actions.tools.interact_action import InteractAction
from open_ai_api.api_requests.actions.tools.move_to_location import MoveToLocation

response_template = '''
{
	"destination" : "WorldRoot:Location1:Location2:Destination",
	"speed" : 4,
	"duration" : 10,
	"reason" : "Agent wants to take a shower",
	"action" : "shower"
}

/*
WHERE: 
destination: The destination object that we want our agent to interact with, given as a full link in the WorldTree from '
                           'the root of the WorldTree to the target itself, separated by : and always starts with the root (the first element in the WorldTree representation). You must only use locations from the worldTree without altering or adding anything. EXAMPLE OUTPUT WorldRoot:Location1:Location2:Destination
speed: specified in the request
duration: specified in the reuqest
reason: Why the agent took this action, told from the agent\'s perspective.
action: the most relevant from the following:
''' + f'[{str.join(", ", availableActions)}] \n*/'


class DoSomething:

    @staticmethod
    async def request(action: str, agent_name: str, agent_summary: str, world_nodes: str, current_location: str, duration: int):
        response = await OpenAIClient.ask(
            messages=[
                SystemMessage(f'The world is represented as a tree and it contains the following, where the first '
                              f'element is the root: {world_nodes}'),
                SystemMessage(f'The output should be in JSON format without any other comments or explanations, following this template: {response_template}'),
                SystemMessage(f'Selected action must be done in the exact selected location. For example, you would brush teeth near the sink, not anywhere in the bathroom'),
                UserMessage(f'You are controlling agent: {agent_name}'),
                UserMessage(f'Summary of the controlled agent: {agent_summary}'),
                UserMessage(f'Current location: {current_location}'),
                UserMessage(f'{agent_name} wants to do this: {action}. The speed is 4, the duration is {duration}. Select the best destination and action and give the response in the required JSON format. The destination must be as specified, a path/link from this world nodes tree: {world_nodes}, separated by :, that starts with the first node (root) and goes all the way down to the destination without skipping any node. The names are case sensitive, avoid changing at all cost.')
            ],
        )
        return response.content

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
