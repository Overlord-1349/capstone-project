import sys
import os
from pathlib import Path
from src.feedback_survey import FeedbackSurvey
from src.gateways.openai_gateway import OpenAIGateway


sys.path.append(Path(__file__).parent)

key = os.environ.get("OPENAI_API_KEY")
FeedbackSurvey(OpenAIGateway(key)).start()
