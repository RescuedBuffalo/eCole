from fastapi import FastAPI

from .cortex.executive import ExecutiveController
from .state.schema import AgentState, Permissions
from .senses.ingest import ingest_message

app = FastAPI()
controller = ExecutiveController()


@app.post("/chat")
async def chat(message: str):
    state = AgentState(last_message=message, permissions=Permissions.default())
    ingest_message(message, state)
    actions = controller.decide(state)
    response = controller.execute(actions[0]) if actions else ""
    return {"response": response}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("ecole.backend.app:app", host="0.0.0.0", port=8000)
