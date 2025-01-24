import os
import sys
import yaml
import json
import time
import streamlit as st
import pandas as pd
from langchain_community.vectorstores import FAISS
from src.exception import AIAssistantException


def load_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config = yaml.full_load(file)
        return config
    except Exception as e:
            raise AIAssistantException(e,sys) 




def load_vector_store(embeddings):
    try:
        vector_store = FAISS.load_local(folder_path="vector_db",embeddings=embeddings,allow_dangerous_deserialization=True)
        return vector_store
    except Exception as e:
            raise AIAssistantException(e,sys) 



def save_info(data,Users_information):
    try:
        with open(os.path.join(Users_information,"info.json"), "w") as json_file:
            json.dump(data, json_file,indent=1)
    except Exception as e:
            raise AIAssistantException(e,sys) 
   
def load_info(Users_information):
    try:
        with open(os.path.join(Users_information,"info.json"),"r") as json_file:
            return json.load(json_file)
    except Exception as e:
            raise AIAssistantException(e,sys) 

def callback():
    try:
        st.session_state.button_clicked = True
    except Exception as e:
            raise AIAssistantException(e,sys) 

def on_feedback():
    try:
        st.session_state.feedback += 1
    except Exception as e:
            raise AIAssistantException(e,sys) 
    
def fun(page):
    try:
        st.markdown(
        """
        <style>
        [data-testid="stBaseButton-secondary"] p{
            font-size: 0.88em;
            background-color: none;
            color: #D3D3D3;
        }
        [data-testid="stBaseButton-secondary"]:hover{
            background-color: none;
            border-color: #D9D9D9;
        }
        [data-testid="stBaseButton-secondary"]:active{
            background-color: #1C1C1C;
            border-color: #D3D3D3;
        }
        .stPopover p{
            background-color: none;
            color: #D3D3D3;
        }
        </style>
        """,
        unsafe_allow_html=True
        ) 
        h1_col, h2_col = st.sidebar.columns([1,0.10])
        if "button_clicked" not in st.session_state:
            st.session_state.button_clicked = False

        with h2_col:
            if st.button(f'{st.session_state.first_letter}', on_click=callback) or st.session_state.button_clicked:
                with h1_col:
                    with st.popover("option"):
                        if st.button("Log Out"):
                            st.session_state.logged_in = False
                            st.session_state.Username = None
                            st.toast("Log out Successfully")
                            time.sleep(0.5)
                            st.switch_page(page=st.Page(page=page, title="Home", icon="🏠"))
                            #st.switch_page(st.Page(page=page, title="Log out", icon="🔒"))
    except Exception as e:
            raise AIAssistantException(e,sys) 

feedback_folder= "feedback"
os.makedirs(feedback_folder,exist_ok=True)


def save_feedback(df,filepath):
    try:
        if os.path.exists(os.path.join(feedback_folder,filepath)):
            data = pd.read_csv(os.path.join(feedback_folder,filepath))
            data = pd.concat([data,df])
            data.to_csv(os.path.join(feedback_folder,filepath),index=False)
        else:
            df.to_csv(os.path.join(feedback_folder,filepath),index=False)
    except Exception as e:
            raise AIAssistantException(e,sys) 
    