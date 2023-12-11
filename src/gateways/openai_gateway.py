from typing import List
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletion


class OpenAIGateway:
    MODEL = "gpt-3.5-turbo-1106"

    @property
    def client(self):
        return self._client

    def __init__(self, key: str) -> None:
        self._client = OpenAI(api_key=key)

    def create_chat_completion(self, messages: List[ChatCompletionMessageParam], **args) -> ChatCompletion:
        return self.client.chat.completions.create(
            model=OpenAIGateway.MODEL,
            messages=messages,
            **args,
        )
