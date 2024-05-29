from openai import AsyncOpenAI
from decouple import config
from typing import List

from open_ai_api import SystemMessage, UserMessage

default_model = 'gpt-4o'
# default_model = 'gpt-3.5-turbo'

class OpenAIClient:
    client = AsyncOpenAI(api_key=config('OPENAI_API_KEY'))

    @staticmethod
    async def ask(messages: List, tools=None, max_tokens=4000, model=default_model):
        processed_messages = list(filter(lambda item: item is not None, messages))
        system_messages = []
        user_messages = ''

        for message in processed_messages:
            if isinstance(message, SystemMessage):
                system_messages.append(message.json())
            elif isinstance(message, UserMessage):
                user_messages += message.content + ' '

        final_messages = system_messages + [UserMessage(user_messages).json()]

        response = await OpenAIClient.client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=final_messages,
            tools=tools,
            temperature=0.001
        )
        return response.choices[0].message
