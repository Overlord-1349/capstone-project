import json
from src.gateways.openai_gateway import OpenAIGateway
from src.report import Report
from openai.types.chat import ChatCompletion


class FeedbackSurvey:
    CHAT_ROLE = """
You are a chatbot that will be helping employees to complete a survey.
First you must get the employee id, after and only after the employee id has been given
ask employee how do they feel about the following topics: supervisor, food services and work-life balance
Employee must give an answer for all the 3 topics before closing the appraisal and you
should rate their answer from 1 to 5 where 1 means employee is not satisfied and 5 means 
employee is very satisfied. 
you need to provide the employee id and the result of the appraisal.
Below is the list in CSV format of current valid employees and their supervisors
"""

    def __init__(self, openai_gateway: OpenAIGateway) -> None:
        self.openai_gateway = openai_gateway
        content = f'{FeedbackSurvey.CHAT_ROLE}\n{Report.read("employees.csv")}'
        self.messages = [
            {"role": "system", "content": content},
        ]
        self._continue = True

    def start(self):
        while self._continue:
            self.next()

    def next(self):
        response = self.openai_gateway.create_chat_completion(messages=self.messages, tools=tools, temperature=0.8)
        self._call_function(response)
        print(response.choices[0].message.content)
        prompt = input("answer: ")
        self.messages.append({"role": "user", "content": prompt})

    def _call_function(self, response: ChatCompletion):
        tool_calls = response.choices[0].message.tool_calls
        if not tool_calls:
            return
        args = json.loads(tool_calls[0].function.arguments)
        results = eval(f"{tool_calls[0].function.name}('{args['employee_id']}','{args['supervisor_rating']}','{args['food_services_rating']}','{args['worklife_balance_rating']}')")
        response.choices[0].message.content = str(tool_calls[0].function)
        self.messages.append(response.choices[0].message)
        self.messages.append({"role": "tool", "tool_call_id": tool_calls[0].id, "name": tool_calls[0].function.name, "content": results})
        self.openai_gateway.create_chat_completion(messages=self.messages, tools=tools)
        self.messages.append({"role": "assistant", "content": "Thanks for your response!"})
        response = self.openai_gateway.create_chat_completion(messages=self.messages, tools=tools)
        print(response.choices[0].message.content)
        self._continue = False
    

def save(*args):
    Report.save(["employee_id", "supervisor_rating", "food_services_rating", "worklife_balance_rating"], args)
    return "SUCCESS"


tools = [
    {
        "type": "function",
        "function": {
            "name": "save",
            "description": "Function to be executed only after the supervisor, food services and work-life balance have been rated by the employee",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "employee's id",
                    },
                    "supervisor_rating": {
                        "type": "string",
                        "description": "employee's supervisor rating",
                    },
                    "food_services_rating": {
                        "type": "string",
                        "description": "food service rating",
                    },
                    "worklife_balance_rating": {
                        "type": "string",
                        "description": "Work-Life balance rating",
                    },
                },
                "required": ["employee_id", "supervisor_rating", "food_services_rating", "worklife_balance_rating"],
            },
        }
    },
]