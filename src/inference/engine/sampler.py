import torch
import torch.nn.functional as F


class Sampler:

    """
    Token sampling strategies.
    """



    @staticmethod
    def greedy(
        logits: torch.Tensor,
    ) -> torch.Tensor:

        return torch.argmax(
            logits,
            dim=-1,
            keepdim=True,
        )



    @staticmethod
    def temperature(
        logits: torch.Tensor,
        temperature: float,
    ) -> torch.Tensor:

        logits = logits / temperature

        probs = F.softmax(
            logits,
            dim=-1,
        )

        return torch.multinomial(
            probs,
            num_samples=1,
        )



    @staticmethod
    def top_k(
        logits: torch.Tensor,
        k: int,
    ) -> torch.Tensor:

        values, indices = torch.topk(
            logits,
            k,
        )

        probs = F.softmax(
            values,
            dim=-1,
        )

        sample = torch.multinomial(
            probs,
            num_samples=1,
        )

        return indices.gather(
            -1,
            sample,
        )



    @staticmethod
    def top_p(
        logits: torch.Tensor,
        p: float,
    ) -> torch.Tensor:

        sorted_logits, sorted_indices = torch.sort(
            logits,
            descending=True,
        )

        probs = F.softmax(
            sorted_logits,
            dim=-1,
        )

        cumulative = torch.cumsum(
            probs,
            dim=-1,
        )

        mask = cumulative > p

        mask[..., 1:] = mask[..., :-1].clone()

        mask[..., 0] = False

        sorted_logits[mask] = float("-inf")

        probs = F.softmax(
            sorted_logits,
            dim=-1,
        )

        sample = torch.multinomial(
            probs,
            num_samples=1,
        )

        return sorted_indices.gather(
            -1,
            sample,
        )