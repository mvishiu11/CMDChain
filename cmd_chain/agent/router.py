"""
This module defines a FastAPI router for interacting with the LLM-based agent.
The router allows users to send commands to the agent,
which processes the requests and returns a response.
"""

import os

from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi import HTTPException
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

load_dotenv()

router = APIRouter()

# Initialize the agent
memory = MemorySaver()
model = ChatOpenAI(model="gpt-3.5-turbo")
fs_tools = FileManagementToolkit(root_dir=str(os.getcwd())).get_tools()
search = DuckDuckGoSearchRun()
tools = [search, *fs_tools]
agent_executor = create_react_agent(model, tools, checkpointer=memory)


class AgentRequest(BaseModel):
    """
    Represents a request to the agent.

    Attributes:
        msg (str): The message to be processed by the agent.
    """

    msg: str


@router.post("/agent")
async def process_request(request: AgentRequest):
    """
    Endpoint to process user requests by interacting with the agent.

    Args:
        request (AgentRequest): The request containing the user message.

    Returns:
        dict: A response containing the agent's processed output.
    """
    config = {"configurable": {"thread_id": "abc123"}}
    human_msg = request.msg
    response = ""

    try:
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=human_msg)]}, config
        ):
            if "agent" in chunk:
                response += chunk["agent"]["messages"][0].content + "\n"
            elif "tools" in chunk:
                response += chunk["tools"]["messages"][0].content + "\n"
            else:
                response += str(chunk) + "\n"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    return {"response": response.strip()}
