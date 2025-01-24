
class Config:
    model_name = "unsloth/llama-3-8b-bnb-4bit"
    max_seq_length=2048
    r=16
    lora_alpha = 16
    lora_dropout = 0
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
    bias = "none"
    random_state = 3407
    per_device_train_batch_size = 2
    gradient_accumulation_steps = 4
    warmup_steps = 10
    num_train_epochs = 3
    logging_steps = 1
    output_dir = "finetuned_model"
    optim = "adamw_8bit"
    seed = 3407
    report_to = "none"
