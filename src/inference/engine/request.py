from dataclasses import dataclass, field


@dataclass
class Request:
   
   # represents one inference request.


    request_id: int

    prompt: str

    generated_text: str = ""

    generated_tokens: list[int] = field(default_factory=list)

    finished: bool = False

    max_new_tokens: int = 128