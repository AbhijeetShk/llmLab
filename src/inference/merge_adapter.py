from transformers import AutoModelForCausalLM
from peft import PeftModel

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

base_model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)

model = PeftModel.from_pretrained(
    base_model,
    "outputs/lora_adapter"
)

merged_model = model.merge_and_unload()

merged_model.save_pretrained(
    "outputs/merged_model"
)

print("Merged model saved.")