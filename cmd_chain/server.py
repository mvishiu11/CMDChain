"""
This module sets up and runs the FastAPI server.
The server includes the agent router to handle requests related to the LLM-based agent.
"""
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from cmd_chain.agent import agent_router

load_dotenv()

app = FastAPI()

app.include_router(agent_router)


def main():
    """
    Entry point to run the FastAPI server using Uvicorn.
    """
    uvicorn.run("cmd_chain.server:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
