import os 
import sys
import yaml
import pandas as pd
from src.utils import load_config
from src.logger import logging
from src.exception import AIAssistantException



class DataIngestion:
    def __init__(self):
        try:
            logging.info(f" ****Start DataIngestion**** ")
            config_file = 'config/config.yaml'
            self.config = load_config(config_file)
            self.folder_path = self.config['source']['folder']
        except Exception as e:
            raise AIAssistantException(e,sys)
       


    
    def ingestion(self):
        try:
            dataframes = []
            for filename in os.listdir(self.folder_path):
                if filename.endswith('.csv'):
                    file_path = os.path.join(self.folder_path, filename)
                    # Read the CSV file and append to the list
                    df = pd.read_csv(file_path)
                    dataframes.append(df)
            
            merged_df = pd.concat(dataframes, ignore_index=True)   
            
            #print(merged_df.head())
            logging.info(f"~~ complete data ingestion ~~")
            return merged_df
        
        except Exception as e:
            raise AIAssistantException(e,sys)
        
