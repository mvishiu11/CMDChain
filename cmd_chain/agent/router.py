"""
This module contains the FastAPI router for the agent endpoint.
"""

import os
from fastapi import APIRouter
from pydantic import BaseModel
from cmd_chain.agent.llm_agent import LLMAgent

router = APIRouter()
custom_agent = LLMAgent(root_dir=os.getenv("AGENT_ROOT_DIR", os.getcwd()))


class AgentRequest(BaseModel):
    """
    Represents a request to the agent.

    Attributes:
        msg (str): The message to be processed by the agent.
        root_dir (str | None): Optional root directory for file management tools.
    """

    msg: str
    root_dir: str | None = None
    reset_memory: bool = False


@router.post("/agent")
async def process_request(request: AgentRequest):
    """
    Endpoint to process user requests by interacting with the agent.

    Args:
        request (AgentRequest): The request containing the user message.

    Returns:
        dict: A response containing the agent's processed output.
    """
    if request.root_dir:
        agent = LLMAgent(root_dir=request.root_dir)
    else:
        agent = custom_agent
    if request.reset_memory:
        agent.reset_memory()
    response = agent.process_request(request.msg)
    return {"response": response}
