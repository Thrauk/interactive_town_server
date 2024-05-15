from openai import AsyncOpenAI
from decouple import config

class EmbeddingClient:
    client = AsyncOpenAI(api_key=config('OPENAI_API_KEY'))

    @staticmethod
    async def encode(text, max_tokens=4000, model="text-embedding-3-small"):
        response = await EmbeddingClient.client.embeddings.create(
            model=model,
            input=text,
        )
        return response.data[0].embedding
