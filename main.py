import sys
from pathlib import Path
from src.Assistant import Assistant
from src.gateways.OpenAIGateway import OpenAIGateway


print(Path(__file__).parent)
sys.path.append(Path(__file__).parent)
with open("key.txt", "r") as fh:
    key = fh.read()

assistant = Assistant(OpenAIGateway(key))

with assistant as appraisal:
    pass