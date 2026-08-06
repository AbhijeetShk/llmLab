import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)


class ModelWorker:

    def __init__(
        self,
        model_name: str,
        device: str | None = None,
    ):

        self.model_name = model_name
        self.device = self.model.device
        self.device = (
            device
            if device
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



    def encode(
        self,
        prompt: str,
    ):

        return self.tokenizer(
            prompt,
            return_tensors="pt",
        ).input_ids.to(self.device)


    # First Forward Pass (Prefill)
  

    @torch.no_grad()
    def prefill(
        self,
        input_ids: torch.Tensor,
    ):

        outputs = self.model(
            input_ids=input_ids,
            use_cache=True,
        )

        logits = outputs.logits[:, -1, :]

        return (
            logits,
            outputs.past_key_values,
        )


    # Decoding one token


    @torch.no_grad()
    def decode(
        self,
        input_ids: torch.Tensor,
        past_key_values,
    ):

        outputs = self.model(
            input_ids=input_ids,
            past_key_values=past_key_values,
            use_cache=True,
        )

        logits = outputs.logits[:, -1, :]

        return (
            logits,
            outputs.past_key_values,
        )


    # convert ids to text


    def decode_tokens(
        self,
        token_ids,
    ):

        if isinstance(token_ids, torch.Tensor):
            token_ids = token_ids.tolist()

        return self.tokenizer.decode(
            token_ids,
            skip_special_tokens=True,
        )