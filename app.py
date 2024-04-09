import uuid
import json
import logging
import uvicorn

from main import chat_interface
from fastapi import FastAPI, Response
from pydantic import BaseModel, HttpUrl


logger = logging.getLogger(__name__)
app = FastAPI()

class ChatRequest(BaseModel):
    chat_id: str
    message: str

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/initialize_chat")
def initialize_chat():
    chat_id = str(uuid.uuid4())
    json_file_path = f"chats/{chat_id}.json"
    
    with open(json_file_path, "w") as f:
        json.dump(
            {
                "chat_id": chat_id,
                "messages": []
            },
            f
        )
    
    return {"chat_id": chat_id, "json_file_path": json_file_path}


@app.post("/api/chat")
def chat(request: ChatRequest):
    chat_id = request.chat_id
    message = request.message
    
    html_path = chat_interface(chat_id, message)
    
    return {"status": "ok", "html": html_path}


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)