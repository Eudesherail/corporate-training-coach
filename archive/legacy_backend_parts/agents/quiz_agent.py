from agents.agent import AgentHandler
import tools.tools as tools
import tools.quiz_tools as quizTools
from prompts.quiz import template, template2
from utils.service import get_current_status, get_question_by_id, get_topics
from utils.logger import setup_logger

class AgentClass(AgentHandler):
    logger = setup_logger(__name__)

    # Create Quiz Bot
    def __init__(self, state, information="", history="", userId="", token=""):
        self.tool_list = [
            quizTools.ExitTool(
                description="Use this if the user wants to exit the quiz",
                userId=userId, 
                token=token),
            quizTools.GetQuestionTool(token=token, userId=userId)
        ]
        prompt = ""
        if state == 0:
            prompt = self.template1(token)
        elif state == 1:
            prompt = self.get_qa(token, userId)
            self.tool_list = [
                quizTools.ExitTool(userId=userId, token=token),
                quizTools.QuizEvaluationTool(token=token, userId=userId),
                quizTools.AnotherQuestionTool(token=token, userId=userId)
            ]
        self.prompt = prompt
        super().__init__(
            prompt=self.prompt,
            model="gpt-4-1106-preview",
            tool_list=self.tool_list,
            history=history,
            information=information,
            userId=userId,
            token=token,
            state=state,
        )

    # Function to execute the Agent
    def execute(self, message):
        try:
            answer = self.agent.invoke({"input": message})
            return answer["output"]
        except Exception as e:
            self.logger.error(f"Error during execution: {e}")
            return "An error occurred during execution. Please report this issue."

    def template1(self, token: str):
        try:
            topics = get_topics(token)
            topicsString = '\n'.join([f"{item['id']}. {item['name']}" for item in topics])
            prompt = template.replace("{topics}", topicsString)
            return prompt
        except Exception as e:
            self.logger.error(f"Error in template1: {e}")
            return "Error in generating topics list."

    def get_qa(self, token: str, userId: int):
        try:
            status = get_current_status(token, userId)
            qa = get_question_by_id(token, status["questionId"])
            prompt = template2.replace("{query}", qa["question"]).replace("{answer}", qa["answer"])
            return prompt
        except Exception as e:
            self.logger.error(f"Error in get_qa: {e}")
            return "Error in generating question and answer."
