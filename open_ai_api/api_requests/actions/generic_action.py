import json

from open_ai_api import *


class GenericAction:

    @staticmethod
    async def request(messages, tools):
        response = await OpenAIClient.ask(
            messages=[
                         SystemMessage(
                             'Keep the answers simple. Give the answers from the agent perspective. You are controlling an '
                             'NPC inside a video game simulation.'),
                         SystemMessage('Use a 24 hour format.'),
                     ] + messages,
            tools=tools
        )
        ret = []
        for tool in response.tool_calls:
            func = {
                'function': tool.function.name,
                'arguments': tool.function.arguments,
            }
            ret.append(func)
        return ret
