from fastapi import FastAPI
import uvicorn
from engine import get_chatbot_engine
from nodes.graph_state import get_empty_state
from pydantic import BaseModel

server = FastAPI()
engine = get_chatbot_engine()

@server.get("/")
async def checkHome():
    return {"message": "QnA POC"}

class ChatRequest(BaseModel):
    query:str

@server.post("/chat")
async def generate(
    request: ChatRequest
) -> str:
    print("Received Query: ", request.query)

    initial_state = get_empty_state()
    print("INITIAL STATE: \n", initial_state)
    print(type(initial_state))
    initial_state["messages"].append({"role": "user", "content": request.query})
    final_state = engine.invoke(initial_state)
    print("Final State: \n", final_state)
    response = final_state["messages"][-1]["content"]
    return {"response":response}

if __name__ == "__main__":
    # uvicorn.run(server, "0.0.0.0", 8000)
    uvicorn.run(server, host="127.0.0.1", port=8000)
    # uvicorn.run(server)