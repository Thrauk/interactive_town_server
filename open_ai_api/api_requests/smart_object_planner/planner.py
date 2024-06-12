from agent import Agent
from open_ai_api.api_requests.actions.tools.execute_action import availableActions
from open_ai_api.chat_message import *
from open_ai_api.open_ai_client import OpenAIClient

template_old = '''
{
    "target" : "Doing the morning routine",
    "tasks" : [
        {
            "location" : "WorldRoot:Node1:Node2:Destination",
            "task" : "Task description",
            "actions" : [
                {
                    "action" : "brush_teeth",
                    "duration" : 5,
                },
                {
                    "action" : "shower",
                    "duration" : 10,
                },
            ]
        }
        {
            "location" : "WorldRoot:Node1:Node2:Destination2",
            "task" : "Making breakfast.",
            "actions" : [
                {
                    "action" : "get_food",
                    "duration" : 5,
                },
                {
                    "action" : "cook",
                    "duration" : 10,
                },
                {
                    "action" : "eat",
                    "duration" : 25,
                },
            ]
        }
    ]
}

WHERE: 

target: The main target/task the agent wants to do
tasks: The main target split into one or more sub-tasks. Each sub-task can take place only in a single location. The agent is going to move to the specified location each task. The agent can go back and forth if required, but there shouldn't be two consecutive tasks at the same location.

location: The destination that we want our agent to execute a sub-task split into a seris of actions, given as a full link in the WorldTree from '
                           'the root of the WorldTree to the target itself, separated by : and always starts with the root (the first element in the WorldTree representation). You must only use locations from the worldTree without altering or adding anything. EXAMPLE OUTPUT WorldRoot:Location1:Location2:Destination. You must not skip over any Node in the tree, define the path by using every single node in the path.
task: the description of the current task
actions: a list of objects describing the sequence of actions needed in order to complete the task.
reason: Why the agent took this action, told from the agent\'s perspective.
action: the most relevant from the following list:
''' + f'[{str.join(", ", availableActions)}]. \n The selected action must be present in this list, dont use an action not present here.*/' + '''
duration: how long should this action take in minutes. An action should not take more than 20 minutes.
'''

template = '''
EXAMPLE 1
{
    "location" : "WorldRoot:Node1:Node2:Destination",
    "task" : "Task description",
    "actions" : [
        {
            "action" : "brush_teeth",
            "duration" : 5
        },
        {
            "action" : "shower",
            "duration" : 10
        }
    ]
}

EXAMPLE 2
{
    "location" : "WorldRoot:Node1:Node2:Destination2",
    "task" : "Making breakfast.",
    "actions" : [
        {
            "action" : "get_food",
            "duration" : 5
        },
        {
            "action" : "cook",
            "duration" : 10
        },
        {
            "action" : "eat",
            "duration" : 25
        }
    ]
}


WHERE: 


location: The destination that we want our agent to execute a task  given as a full link in the WorldTree from '
                           'the root of the WorldTree to the target itself, separated by : and always starts with the root (the first element in the WorldTree representation). You must only use locations from the worldTree without altering or adding anything. EXAMPLE OUTPUT WorldRoot:Location1:Location2:Destination. You must not skip over any Node in the tree, define the path by using every single node in the path.
task: the description of the current task
actions: a list of objects describing the sequence of actions needed in order to complete the task.
reason: Why the agent took this action, told from the agent\'s perspective.
action: the most relevant from the following list:
''' + f'[{str.join(", ", availableActions)}]. \n The selected action must be present in this list, dont use an action not present here. The action must be doable in the selected location. For example showering or brushing teeth cannot be done in the bedroom, only in the bathroom.*/' + '''
duration: how long should this action take in minutes.
'''

class Planner:

    @staticmethod
    async def request(agent: Agent, day_number: int, current_hour: int,
                      relevant_memories: str, recent_actions: str, today_plan:str):
        actions = str.join(', ', availableActions)
        response = await OpenAIClient.ask(
            messages=[
                SystemMessage('You are controlling an NPC inside a video game simulation.'),
                SystemMessage('Use a 24 hour format.'),
                SystemMessage(f'The world is represented as a tree and it contains the following, where the first '
                            f'element is the root: {agent.world_nodes}'),
                SystemMessage(f'Keep the answer simple and precise, using only one sentence.'),
                SystemMessage(
                    f'Try not to repeat the recent actions in a short period of time. Make actions seem believable for their '
                    f'specified hour.'
                ),
                SystemMessage(
                    f'Actions should reflect a realistic human behaviour based on the memories and the previous actions. For '
                    f'example, a human would not repeat the exact same action again after one hour.'
                ),
                SystemMessage(f'A summary of relevant memories for the agent: {relevant_memories}') if len(
                    relevant_memories) > 0 else None,
                SystemMessage(f'Most recent actions: {recent_actions}. The agent has to take this actions into account, '
                              f'avoiding repeating a action without reason.'),
                SystemMessage(f'His plan for today: {today_plan}. He should take this plan into account when making decisions.'),
                SystemMessage(f'{agent.name} usually wakes up at {agent.wake_up_hour} and starts the morning routine.'),
                SystemMessage(f'A brief summary of the controlled agent: {agent.summary}'),
                SystemMessage(f'At the end of the day or plan, the agent must go to sleep.'),
                SystemMessage(f'Give the answer as a JSON following this template: {template}. Only send the JSON response '
                              f'without using any other text.'),
                SystemMessage(f"Try to split the task in multiple actions if possible. The final action used in the day "
                              f"should be sleep."),
                UserMessage(
                    f"It is day {day_number} and hour {current_hour}. Using the required format, describe what {agent.name} "
                    f"is planning to do now and how is he going to do it."),
            ],
        )
        return response.content
