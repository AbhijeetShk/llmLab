from pydantic import BaseModel


class GenerateRequest(BaseModel):

    prompt: str

    max_new_tokens: int = 128


class GenerateResponse(BaseModel):

    generated_text: str


class ChatMessage(BaseModel):

    role: str

    content: str


class ChatCompletionRequest(BaseModel):

    model: str

    messages: list[ChatMessage]

    stream: bool = False

    max_tokens: int = 128


class Choice(BaseModel):

    index: int

    message: ChatMessage

    finish_reason: str


class ChatCompletionResponse(BaseModel):

    id: str

    object: str

    choices: list[Choice]

class ModelInfo(BaseModel):

    id: str

    object: str = "model"

    owned_by: str


class ModelsResponse(BaseModel):

    object: str = "list"

    data: list[ModelInfo]