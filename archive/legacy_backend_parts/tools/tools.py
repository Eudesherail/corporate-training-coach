from langchain.agents import Tool
from langchain.tools import YouTubeSearchTool, WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import tool, BaseTool
import os

from pydantic.v1 import BaseModel, Field
from typing import Optional, Type
from datetime import datetime

from utils.service import delete_session, set_bot, set_goal, get_questions_by_topic, DB, set_state, set_current_status, get_current_status, get_topics
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores.pgvector import PGVector
from langchain.chains import RetrievalQA
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


@tool
def ask_wiss(query: str) -> str:
    """prüfe immer dieses dieses Tool, wenn dir eine Frage gestellt wird, um zu sehen, ob in dem Dokument eine Antwort auf die Frage steckt! und ergänze die Antwort, wenn es sein muss"""
    result = getVector(query, "MeineDokumenten")
    return result

@tool
def ask_winfo1(query: str) -> str:
    """Use this tool if the user has a question about digital transformations and services"""
    result = getVector(query, "winfo1")
    return result

@tool
def ask_features(query: str) -> str:
    """Use this tool if the user wants to know what you can do"""
    return "Tell the user that you can help him to define a smart goal, do a quiz with him or answer question about different topics"


youtube = YouTubeSearchTool()

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

def getVector(query: str, collection: str):
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    embeddings = OpenAIEmbeddings(
        openai_api_key=openai_api_key
    )
    CONNECTION_STRING = DB
    COLLECTION_NAME = collection
    store = PGVector(
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
    )
    retriever = store.as_retriever()
    llm = OpenAI(openai_api_key=openai_api_key,
    temperature=0, model='gpt-3.5-turbo-instruct', max_tokens=700)
    ruff = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever
    )
    result = ruff.run(query)
    return result


# tool to delete the message history of the user
class DeleteTool(BaseTool):
    name: str = "delete_tool"
    description = "useful when the user wants to delete his message history"
    number: str = ""
  
    def _run(
        self, query: str
    ) -> str:
        """Use the tool."""
        delete_session(self.number)
        return f"Dein Nachrichtenverlauf wurde gelöscht"


class SmartGoalTool(BaseTool):
    name: str = "smart_goal"
    description = "useful when the user wants to define a goal"
    token: str = ""
    userId: int = ""
    botId: int = 1
    def _run(
        self, query: str
    ) -> str:
        """Use the tool."""
        set_bot(self.token, self.userId, self.botId)
        return f"answer exactly with: Es ist sinnvoll seine Ziele smart zu formulieren. Weißt du was smarte Ziele sind?"

class QuizTool(BaseTool):
    name: str = "quiz_tool"
    description = "useful when the user do a quiz"
    token: str = ""
    userId: int = ""
    botId: int = 2
    def _run(
        self, query: str
    ) -> str:
        """Use the tool."""
        set_bot(self.token, self.userId, self.botId)
        topics = get_topics(self.token)
        topicsSting = '\n'.join([f"{item['id']}. {item['name']}" for item in topics])
        return f"answer exactly with: Zu welchem Thema würdest du denn gerne ein Quizt machen 🎮? /n {topicsSting}"

class ExtractGoalSchema(BaseModel):
    goal: str = Field(description="schould be the smart goal with all relevant infomations like the relevance of the goal")
    date: str = Field(description="dateToday is the acutal date today. Date should be the extracted enddate for the goal in the format yyyy-mm-dd")

class ExtractGoal(BaseTool):
    name: str = "extract_goal_tool"
    description = "Use this if you have defined a smart goal with the user."
    token: str = ""
    userId: int = ""
    botId: int = 0
    dateToday = datetime.now().date()
    args_schema: Type[ExtractGoalSchema] = ExtractGoalSchema
    def _run(
        self, goal: str, date: str
    ) -> str:
        """Use the tool."""
        set_bot(self.token, self.userId, self.botId)
        set_goal(self.token, self.userId, goal, date)
        return f"answer with: Super ich habe dein Ziel {goal} gespeichert"

class ExitTool(BaseTool):
    name: str = "exit_tool"
    description = "Use this if the user do not want to define a smart goal anymore"
    token: str = ""
    userId: int = ""
    botId: int = 0
    def _run(
        self, query: str
    ) -> str:
        """Use the tool."""
        set_bot(self.token, self.userId, self.botId)
        return f"answer with: Alles klar, dann vielleicht ein anderes mal."
