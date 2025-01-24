import streamlit as st
import os,sys
import time
from src.utils import load_info,save_info,fun
from src.logger import logging
from src.exception import AIAssistantException
Users_information = "Users_Information"
os.makedirs(Users_information,exist_ok=True)
user_data = {}

class App:
    def __init__(self):
        pass

    def signin(self):
        try:
            st.markdown(
            """
            <h1 style='font-size: 2em; margin-bottom: 0px; color: black;'>🔐Sign-in</h1>
            """, 
            unsafe_allow_html=True
            )
            st.markdown(
            """
            <style>
            .stTextInput input {
                width: 500px;
            }
            .stTextInput p {
                color: black;
            }
            .stAlertContainer  {
                width: 510px;
                background-color: white;
                color: Red;
            }
            .stButton >button {
                width: 80px
            }
            .stButton p {
                color: black;
            }
            .stButton >button:hover {
                border: none;
                background-color: #9AAE91;
            }
            </style>
            """, 
            unsafe_allow_html=True
            )
            
            _,col,_ = st.columns([0.20,1,0.30])
            with col:
                new_username = st.text_input("Username",placeholder="enter new username")
                new_password = st.text_input("Password",type="password",placeholder="enter new password",max_chars=10)
                sub_col1, sub_col2 = st.columns([1,0.30])
                with sub_col1:
                    if st.button("Sing-in"):
                        if os.path.exists(os.path.join(Users_information,"info.json")):
                            User_info = load_info(Users_information)
                            keys = User_info.keys()
                            if new_username in keys:
                                st.error("Try Another Username:warning:")
                                return False
                            else:
                                key = f"{new_username}"
                                value = f"{new_password}"
                                User_info.update({key:value})
                                st.session_state.sign_up = True
                                save_info(User_info,Users_information)
                                logging.info("sucessfully sign-in")
                                st.switch_page(st.Page(self.loging))
                        else:
                            key = f"{new_username}"
                            value = f"{new_password}"
                            user_data.update({key:value})
                            st.session_state.sign_up = True
                            save_info(user_data,Users_information)
                            logging.info("sucessfully sign-in")
                            st.switch_page(st.Page(self.loging))
            
                with sub_col2:
                    if st.button("cancel"):
                        st.switch_page(page=st.Page(self.home_page))
        except Exception as e:
            raise AIAssistantException(e,sys)

                
    
    def loging(self):
        try:
            if "previous_page" not in st.session_state:
                st.session_state.previous_page = None
            # Add the header with inline styles or class
            st.markdown(
            """
            <h1 style='font-size: 2em; margin-bottom: 0px; color: black;'>🔓Login</h1>
            """, 
            unsafe_allow_html=True
            )
            st.markdown(
            """
            <style>
            .stTextInput input {
                width: 500px;
            }
            .stTextInput p {
                color: black;
            }
            .stButton >button {
                width: 80px
            }
            .stButton p {
                color: black;
            }
            .stAlertContainer  {
                width: 510px;
                background-color: white;
                color: Red;
            }
            .stButton >button:hover {
                border: none;
                background-color: #9AAE91;
            }
            </style>
            """, 
            unsafe_allow_html=True
            )
        
            _,col,_ = st.columns([0.20,1,0.30])
            with col:
                Username=st.text_input("Username",placeholder="enter username")
                Password=st.text_input("Password",type="password",placeholder="enter password",max_chars=10)
                sub_col1, sub_col2 = st.columns([1,0.30])
                with sub_col1:
                    if st.button("login"):
                        User_info = load_info(Users_information)
                        if Username in User_info and User_info[Username] != Password:
                            st.error("Wrong Username or Password!:warning: OR If you have not sign-in yet, please sign-in first then login!")
                        if Username in User_info and User_info[Username] == Password:
                            st.session_state.logged_in=True
                            name=f"{Username}"
                            st.session_state.Username = name
                            st.session_state.first_letter = name[0]
                            
                            if st.session_state.previous_page:
                                logging.info("sucessfully logged in")
                                st.switch_page(page=st.session_state.previous_page)
                            else:
                                st.session_state.Username = Username
                                st.switch_page(page=st.Page(self.home_page))
                            

                with sub_col2:
                    if st.button("cancel"):
                        st.switch_page(page=st.Page(self.home_page))
        except Exception as e:
            raise AIAssistantException(e,sys)

                    

    def logout(self):
        try:
            st.markdown(
            """
            <h1 style='font-size: 2em; margin-bottom: 0px; color: black;'>🔒Log out</h1>
            """, 
            unsafe_allow_html=True
            )
            st.markdown(
            """
            <style>
            .stButton >button {
                width: 80px
            }
            .stButton{
                color: #273238;
            }
            .stButton >button:hover {
                border: none;
                background-color: #FF6347;
            }
            .stToast{
                color: black;
            }
            </style>
            """, 
            unsafe_allow_html=True
            )
        
            _,sub_col1, sub_col2,= st.columns([0.30,1,1])
            with sub_col1:
                if st.button("Log Out"):
                    st.session_state.logged_in = False
                    st.session_state.Username = None
                    st.toast("Log out Successfully")
                    time.sleep(0.5)
                    st.switch_page(page=st.Page(self.home_page))
            with sub_col2:
                if st.button("Cancel"):
                    if st.session_state.previous_page:
                        st.switch_page(page=st.session_state.previous_page)
        except Exception as e:
            raise AIAssistantException(e,sys)

    def home_page(self):
        try:
            st.markdown(
            """
            <style>
            .upper_container {
                border: 2px solid #676767; 
                padding: 5px;
                border-radius: 10px;
                margin-top: 10px;
                height: 100px;  
                width: 300px;  
                display: flex;
                align-User_infos: flex-start;  
                justify-content: flex-start;
                
            }
            .custom-container {
                border: 2px solid #FF6347; 
                padding: 5px;
                border-radius: 10px;
                margin-top: 10px;
                height: 100px;  
                width: 180px; 
                display: flex;
                align-User_infos: flex-start;  
                justify-content: flex-start;
            }
            .custom-font {
                font-size: 0.95em;
                color: #676767;
            }
            .custom-font0 {
                font-size: 1em;
                color: black;
            }
            .stToast{
                color: black;
            }
            
            [data-testid="stBaseButton-primary"] {
                background-color: white;
                color: #F08080;
            }
            
            [data-testid="stBaseButton-primary"]:hover{
                background-color: white;
                border-color: #F08080;
            }
            [data-testid="stBaseButton-primary"]:active{
                background-color: white;
                border-color: #F08080;
            }
            .circular-container {
            width: 28px;         
            height: 28px;        
            border-radius: 50%;  
            border: 1px solid #FF6347;  
            text-align: center;
            background-color: #FF6347;
            }
            </style>
            """, unsafe_allow_html=True
            )
            html_code = """
            <div style="position: relative; width: 50px; height: 30px; margin: auto;">
                <!-- Line -->
                <div id="line1" style="
                    position: absolute;
                    width: 2px;
                    height: 100px;
                    background-color:  #676767;
                    transform-origin: bottom left;
                    transform: rotate(0deg);
                "></div>
                <div id="line2" style="
                    position: absolute;
                    width: 2px;
                    height: 100px;
                    background-color:  #676767;
                    transform-origin: bottom center;
                    transform: rotate(90deg);
                "></div>
                <div id="line2" style="
                    position: absolute;
                    width: 2px;
                    height: 100px;
                    background-color:  #676767;
                    transform-origin: bottom center;
                    transform: rotate(270deg);
                "></div>
            </div>
            """
            
            
            if "Username" not in st.session_state:
                st.session_state.Username = None
            
            if st.session_state.Username:
                st.sidebar.markdown("<br><br><br><br>", unsafe_allow_html=True)
                fun(self.home_page)
                col,last_col = st.columns([1,0.20])
                with col:
                    st.markdown('<h1 style="font-size:1.85em; color:black;">E-commerece AI Assistant 💬</h1>', unsafe_allow_html=True)
                with last_col:
                    st.markdown(f'<div style="font-size:1em; color:#2F3E46;" class="circular-container">{st.session_state.first_letter}</div>', unsafe_allow_html=True)
                
                st.markdown('<p style="font-size:0.85em; color: #676767;">Would you like a personalized recommendation or prefer to negotiate? then navigate...</p>', unsafe_allow_html=True)
                _,col_m, _ = st.columns([0.40,0.50,0.70])
                with col_m:
                    st.markdown("""<div style="font-size:0.8em; color:#676767;" class="upper_container">
                                <span class="custom-font0"> 📢 Feature section and start a chat to easily find product with product's details.Enjoy Recommendation, explore options, and bargain to secure a better deal on your purchase.</span></div>""", unsafe_allow_html=True)
                st.markdown(html_code, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1,0.50])
                with col1:
                    st.markdown("""<div style="font-size:0.8em; color:#2F3E46;" class="custom-container">Get Recommendation... <br>
                                <span class="custom-font"> - 👍to receive a personalized recomendation.</span></div>""", unsafe_allow_html=True)
                with col2:
                    st.markdown("""<div style="font-size:0.8em; color:#2F3E46;" class="custom-container">Opt for negotiation... <br>
                                <span class="custom-font"> - 🤝Go for negotiation to secure a better deal and offer.</span></div>""", unsafe_allow_html=True)
            
            else:
                col,left_col,right_col= st.columns([1,0.20,0.20])
                with left_col:
                    if st.button("Sign-in",type="primary"):
                        st.switch_page(st.Page(self.signin))
                with right_col:
                    if st.button("login",type="primary"):
                        st.switch_page(st.Page(self.loging))
                with col:
                    st.markdown('<h1 style="font-size:1.85em; color:black;">E-commerece AI Assistant 💬</h1>', unsafe_allow_html=True)
                
                #st.header("E-commerece AI Assistant")
                st.markdown('<p style="font-size:0.85em; margin-bottom: 20px; color: #676767;">Would you like a personalized recommendation or prefer to negotiate? then navigate...</p>', unsafe_allow_html=True)
                _,col_m, _ = st.columns([0.40,0.50,0.70])
                with col_m:
                    st.markdown("""<div style="font-size:0.8em; color:#676767;" class="upper_container">
                                <span class="custom-font0"> 📢 Feature section and start a chat to easily find product with product's details.Enjoy Recommendation, explore options, and bargain to secure a better deal on your purchase.</span></div>""", unsafe_allow_html=True)
                st.markdown(html_code, unsafe_allow_html=True)
                col1, col2 = st.columns([1,0.50])
                with col1:
                    st.markdown("""<div style="font-size:0.8em; color:#2F3E46;" class="custom-container">Get Recommendation... <br>
                                <span class="custom-font"> - 👍to receive a personalized recomendation.</span></div>""", unsafe_allow_html=True)
                with col2:
                    st.markdown("""<div style="font-size:0.8em; color:#2F3E46;" class="custom-container">Opt for negotiation... <br>
                                <span class="custom-font"> - 🤝Go for negotiation to secure a better deal and offer.</span></div>""", unsafe_allow_html=True)
                

                if "toast_count" not in st.session_state:
                    st.session_state.toast_count = 0
                
                if st.session_state.toast_count < 1:
                    st.toast("Hello! Welcome to the app.")
                    time.sleep(0.5)
                    st.toast("let's make your experience amazing!")
                    time.sleep(0.5)
                    st.toast("Sign-in/login to use app features.")
                    st.session_state.toast_count += 1
                st.session_state.previous_page = st.Page(self.home_page)
        except Exception as e:
            raise AIAssistantException(e,sys)
            
            
    def pages(self):
        try:
        
            st.set_page_config(page_title="Chatbot",page_icon="💬")

            if "Username" not in st.session_state:
                st.session_state.Username = None
            if st.session_state.Username:
                pages = {
                
                "E-commerce AI Assistant":[st.Page(self.home_page, title="Home", icon="🏠"),],
                    
                "Feature": [ 
                    st.Page(r"src\web_app_page\Recommendation_negotiation.py", title="Let's start a chat...",icon="🪄"),
                #
                    ],

                "User's Feedback":[
                    st.Page(r"src\web_app_page\feedback_form.py",title="Feedback",icon="📋")  
                ],

                " ":[
                        st.Page(self.logout, title="Log out", icon="🔒")
                    ],
                }
                pg = st.navigation(pages)
                pg.run()
            else:
                pages = {
                
                "E-commerce AI Assistant":[st.Page(self.home_page, title="Home", icon="🏠"),],
                    
                "Feature": [ 
                    st.Page(r"src\web_app_page\Recommendation_negotiation.py", title="Let's start a chat...",icon="🪄"),
                #
                    ],

                "User's Feedback":[
                    st.Page(r"src\web_app_page\feedback_form.py",title="Feedback",icon="📋")  
                ],

                " ":[
                        st.Page(self.signin, title="Sign-in",icon="🔐"),
                        st.Page(self.loging, title="Login",icon="🔓"),
                    ],
                }
                pg = st.navigation(pages)
                pg.run()
        except Exception as e:
            raise AIAssistantException(e,sys)

        
        
    