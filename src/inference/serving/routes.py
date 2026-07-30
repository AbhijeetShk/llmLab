from fastapi import APIRouter

from ..engine.request import Request

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