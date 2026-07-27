from dataclasses import dataclass, field


@dataclass
class Request:

    request_id: int

    prompt: str

    generated_tokens: list[int] = field(default_factory=list)

    generated_text: str = ""

    finished: bool = False

    max_new_tokens: int = 128



    def append_token(
        self,
        token_id: int,
    ):

        self.generated_tokens.append(token_id)


    def update_text(
        self,
        text: str,
    ):

        self.generated_text = text



    def mark_finished(self):

        self.finished = True



    def is_finished(self):

        return (
            self.finished
            or len(self.generated_tokens)
            >= self.max_new_tokens
        )


    def generated_length(self):

        return len(self.generated_tokens)

    def reset(self):

        self.generated_tokens.clear()

        self.generated_text = ""

        self.finished = False