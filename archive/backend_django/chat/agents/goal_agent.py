from chat.agents.agent import AgentHandler
from chat.tools.goal_tools import ExtractGoal, ExitTool
from chat.prompts.goal_prompt import template
from datetime import datetime

class AgentClass(AgentHandler):

    def __init__(self, state: int, information="", history="", userId="", token = ""):
        tool_list = [
            ExtractGoal(userId=userId),
            ExitTool(userId=userId),
        ]
        current_date = datetime.now().date()
        prompt = template.replace("{date}", str(current_date))
        super().__init__(
            prompt=prompt,
            model="gpt-4-turbo-preview",
            tool_list=tool_list,
            history=history,
            information=information,
            userId=userId,
            state=state,
        )

    def execute(self, message):
        try:
            answer = self.agent.invoke({"input": message})
            return answer["output"]
        except Exception as e:
            return "Es ist tut mir leid, ich hab dich nicht verstanden! 😧 Könntest du das vielleicht nochmal anders formulieren?"


