from typing import List
from pydantic import BaseModel
from fastapi.responses import Response
from llama_index.core.base.base_query_engine import BaseQueryEngine
from fastapi import APIRouter, Request, Depends
from llama_index.core.llms import MessageRole
from app.engine import get_query_engine

query_router = query = APIRouter()

class _Message(BaseModel):
    role: MessageRole
    content: str

class _ChatData(BaseModel):
    messages: List[_Message]

@query.post("")
async def query(
    request: Request,
    data: _ChatData,
    query_engine: BaseQueryEngine = Depends(get_query_engine),
):
    last_message = data.messages.pop()
    # query engine
    response = query_engine.query(last_message.content)

    return Response(response.response, media_type="text/plain")
