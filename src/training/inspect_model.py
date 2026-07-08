from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)

for name, module in model.named_modules():

    if "q_proj" in name:
        print(name)

    if "k_proj" in name:
        print(name)

    if "v_proj" in name:
        print(name)