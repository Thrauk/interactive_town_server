from open_ai_api.api_requests.actions.tools.tool_function import ToolFunction

availableActionsModern = [
    'sit',
    # 'lay',
    'sleep',
    'shower',
    'make_coffee',
    'watch_tv',
    #'make_bbq',
    'throw_thrash',
    'wash_clothes',
    'brush_teeth',
    'look_mirror',
    'change_clothes',
    'physical_exercise',
    'stretch',
    'dance',
    'eat',
    #'make_breakfast',
    'cook',
    'use_fridge',
    # 'move_to',
    'read',
    'drink',
    'greet',
    'get_food_ingredients',
    'work',

]

availableActions = [
    'sit',
    # 'lay',
    'sleep',
    'shower',
    # 'make_coffee',
    # 'watch_tv',
    #'make_bbq',
    # 'throw_thrash',
    # 'wash_clothes',
    # 'brush_teeth',
    # 'look_mirror',
    'change_clothes',
    'physical_exercise',
    'stretch',
    # 'dance',
    'eat',
    #'make_breakfast',
    'cook',
    # 'use_fridge',
    # 'move_to',
    'read',
    'drink',
    # 'greet',
    'get_food_ingredients',
    'use_forge_furnace',
    'use_anvil',
    'gardening',
    'feed_animals'

]


ExecuteAction = ToolFunction(
    name='ExecuteCustomAction',
    description='Makes the agent executes a specific action, like moving, cooking, drinking, sitting, and so on',
    parameters={
        'destination': {
            'type': 'string',
            'description': 'The destination object that we want our agent to interact with, given as a full link in the WorldTree from '
                           'the root of the WorldTree to the target itself, separated by : and always starts with the root. You must only use locations from the worldTree without altering or adding anything. EXAMPLE OUTPUT WorldRoot:Location1:Location2:Destination'
        },
        'speed': {
            'type': 'integer',
            'description': 'A number between 1 and 10, where 1 is walking very slowly, 4 is normal walking and 10 is running, '
                           'representing the agent speed. This parameter is required and should always be present. This is the speed used to move in range to the object, if the agent is not already there.'
        },
        'duration': {
            'type': 'integer',
            'description': 'The number of minutes needed for the agent to execute the duration. In case of moving, '
                           'this duration represents how much the agent should wait at the target.'
        },
        'reason': {
            'type': 'string',
            'description': 'Why the agent took this action, told from the agent\'s perspective. What is the agent doing?'
        },
        'action': {
            'type': 'string',
            'description': 'The selected action that is going to be executed by the agent. To be noted, for any action where '
                           'the agent is not in range, the agent will automatically move to the destination before executing'
                           ' the action.',
            'enum': availableActions,
        }

    }
).format()
