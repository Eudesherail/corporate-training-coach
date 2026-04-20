from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.tools.render import format_tool_to_openai_function

import os
from dotenv import load_dotenv
import importlib

import tools.tools as tools
from utils.logger import setup_logger

logger = setup_logger(__name__)
def load_environment_variables(env_path="../.env"):
    """
    Load environment variables from a specified path.
    Raises an error if essential variables are missing.
    """
    load_dotenv(env_path)
    openai_key = os.getenv('OPENAI_KEY')
    if not openai_key:
        raise EnvironmentError("OPENAI_KEY not found in environment variables")
    return openai_key

class AgentHandler:
    def __init__(self, prompt, model, tool_list, history, information, userId, token, state):
        try:
            # Load openai key
            self.openai_key = load_environment_variables()

            # Create a list of functions fot the bot
            self.tool_list = tool_list
            self.functions = [format_tool_to_openai_function(f) for f in self.tool_list] #convert the langchain to openai functions

            # Create llm and insert functions
            self.llm = ChatOpenAI(
                openai_api_key=self.openai_key,
                temperature=0.0,
                model_name=model
            ).bind(functions=self.functions)

            self.information = information
            self.token = token
            self.userId = userId

            # Create memory
            self.memory = ConversationBufferMemory(
                chat_memory=history, 
                return_messages=True,
                memory_key="chat_history")

            # Create Prompt          
            #prompt = importlib.import_module("prompts." + prompt_name) # Importiert den Prompt dynamisch basierend auf dem übergebenen Namen
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ])

            # Create the AgentChain
            self.chain = RunnablePassthrough.assign(
                agent_scratchpad = lambda x: format_to_openai_functions(x["intermediate_steps"])
            ) | self.prompt.partial(
                tools=self._convert_tools(self.tool_list), 
                tool_names=", ".join(tool.name for tool in self.tool_list),
                user_information=self.information,
            ) | self.llm | OpenAIFunctionsAgentOutputParser()

            self.state = state

            # Create Executor for the Agent
            self.agent = AgentExecutor(agent=self.chain, tools=self.tool_list, verbose=True, memory=self.memory, max_iterations=2,)

        except Exception as e:
            logger.error(f"Error initializing AgentHandler: {e}")
            raise ValueError("An unexpected error occurred during agent initializing.") 

    # Function to make a list of the tool names
    @staticmethod
    def _convert_tools(tools):
        return "\n".join(f"{tool.name}: {tool.description}" for tool in tools)