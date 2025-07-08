from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.llms import Ollama
from src.logger import logging
from src.exception import AIAssistantException
import sys
llm=Ollama(model='test12_model')


class Retriever:
    def __init__(self, vectorstore):
        try:
            self.vector_db = vectorstore
        except Exception as e:
            raise AIAssistantException(e,sys)


    def retriever(self):
        try:
            logging.info("create a retriever for retrieve docs")
            retriever = self.vector_db.as_retriever(search_type ='similarity',search_kwargs={'k': 10})
            return retriever
        except Exception as e:
            raise AIAssistantException(e,sys)
        
    def recommend_retriever(self):
        try:
            logging.info("create a retriever for retrieve docs")
            retriever = self.vector_db.as_retriever(search_type ='similarity',search_kwargs={'k': 100})
            return retriever
        except Exception as e:
            raise AIAssistantException(e,sys)

class PromtChain:
    def __init__(self):
        pass

    def prompt(self):
        try:
            system_prompt =("""
            {context}
            """
            )
            prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
            )
            logging.info("create a chain with llm, prompt")
            conversation_chain = create_stuff_documents_chain(llm, prompt)
            return conversation_chain
        except Exception as e:
            raise AIAssistantException(e,sys)
    
    
    