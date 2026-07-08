from transformers import AutoModelForCausalLM
from peft import LoraConfig
from peft import get_peft_model

model = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)

config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=[
        "q_proj",
        "v_proj"
    ],
    lora_dropout=0.05,
)

model = get_peft_model(
    model,
    config
)

model.print_trainable_parameters()