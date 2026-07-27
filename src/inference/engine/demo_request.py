from .request import Request


request = Request(
    request_id=1,
    prompt="Explain LoRA."
)

print(request)

print()

print("Appending tokens...")

request.append_token(123)

request.append_token(456)

request.append_token(789)

print(request.generated_tokens)

print()

request.update_text(
    "LoRA is a parameter-efficient fine-tuning technique."
)

print(request.generated_text)

print()

print(request.generated_length())

print(request.is_finished())

print()

request.mark_finished()

print(request.is_finished())