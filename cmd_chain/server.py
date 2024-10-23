import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from cmd_chain.agent import agent_router

load_dotenv()

app = FastAPI()

app.include_router(agent_router)


def main():
    uvicorn.run("cmd_chain.server:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
