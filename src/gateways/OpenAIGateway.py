from typing import List, Dict
from openai import OpenAI


class OpenAIGateway:
    MODEL = "gpt-3.5-turbo-1106"

    @property
    def client(self):
        return self._client

    def __init__(self, key: str) -> None:
        self._client = OpenAI(api_key=key)

    def create_assistant(self, name: str, instructions: str, tools: List[Dict]):
        return self._client.beta.assistants.create(
            name=name,
            instructions=instructions,
            tools=tools,
            model=OpenAIGateway.MODEL
        )
