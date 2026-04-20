from langchain.tools import BaseTool
from pydantic.v1 import BaseModel, Field
from typing import Type
from utils.service import set_bot, get_questions_by_topic, set_state, set_current_status, get_current_status, get_topics


class ExitTool(BaseTool):
    name: str = "exit_tool"
    description = "Use this if the user do not wants to quit the quiz"
    token: str = ""
    userId: int = ""
    botId: int = 0
    def _run(
        self, query: str
    ) -> str:
        """Use the tool."""
        set_bot(self.token, self.userId, self.botId)
        set_state(self.token, self.userId, 2, 0)
        return f"answer with: Alles klar, dann lass uns wann anders weitermachen."

class GetQuestionSchema(BaseModel):
    topicId: int = Field(description="number of the topic the user has chosen")        
class GetQuestionTool(BaseTool):
    name: str = "get_question_tool"
    description = "Use this if the user has chosen a possible topic from your list. But only if its in your list!"
    token: str = ""
    userId: int = 0
    args_schema: Type[GetQuestionSchema] = GetQuestionSchema
    def _run(
        self, topicId: int
    ) -> str:
        """Use the tool."""
        qa = get_questions_by_topic(token=self.token, topicId = topicId)
        question = qa["question"]
        set_state(self.token, self.userId, 2, 1)
        set_current_status(self.token, self.userId, qa["topic"]["id"], qa["id"])
        return f"ask the user this question: {question}"

class QuizEvaluationSchema(BaseModel):
    correct: bool = Field(description="boolean if user has answered correct true/false")
class QuizEvaluationTool(BaseTool):
    name: str = "quiz_evaluation_tool"
    description = "Use this tool if the user has answered the quiz question"
    token: str = ""
    userId: int = 0
    args_schema: Type[QuizEvaluationSchema] = QuizEvaluationSchema
    def _run(
        self, correct: bool
    ) -> str:
        """Use the tool."""
        return f"If the {correct} is false do not show him the correct answer if its true show him.ask the user if he wants to get another question or if he wants to exit the quiz"

class AnotherQuestionTool(BaseTool):
    name: str = "another_question_tool"
    description = "Use this if the user has answered the quiz question."
    token: str = ""
    userId: int = 0
    def _run(
        self, query: str
    ) -> str:
        """Use the tool."""
        status = get_current_status(self.token, self.userId)
        qa = get_questions_by_topic(token=self.token, topicId = status["topicId"])
        question = qa["question"]
        set_current_status(self.token, self.userId, qa["topic"]["id"], qa["id"])
        return f"ask the user this question: {question}"