from langchain.agents import Tool
from langchain_community.tools import YouTubeSearchTool, DuckDuckGoSearchRun
from langchain.tools import tool, BaseTool

from pydantic.v1 import BaseModel, Field
from typing import Optional, Type
from datetime import datetime
from dotenv import load_dotenv
import os
from users.models import User, Goal  
from agents.models import State, Agent 
from quiz.models import Topic

from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain.vectorstores.pgvector import PGVector
from langchain.chains import RetrievalQA
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
# Load the environment variables from the .env file
env_path="../.env"
load_dotenv(env_path)

# Database connection string for PostgresChatMessageHistory
DB = os.getenv('DATABASE_URL')

def load_environment_variable(env_path="../.env"):
    load_dotenv(env_path)
    openai_key = os.getenv('OPENAI_KEY')
    if not openai_key:
        raise EnvironmentError("OPENAI_KEY not found in environment variables")
    return openai_key

# tool to answer questions about the Studienbrief Wissenschaftliches Arbeiten
@tool
def ask_wiss(query: str) -> str:
    """Nutze dieses Tool wenn der Nutzer Fragen zu wissenschaftlichem Arbeiten hat"""
    result = getVector(query, "meinedokumenten")
    return result

@tool
def ask_winfo1(query: str) -> str:
    """Use this tool if the user has a question about digital transformations and services"""
    result = getVector(query, "meinedokumenten")
    return result

@tool
def ask_features(query: str) -> str:
    #"""Use this tool if the user wants to know what you can do"""
    """Briefly outlines the agent's main functions in response to user inquiries about capabilities."""
    return "Du kannst dem Nutzer helfen ein smartes Ziel festzulegen, ein Quiz zu machen oder ihm einfach nur ein paar Informationen zu geben."


youtube = DuckDuckGoSearchRun()

def getVector(query: str, collection: str):
    embeddings = OpenAIEmbeddings(
        openai_api_key=load_environment_variable()
    )
    CONNECTION_STRING = DB
    COLLECTION_NAME = collection
    store = PGVector(
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
    )
    retriever = store.as_retriever()
    llm = OpenAI(openai_api_key=load_environment_variable(),
    temperature=0, model='gpt-3.5-turbo-instruct', max_tokens=700)
    ruff = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever
    )
    result = ruff.invoke(query)
    return result

# tool to change the current agent to the goal agent
class SmartGoalTool(BaseTool):
    name: str = "smart_goal"
    description = "Useful for when you want to define or update a goal. No input needed."
    userId: int = ""
    def _run(
        self, query: str
    ) -> str:
        """
        Activate the SmartGoalTool when the user indicates a desire to set or define a goal.
        """
        agent = Agent.objects.get(name='goal')
        state, created = State.objects.update_or_create(
            user=self.userId,
            defaults={'current_state': 0,
            'agent': agent}  
        )
        return "Es ist sinnvoll seine Ziele smart zu formulieren. Weißt du was smarte Ziele sind?"

# tool to change the current agent to the goal agent
class QuizTool(BaseTool):
    name: str = "quiz_tool"
    description = "useful for making a quiz. No input needed. If the user has already defined a goal ask him if he wants to change it before using this tool"
    userId: int = ""
    def _run(
        self, query: str
    ) -> str:
        """Use the tool."""
        agent = Agent.objects.get(name='quiz')
        state, created = State.objects.update_or_create(
            user=self.userId,
            defaults={'current_state': 0,
            'agent': agent}  
        )
        topics = Topic.objects.all().values()
        print(topics)
        topicsSting = '\n'.join([f"{item['id']}. {item['name']}" for item in topics])
        print(topicsSting)
        return f"Zu welchem Thema würdest du denn gerne ein Quiz machen 🎮? /n {topicsSting}"


# tool to exit the current agent and return to the base agent
class ExitTool(BaseTool):
    name: str = "exit_tool"
    description = "Use this if the user do not want to define a smart goal anymore"
    userId: int = ""
    botId: int = 0
    def _run(
        self, query: str
    ) -> str:
        """Use the tool."""
        agent = Agent.objects.get(name='base')
        created = State.objects.update_or_create(
            user=self.userId,
            defaults={'current_state': 0,
            'agent': agent}  
        )
        return f"Alles klar, dann vielleicht ein anderes mal."
