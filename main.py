import sys
from pathlib import Path
from src.SelfAppraisal import SelfAppraisal
from src.gateways.OpenAIGateway import OpenAIGateway


sys.path.append(Path(__file__).parent)
with open("key.txt", "r") as fh:
    key = fh.read()

self_appraisal = SelfAppraisal(OpenAIGateway(key))

for _ in range(0, 10):
    self_appraisal.ask()