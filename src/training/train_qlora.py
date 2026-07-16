import json
import torch

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    BitsAndBytesConfig,
)

from peft import (
    LoraConfig,
    prepare_model_for_kbit_training,
)

from trl import SFTTrainer


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

with open(
    "dataset/ai_engineering_dataset.json",
    "r",
    encoding="utf-8"
) as f:
    raw_data = json.load(f)

formatted_data = []

for item in raw_data:
    text = (
        f"-> Instruction:\n"
        f"{item['instruction']}\n\n"
        f"-> Response:\n"
        f"{item['response']}"
    )

    formatted_data.append(
        {
            "text": text
        }
    )

dataset = Dataset.from_list(
    formatted_data
)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
)

model = prepare_model_for_kbit_training(
    model
)

peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
    ],
)

training_args = TrainingArguments(
    output_dir="outputs/qlora",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=5,
    save_strategy="epoch",
    fp16=True,
    report_to="none",
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    args=training_args,
)

trainer.train()

trainer.save_model(
    "outputs/qlora_adapter"
)

tokenizer.save_pretrained(
    "outputs/qlora_adapter"
)