from open_ai_api.api_requests.actions.tools.tool_function import ToolFunction

MoveToLocation = ToolFunction(
    name='MoveToLocation',
    description='Move the agent to a specific location, zone, room, ...',
    parameters={
        'destination': {
            'type': 'string',
            'description': 'The destination where we want the agent to arrive, given as a full path in the WorldTree from '
                           'the root to the location itself, separated by : and always starts with the root'
        },
        'speed': {
            'type': 'integer',
            'description': 'A number between 1 and 10, where 1 is walking very slowly, 4 is normal walking and 10 is running, '
                           'representing the agent speed. This parameter is required and should always be present.'
        },
        'duration': {
            'type': 'integer',
            'description': 'The number of minutes needed to stay at the location. This is the total duration described in the '
                           'task specification.'
        },
        'reason': {
            'type': 'string',
            'description': 'Why the agent took this action, told from the agent\'s perspective.'
        },

    }
).format()
