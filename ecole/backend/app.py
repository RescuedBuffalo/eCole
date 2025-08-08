from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .cortex.executive import ExecutiveController
from .state.schema import AgentState, Permissions
from .senses.ingest import ingest_message


class ChatRequest(BaseModel):
    message: str


class GoalIn(BaseModel):
    description: str


app = FastAPI()
controller = ExecutiveController()
goals: List[GoalIn] = []

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/")
async def index():
    return FileResponse(frontend_dir / "index.html")


@app.post("/chat")
async def chat(req: ChatRequest):
    message = req.message
    state = AgentState(last_message=message, permissions=Permissions.default())
    ingest_message(message, state)
    actions = controller.decide(state)
    response = controller.execute(actions[0]) if actions else ""
    return {"response": response}


@app.get("/goals")
async def get_goals():
    return {"goals": goals}


@app.post("/goals")
async def add_goal(goal: GoalIn):
    goals.append(goal)
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("ecole.backend.app:app", host="0.0.0.0", port=8000)
