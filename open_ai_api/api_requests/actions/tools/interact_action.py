from open_ai_api.api_requests.actions.tools.tool_function import ToolFunction

InteractAction = ToolFunction(
    name='InteractAction',
    description='Interact with a specific object from the world nodes. Locations cannot be interacted with, only objects, furniture and devices. '
                'This interaction differs from object to object,'
                'for example, interacting with bed would make the agent lay on the bed, sit on a chair or sofa, and interacting with a coffee machine '
                'will make the agent use the coffee machine to make a coffee. Basically if the Agent wants to do something on or with an object, the agent should interact with it.',
    parameters={
        'destination': {
            'type': 'string',
            'description': 'The destination object that we want our agent to interact with, given as a full path in the WorldTree from '
                           'the root of the WorldTree to the target itself, separated by : and always starts with the root. You must only use locations from the worldTree without altering or adding anything.'
        },
        'speed': {
            'type': 'integer',
            'description': 'A number between 1 and 10, where 1 is walking very slowly, 4 is normal walking and 10 is running, '
                           'representing the agent speed. This parameter is required and should always be present. This is the speed used to move in range to the object, if the agent is not already there.'
        },
        'duration': {
            'type': 'integer',
            'description': 'The number of minutes needed to interact with the object. This is the total duration described in the '
                           'task specification.'
        },
        'reason': {
            'type': 'string',
            'description': 'Why the agent took this action, told from the agent\'s perspective.'
        },

    }
).format()
