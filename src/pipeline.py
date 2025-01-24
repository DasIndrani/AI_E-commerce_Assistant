import os 
import sys
from src.component.data_ingestion import DataIngestion
from src.component.data_preprocessing import DataPreprocessing
from src.component.finetune import ModelTrainer
from src.component.data_embedding import DataEmbedding
from src.logger import logging
from src.exception import AIAssistantException



class Pipeline:
    def __init__(self):
        try:
            self.data_ingestion = DataIngestion()
        except Exception as e:
            raise AIAssistantException(e,sys) 
    



    def run(self):
        try:
            logging.info("Start Datapipeline")
            merged_df= self.data_ingestion.ingestion()

            self.data_preprocessing = DataPreprocessing(df=merged_df)
            processed_df, documents = self.data_preprocessing.preprocessing()
            
            self.model_trainer = ModelTrainer()
            self.model_trainer.train()

            self.data_embedding = DataEmbedding(docs=documents)
            self.data_embedding.embedding()
        except Exception as e:
            raise AIAssistantException(e,sys) 

