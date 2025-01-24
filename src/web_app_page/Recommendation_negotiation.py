import streamlit as st
import os
import sys
import pandas as pd
from src.Tools import PreprocessingTools
from src.web_app_page.retriever_prompt_chain import Retriever,PromtChain
from langchain_community.embeddings import OllamaEmbeddings
from src.utils import load_vector_store,fun,save_feedback
from src.web_app_page.main import App
from src.logger import logging
from src.exception import AIAssistantException
from langchain_core.messages import HumanMessage,AIMessage


embeddings = OllamaEmbeddings(model='nomic-embed-text')
vectorstore = load_vector_store(embeddings=embeddings)



prompt_chain = PromtChain()
conversation_chain = prompt_chain.prompt()

class RecommendationAndNegotiation:
    def __init__(self,conversation_chain):
        try:
            self.conversation_chain = conversation_chain
        except Exception as e:
            raise AIAssistantException(e,sys)

    @st.dialog("Are you want to clear all chat history 🗑?")    
    def clear_chat(self):
        try:
            st.markdown("""
            <style>
            
            .stButton > button:hover {
                background-color: #D9D9D9;
                color: black;
            }
            
            </style>
            """, unsafe_allow_html=True)
            _, col1, col2 = st.columns([0.20,1.30,1],gap="small")
            if col1.button("Yes"):
                st.session_state.chat_history = []
                logging.info("clear chat history and it becomes an empty list")
                st.rerun() 
            if col2.button("No"):
                st.rerun() 
        except Exception as e:
            raise AIAssistantException(e,sys)  

    
    def handle_query(self,user_query):
        try:
            self.retriever_obj= Retriever(vectorstore)
            self.tool = PreprocessingTools()
            logging.info('start generating response')
            previous_query_response = ["\n".join([obj["content"] for obj in st.session_state.chat_history][-2:])]
            if not "recommend" in user_query.lower():
                retrieved_doc = self.retriever_obj.retriever().invoke(user_query)
                response = self.conversation_chain.invoke({"context":retrieved_doc,"input": user_query,"chat_history": previous_query_response})
              
            elif "recommend" in user_query.lower():
                retrieved_doc = self.retriever_obj.recommend_retriever().invoke(user_query)
                filter_doc = self.tool.recommend(retrieved_doc)
                response = self.conversation_chain.invoke({"context":filter_doc,"input": user_query,"chat_history": previous_query_response})
               
            return response
        except Exception as e:
            raise AIAssistantException(e,sys)
    
    def Recommendation_and_negotiation(self,user_query):
        try:
            st.markdown("""
                <style>

                div[data-testid="stTabs"] p {
                    color: #000033
                }
                </style>
                """, unsafe_allow_html=True)
            
            if "toast_count" not in st.session_state:
                st.session_state.toast_count = 0
            
            if st.session_state.toast_count < 2:
                st.toast("🔔Kindly give us your valuable feedback after conversion.")
                st.session_state.toast_count += 1
            

            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            
            for message in st.session_state.chat_history:
                #st.write(message)
                count=int(len(message))
                #st.write(count)
                i=0
                col1, _ = st.columns([i+count,1])
                col, col2 = st.columns([0.3,0.7])

                if message["role"] == "user":
                    with col1:
                        with st.chat_message(message["role"]):
                            st.markdown(f'<div style="color:black; font-size:0.8em;">{message["content"]}</div>',unsafe_allow_html=True)

                if message["role"] == "assistant":
                    with col2:
                        with st.chat_message(message["role"]):
                            message["content"] = message["content"].replace("\n\n", "<br><br>").replace("\n", "</p><p>")
                            st.markdown(f"""<style>div[data-testid="stMarkdown"] p {{font-size: 1em;}}</style><div style="color:black; font-size:0.83em;">{message["content"]}</div>""",unsafe_allow_html=True)

                        
        
            
            if user_query:
                logging.info("Display user query in chat message container")
                st.chat_message("user").markdown(f'<p style = "color:black; font-size:0.8em;">{user_query}</p>', unsafe_allow_html=True)
                logging.info("Add user message to chat history")
                st.session_state.chat_history.append({"role": "user", "content": user_query})
                with st.spinner('....'):
                    response =self.handle_query(user_query)
                    logging.info("Display assistant response in chat message container")
                    with st.chat_message("assistant"):
                        response = response.replace("\n\n", "<br><br>").replace("\n", "</p><p>")
                        st.markdown(f"""<style>div[data-testid="stMarkdown"] p {{font-size: 1em;}}</style><div style="color:black; font-size:0.83em;">{response}</div>""",unsafe_allow_html=True)
                       
                            #st.markdown(f'<div style="color:black; font-size:0.8em;">{response}</div>',unsafe_allow_html=True)
                    
                
                logging.info("Add assistant response to chat history")
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            
            if "clear_chat" not in st.session_state:
                with st.sidebar:
                    col3,_ = st.columns([1,1])
                    with col3:
                        if st.button("clear_chat",use_container_width=True):
                            self.clear_chat()
                            
            st.sidebar.markdown("<br><br>", unsafe_allow_html=True) 
            fun(App.home_page)
        except Exception as e:
            raise AIAssistantException(e,sys)
            

    def start(self):
        try:
            st.markdown(f'<div style="font-size:1em; color:#2F3E46;" class="circular-container">{st.session_state.first_letter}</div>', unsafe_allow_html=True)
            
            placeholder1=st.sidebar.empty()

            st.markdown(
                """
                <style>
                
                .stDialog > div > div {
                    background-color: #2E2E2E;  
                    padding: 20px;
                    border-radius: 10px;
                }
                div[data-testid="stDialog"] p {
                    color: #2E2E2E;  
                }
                .stToast{
                    position: fixed;
                    bottom: 10px;
                    color: black;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <style>
                .main > div:first-child {
                    padding-top: 5px;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <style>
                .stSlider > div > div > div > div > div{
                    color: gray;   
                }
                .stSlider > div > div > div > div{
                    background-color: #E34234;   
                }
                .stSlider{
                    margin-top: -35px;  
                }
                .stSlider label p{
                    font-size: 1em; 
                    color: #D3D3D3;   
                }
                div[data-testid="stSidebarUserContent"] {
                    margin-top: 17px;  
                }
                [data-testid="stBaseButton-primary"] {
                    background-color: white;
                }
                [data-testid="stBaseButton-primary"]:hover{
                    background-color: white;
                    border-color: #D9D9D9;
                }
                [data-testid="stBaseButton-primary"]:active{
                    background-color: white;
                    border-color: #F08080;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            
           
            rating = placeholder1.slider("Rating ⭐",min_value=0.0, step=0.1,max_value=5.0)
            value = f"{rating}"
            if "rating" not in st.session_state:
                st.session_state.rating = []

            if "avg_rating" not in st.session_state:
                st.session_state.avg_rating = None

            logging.info("calculating Average rating and store in csv file")
            if value >= "1.0":
                st.session_state.rating.append(value)
                v = f"{round((sum(map(float,st.session_state.rating))/len(st.session_state.rating)),2)}"
                st.session_state.avg_rating = v
                df1 = pd.DataFrame(
                    {
                        "Username": [f"{st.session_state.Username}"],
                        "rating": [f"{value}"]
                    }
                )
                filepath2 = "rating_feedback.csv"
                save_feedback(df1,filepath2)

            if value > "0.0" and value < "1.0":
                st.session_state.avg_rating = None
                value = None
                df2 = pd.DataFrame(
                    {
                        "Username": [f"{st.session_state.Username}"],
                        "rating": [f"{value}"]
                    }
                )
                filepath2 = "rating_feedback.csv"
                save_feedback(df2,filepath2)

            logging.info("create a chat input box")
            user_query = st.chat_input("write your query")

            tab1, tab2= st.tabs(["Assistant","Feedback"])
            with tab1:
                st.markdown("""<h2 style='font-size: 1.40em; color:black;'>Hello! I am an E-Commerce assistant. how can I help you?</h2>""", unsafe_allow_html=True)
                self.Recommendation_and_negotiation(user_query)
            with tab2:
                st.markdown("""<p style=color:black;'>Your feedback matters to us! Please share your experience by completing the form.</p>""", unsafe_allow_html=True)
                if st.button("📋click here",type='primary'):
                    st.switch_page(st.Page(r"src\web_app_page\feedback_form.py"))
        except Exception as e:
            raise AIAssistantException(e,sys)
        


if "logged_in" not in st.session_state:
    st.session_state.previous_page = st.Page(r"src\web_app_page\Recommendation_negotiation.py")
    st.switch_page(st.Page(App.loging)) # Redirect to login
    st.rerun()

if "Username" not in st.session_state:
    st.session_state.Username = None

st.markdown(
    """
    <style>
    .circular-container {
        width: 28px;        
        height: 28px;      
        border-radius: 50%;   
        border: 1px solid #FF6347;  
        text-align: center;
        background-color: #FF6347;
        position: absolute;
        top: 50px;  
        right: 10px;  
        z-index: 1000;
    }
    
    </style>
    """, unsafe_allow_html=True
    )


if st.session_state.logged_in and st.session_state.Username:
    obj = RecommendationAndNegotiation(conversation_chain)
    obj.start()

 

if not st.session_state.logged_in:
    st.session_state.previous_page = st.Page(r"src\web_app_page\Recommendation_negotiation.py")
    st.switch_page(st.Page(App.loging)) # Redirect to login
    st.rerun()