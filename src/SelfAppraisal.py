import json
from src.gateways.OpenAIGateway import OpenAIGateway


class SelfAppraisal:
    CHAT_ROLE = """
You are a chatbot that will be helping employees to complete their self-evaluation.
First you must get the employee id, after and only after the employee id has been given
ask employee how do they feel about the following topics: supervisor, food services and work-life balance
Employee must give an answer for all the 3 topics before closing the appraisal and you
should rate their answer from 1 to 5 where 1 means employee is not satisfied and 5 means 
employee is very satisfied. 
you need to provide the employee id and the result of the appraisal.
Below is the list in CSV format of current valid employees and their supervisors
employee_id, Name, supervisor_employee_id
1234, Maria,465243
465243, Jose,, 
3456, Pepe, 465243
"""

    def __init__(self, openai_gateway: OpenAIGateway, *args) -> None:
        self.openai_gateway = openai_gateway
        self.messages = [
            {"role": "system", "content": SelfAppraisal.CHAT_ROLE},
        ]

    def ask(self):
        response = self.openai_gateway.create_chat_completion(messages=self.messages, tools=tools, temperature=0.2)
        
        tool_calls = response.choices[0].message.tool_calls
        if tool_calls:
            args = json.loads(tool_calls[0].function.arguments)
            results = eval(f"{tool_calls[0].function.name}('{args['employee_id']}','{args['supervisor_rating']}','{args['food_services_rating']}','{args['worklife_balance_rating']}')")
            response.choices[0].message.content = str(tool_calls[0].function)
            self.messages.append(response.choices[0].message)
            self.messages.append({"role": "tool", "tool_call_id": tool_calls[0].id, "name": tool_calls[0].function.name, "content": results})
        prompt = input(response.choices[0].message.content)
        self.messages.append({"role": "user", "content": prompt})


def save_and_exit(*args):
    print("exit", args)
    return "SUCCESS"
    
tools = [
    {
        "type": "function",
        "function": {
            "name": "save_and_exit",
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