import asyncio
import datetime
import json
from typing import AsyncGenerator, Dict, List

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")  # 设置模板目录


class Message(BaseModel):
    content: str


async def generate_stream_response():
    while True:
        message = Message(
            content=f"time from server：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        yield f"data: {json.dumps(message.dict())}\n\n"
        await asyncio.sleep(1)


@app.get("/nice_gui/message_channel")
async def chat_completions(request: Request):
    return StreamingResponse(generate_stream_response(), media_type="text/event-stream")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=5000, workers=3)
