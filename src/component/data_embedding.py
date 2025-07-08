import os 
import sys
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from src.logger import logging
from src.exception import AIAssistantException
folder_path='vector_db'


class DataEmbedding:
    
    def __init__(self,docs):
        try:
            logging.info(f" ***start Data Embedding*** ")
            self.docs = docs
        except Exception as e:
            raise AIAssistantException(e,sys)

    
    
    def store_embeddings_into_database(self,docs,embedding_model):
        try:
            logging.info("check vector database is present or not")
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                logging.info("vector_db is present")
                vector_db = FAISS.load_local(folder_path=folder_path,embeddings=embedding_model,allow_dangerous_deserialization=True)
                vector_db.merge_from(FAISS.from_documents(docs,embedding_model))
                vector_db.save_local(folder_path=folder_path)
                
            else:
                logging.info("vector_db is not present")
                vector_db = FAISS.from_documents(docs,embedding_model)
                vector_db.save_local(folder_path=folder_path)
    
                
        except Exception as e:
            raise AIAssistantException(e,sys)
    

    def embedding(self):
        try:
            embedding_model = OllamaEmbeddings(model='nomic-embed-text')
            logging.info("start Embedding")
            self.store_embeddings_into_database(docs = self.docs,embedding_model=embedding_model)
            logging.info("~~ complete data Embedding")
            
        except Exception as e:
            raise AIAssistantException(e,sys)
        