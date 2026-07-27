from src.inference.sampling import sample_next_token


class Sampler:

    def sample(
        self,
        logits,
        temperature=1.0,
        top_k=50,
        top_p=0.95,
    ):

        return sample_next_token(
            logits,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
        )