import json

from datasets import Dataset

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)

from peft import (
    LoraConfig,
    get_peft_model,
)

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"


with open(
    "dataset/ai_engineering_dataset.json",
    "r",
    encoding="utf-8",
) as f:
    data = json.load(f)

formatted_data = []

for item in data:

    text = f"""-> Instruction:
{item['instruction']}

-> Response:
{item['response']}
"""

    formatted_data.append(
        {"text": text}
    )

dataset = Dataset.from_list(
    formatted_data
)



tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

tokenizer.pad_token = tokenizer.eos_token



def tokenize(example):

    return tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=256,
    )

tokenized_dataset = dataset.map(
    tokenize,
    batched=True,
)



model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)



lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=[
        "q_proj",
        "v_proj",
    ],
    lora_dropout=0.05,
)

model = get_peft_model(
    model,
    lora_config,
)

model.print_trainable_parameters()



training_args = TrainingArguments(
    output_dir="outputs/checkpoints",

    num_train_epochs=3,

    per_device_train_batch_size=2,

    logging_steps=5,

    save_strategy="epoch",

    learning_rate=2e-4,

    fp16=False,
)



trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,

    data_collator=DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    ),
)



trainer.train()



model.save_pretrained(
    "outputs/lora_adapter"
)

tokenizer.save_pretrained(
    "outputs/lora_adapter"
)

print("Training Complete.")