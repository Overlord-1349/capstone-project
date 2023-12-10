from src.gateways.OpenAIGateway import OpenAIGateway

__INSTRUCTIONS__ = """This is time of the year to do appraisals, and you will be helping us to do the appraisal.  First collect the employee ID, then ask how do they feel about their supervisor, balance between home and office work.
"""


class Assistant:
    def __init__(self, openai_gateway: OpenAIGateway, *args) -> None:
        self.openai_gateway = openai_gateway
        self.assistant = openai_gateway.create_assistant(
            name="Lumalee",
            instructions=__INSTRUCTIONS__,
            tools=[{"type": "code_interpreter"}],
        )
        self.thread = openai_gateway.client.beta.threads.create()
        openai_gateway.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content="Hey there"
        )

    def __enter__(self, *_) -> None:
        self.run = self.openai_gateway.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )
        print(self.openai_gateway.client.beta.threads.runs.retrieve(
            thread_id=self.thread.id,
            run_id=self.run.id
        ))

    def __exit__(self, *_) -> None:
        print(self.openai_gateway.client.beta.threads.messages.list(
            thread_id=self.thread.id
        ))
