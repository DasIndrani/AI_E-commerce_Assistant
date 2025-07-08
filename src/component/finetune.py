import os 
import sys
import torch
import pandas as pd
from src.utils import load_config
from src.config import Config
from datasets import Dataset
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth import is_bfloat16_supported
from src.logger import logging
from src.exception import AIAssistantException


class ModelTrainer:
    def __init__(self):
        try:
            logging.info("*** start Modeltraining ***")
            self.config = Config()
            config_file = 'config/config.yaml'
            self.path_config = load_config(config_file)
            self.dataset_path = self.path_config['dataset']['file_path']
        except Exception as e:
            raise AIAssistantException(e,sys)

    def load_model_and_tokenizer(self):
        try:
            logging.info("load base model and tokenizer")
            model, tokenizer =FastLanguageModel.from_pretrained(
                    model_name = self.config.model_name,
                    max_seq_length = self.config.max_seq_length,
                    dtype=None,
                    load_in_4bit=True)
            return model,tokenizer
        except Exception as e:
            raise AIAssistantException(e,sys)

    def prepare_dataset_and_training_argument(self):
        try:
            model,tokenizer = self.load_model_and_tokenizer()
            df = pd.read_csv(self.dataset_path)
            logging.info("prepare dataset for training") 
            data = Dataset.from_pandas(df)
            chat_template = """You are a helpful assistant

            ### Instruction:
            {}

            ### Response:
            {}"""
            EOS_TOKEN = tokenizer.eos_token
            def function(examples):
                input = examples["Query"]
                output  = examples["Response"]
                texts = []
                for input, output in zip(input, output):
                    text = chat_template.format(input, output) + EOS_TOKEN
                    texts.append(text)
                return { "text" : texts }
            dataset = data.map(function, batched = True)
            
            logging.info("Prepare model for training")
            model=FastLanguageModel.get_peft_model(
                    model,
                    r=self.config.r,
                    lora_alpha = self.config.lora_alpha,
                    lora_dropout = self.config.lora_dropout,
                    target_modules = self.config.target_modules,
                    bias = self.config.bias,
                    use_gradient_checkpointing = True,
                    random_state = self.config.random_state,
                    max_seq_length = self.config.max_seq_length
                )
            logging.info("set arguments for training")
            training_argument=TrainingArguments(
                    per_device_train_batch_size = self.config.per_device_train_batch_size,
                    gradient_accumulation_steps = self.config.gradient_accumulation_steps,
                    warmup_steps = self.config.warmup_steps,
                    num_train_epochs = self.config.num_train_epochs,
                    fp16 = not is_bfloat16_supported(),
                    bf16 = is_bfloat16_supported(),
                    logging_steps = self.config.logging_steps,
                    output_dir = self.config.output_dir,
                    optim = self.config.optim,
                    seed = self.config.seed,
                    report_to = self.config.report_to
                )
            return dataset, tokenizer, model, training_argument
            
            return data
        except Exception as e:
            raise AIAssistantException(e,sys)
    
    def train(self):
        try:
            data = self.prepare_dataset_and_training_argument()
            dataset, tokenizer, model, training_argument = self.prepare_dataset_and_training_argument()
            trainer=SFTTrainer(
                    model=model,
                    train_dataset=dataset,
                    dataset_text_field="text",
                    tokenizer=tokenizer,
                    args=training_argument,
                    max_seq_length=self.config.max_seq_length,
                    packing = False
                )
            logging.info("start training")
            trainer_stats = trainer.train()
            logging.info("save the finetuned model")
            model.save_pretrained_gguf("model", tokenizer, quantization_method = "q4_k_m")
            
        except Exception as e:
            raise AIAssistantException(e,sys)