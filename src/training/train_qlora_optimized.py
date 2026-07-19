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
from transformers.trainer_utils import get_last_checkpoint


OUTPUT_DIR = "/content/drive/MyDrive/AI/qwen_qlora"
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

with open(
    "ai_engineering_dataset.json",
    "r",
    encoding="utf-8"
) as f:
    raw_data = json.load(f)

formatted_data = [
    {
        "text": (
            f"-> Instruction:\n"
            f"{item['instruction']}\n\n"
            f"-> Response:\n"
            f"{item['response']}"
        )
    }
    for item in raw_data
]

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
tokenizer.padding_side = "right"


model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto",
)

model = prepare_model_for_kbit_training(
    model
)
model.config.use_cache = False
# model.print_trainable_parameters()
print(model.config.torch_dtype)
print(torch.get_default_dtype())
for name, p in model.named_parameters():
    print(name, p.dtype)
    break
for name, p in model.named_parameters():
    if p.requires_grad:
        print(name, p.dtype)
        break

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
    output_dir=OUTPUT_DIR,

    num_train_epochs=5,

    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.1,
    learning_rate=2e-4,
    weight_decay=0.01,
    seed=42,
    logging_strategy="steps",
    logging_steps=1,
    optim="paged_adamw_8bit",

    save_strategy="epoch",
    # eval_strategy="epoch",

    save_total_limit=3,

    gradient_checkpointing=True,
    
    fp16=False,
    bf16=True,

    report_to="none",
)
training_args.save_safetensors = True

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    processing_class=tokenizer,
    peft_config=peft_config,
    args=training_args,
)
checkpoint = get_last_checkpoint(OUTPUT_DIR)

if checkpoint is not None:
    print("Resuming from:", checkpoint)
    trainer.train(resume_from_checkpoint=checkpoint)
else:
    print("Starting new training")
    trainer.train()


FINAL_MODEL = "/content/drive/MyDrive/AI/qwen_qlora/final_adapter"

trainer.save_model(FINAL_MODEL)
tokenizer.save_pretrained(FINAL_MODEL)