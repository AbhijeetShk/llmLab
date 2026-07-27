import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)


class ModelWorker:

    def __init__(
        self,
        model_name: str,
        device: str | None = None,
    ):

        self.device = (
            device
            if device is not None
            else (
                "cuda"
                if torch.cuda.is_available()
                else "cpu"
            )
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name
        ).to(self.device)

        self.model.eval()

    @torch.no_grad()
    def generate(
        self,
        prompt: str,
        *,
        max_new_tokens: int = 128,
        temperature: float = 1.0,
        top_k: int = 50,
        top_p: float = 0.95,
    ) -> str:

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
        ).to(self.device)

        output = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            use_cache=True,
        )

        return self.tokenizer.decode(
            output[0],
            skip_special_tokens=True,
        )