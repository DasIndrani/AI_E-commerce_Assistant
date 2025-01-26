## AI_E-commerce_Assistant

## Description:
    This repository houses a system to designed to build a fine-tune LLM model from pretrained LLM with custom data and use fine-tune model to create a chatbot with RAG, aimed at providing content-based recommendation, product information available at the moment and real time price negotiation capability to enhance shopping experience.


## Install
### Requirements:
    * python 3.11
    * langchain
    * streamlit
    * langchain_community
    * faiss-cpu
    * scikit-learn
    * datasets 
    * accelerate
    * "unsloth[cu121-torch250] @ git+https://github.com/unslothai/unsloth.git"
    * Ollama version >= 0.5.4

## note:
    * GPU is needed to train model.
    * pull open embedding model "nomic-embed-text" from ollama.

    * Use the fine-tune model with ollama, open a cmd and then change directory to "Modelfile" path and then create model with ollama.
    * command to create model with ollama  "ollama create -f Modelfile test12_model".

### Run the pipeline to build fine-tune model and embedding:
    * python worflow.py

## host in local: 
    * streamlit run app.py
