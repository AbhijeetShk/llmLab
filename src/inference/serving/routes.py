from fastapi import APIRouter

from ..engine.request import Request
from fastapi.responses import StreamingResponse
from .schemas import (
    GenerateRequest,
    GenerateResponse,
)
from .server import InferenceServer


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