import sys
import os
from pathlib import Path
from src.SelfAppraisal import SelfAppraisal
from src.gateways.OpenAIGateway import OpenAIGateway


sys.path.append(Path(__file__).parent)

key = os.environ.get("OPENAI_API_KEY")
SelfAppraisal(OpenAIGateway(key)).start()