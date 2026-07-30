from pydantic import BaseModel


class GenerateRequest(BaseModel):

    prompt: str

    max_new_tokens: int = 128


class GenerateResponse(BaseModel):

    generated_text: str