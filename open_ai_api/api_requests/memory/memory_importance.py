from open_ai_api import *


class MemoryImportance:

    @staticmethod
    async def request(memory: str):
        response = await OpenAIClient.ask(
            messages=[
                SystemMessage('The answer must be a number, between 1 and 10, that represents the given rating. There should '
                              'be no words used in the response.'),
                UserMessage(f"On the scale of 1 to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is "
                            f"extremely important and emotional (e.g., a break up, college acceptance), rate the likely "
                            f"importance of the"
                            f"following piece of memory. Memory: {memory}"
                            f" Rating: <fill in>"),
            ],
        )
        return response.content
