from fastapi import APIRouter

from ..engine.request import Request
from fastapi.responses import StreamingResponse
from .schemas import (
    GenerateRequest,
    GenerateResponse,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    Choice,
)
from .server import InferenceServer
import uuid


router = APIRouter()

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

server = InferenceServer(MODEL_NAME)


@router.post(
    "/generate",
    response_model=GenerateResponse,
)
def generate(
    body: GenerateRequest,
):

    request = Request(
        request_id=0,
        prompt=body.prompt,
        max_new_tokens=body.max_new_tokens,
    )

    response = server.generate(
        request
    )

    return GenerateResponse(
        generated_text=response.generated_text,
    )
@router.post("/stream")
def stream(
    body: GenerateRequest,
):

    request = Request(
        request_id=0,
        prompt=body.prompt,
        max_new_tokens=body.max_new_tokens,
    )

    iterator = server.stream(
        request
    )

    def event_generator():

        for chunk in iterator:

            yield f"data: {chunk}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )

@router.post(
    "/v1/chat/completions",
    response_model=ChatCompletionResponse,
)
def chat_completion(
    body: ChatCompletionRequest,
):
    internal_request_id = uuid.uuid4().hex

    prompt = "\n".join(
        f"{message.role}: {message.content}"
        for message in body.messages
    )

    prompt += "\nassistant: "


    request = Request(
        request_id=internal_request_id,
        prompt=prompt,
        max_new_tokens=body.max_tokens,
    )
    if body.stream:

        iterator = server.stream(
            request
        )

        def event_generator():

            for chunk in iterator:

                yield f"data: {chunk}\n\n"

            yield "data: [DONE]\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
        )
    response = server.generate(
        request
    )
    

    choice = Choice(
        index=0,
        message=ChatMessage(
            role="assistant",
            content=response.generated_text,
        ),
        finish_reason="stop",
    )

    response_id = f"chatcmpl-{uuid.uuid4().hex}"
    
    return ChatCompletionResponse(
        id=response_id,
        object="chat.completion",
        choices=[choice],
    )