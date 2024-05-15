from openai import AsyncOpenAI
from decouple import config
from typing import List

from open_ai_api import SystemMessage, UserMessage


class OpenAIClient:
    client = AsyncOpenAI(api_key=config('OPENAI_API_KEY'))

    @staticmethod
    async def ask(messages: List, tools=None, max_tokens=4000, model="gpt-3.5-turbo"):
        processed_messages = list(filter(lambda item: item is not None, messages))
        system_messages = []
        user_messages = ''

        for message in processed_messages:
            if isinstance(message, SystemMessage):
                system_messages.append(message.json())
            elif isinstance(message, UserMessage):
                user_messages += message.content + ' '

        # final_messages = [
        #     SystemMessage(system_messages).json(),
        #     UserMessage(user_messages).json(),
        # ]

        final_messages = system_messages + [UserMessage(user_messages).json()]

        response = await OpenAIClient.client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            # messages=list(map(lambda x: x.json(), processed_messages)),
            messages=final_messages,
            tools=tools,
            temperature=0
        )
        return response.choices[0].message
