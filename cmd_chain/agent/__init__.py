"""
This module defines a FastAPI router for interacting with the LLM-based agent.
The router allows users to send commands to the agent,
which processes the requests and returns a response.
"""

from cmd_chain.agent.router import router as agent_router  # noqa: F401
