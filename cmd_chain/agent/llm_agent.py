"""
LLM Agent class for managing the LLM-based agent with dynamic tools.
"""

from typing import List, Optional
import os
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph.types import RunnableConfig
from fastapi import HTTPException
from cmd_chain.agent.config import settings


class LLMAgent:
    """
    Custom class for managing the LLM-based agent with dynamic tools.

    Attributes:
        memory (MemorySaver): The agent's memory handler.
        model (ChatOpenAI): The OpenAI model used by the agent.
        tools (List): List of tools available to the agent.
        agent_executor: The agent executor initialized with tools and model.
    """

    def __init__(
        self,
        root_dir: Optional[str] = None,
        extra_tools: Optional[List] = None,
        memory: Optional[MemorySaver] = None,
    ):
        """
        Initializes the LLMAgent with the specified parameters.

        Args:
            root_dir (str): The root directory for file management tools.
            extra_tools (List): Additional tools to be added to the agent's toolkit.
            memory (MemorySaver): The memory handler for the agent.

        NOTE: The default tools include DuckDuckGo search and file management tools.
        """
        if not settings.openai or not settings.openai.api_key:
            raise ValueError("OpenAI configuration is missing")
        self.model = ChatOpenAI(
            api_key=settings.openai.api_key,
            model=settings.openai.model or "gpt-3.5-turbo",
        )

        self.memory = memory if memory is not None else MemorySaver()

        if not root_dir:
            root_dir = os.getcwd()
        fs_tools = FileManagementToolkit(root_dir=root_dir).get_tools()
        search = DuckDuckGoSearchRun()
        self.tools = [search, *fs_tools]
        if extra_tools:
            self.tools.extend(extra_tools)
        self.agent_executor = create_react_agent(
            self.model, self.tools, checkpointer=self.memory
        )

    def reset_memory(self):
        """
        Resets the memory of the agent.
        """
        self.memory = MemorySaver()

    def add_tool(self, tool):
        """
        Adds a new tool to the agent's toolkit.

        Args:
            tool: The tool to be added.
        """
        self.tools.append(tool)

    def process_request(self, msg: str) -> str:
        """
        Processes the user request using the agent.

        Args:
            msg (str): The user's message to be processed.

        Returns:
            str: The response from the agent.
        """
        config = RunnableConfig(configurable={"thread_id": "abc123"})
        response = ""
        try:
            for chunk in self.agent_executor.stream(
                {"messages": [HumanMessage(content=msg)]}, config
            ):
                if "agent" in chunk:
                    response += (
                        "[AGENT] " + chunk["agent"]["messages"][0].content + "\n"
                    )
                elif "tools" in chunk:
                    response += "TOOL" + chunk["tools"]["messages"][0].content + "\n"
                else:
                    response += str(chunk) + "\n"
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e
        return response.strip()
