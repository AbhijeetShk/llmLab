import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

from peft import PeftModel


BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

DEVICE = (
    torch.device("mps")
    if torch.backends.mps.is_available()
    else torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )
)


def load_base():

    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL
    )

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=(
            torch.float16
            if DEVICE.type != "cpu"
            else torch.float32
        ),
    )

    model.to(DEVICE)
    model.eval()

    return tokenizer, model


def load_lora(adapter_path):

    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL
    )

    base = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=(
            torch.float16
            if DEVICE.type != "cpu"
            else torch.float32
        ),
    )

    model = PeftModel.from_pretrained(
        base,
        adapter_path,
    )

    model.to(DEVICE)
    model.eval()

    return tokenizer, model