import streamlit as st
import pandas as pd
from src.web_app_page.main import App
from src.utils import fun,save_feedback

filepath1 = "feedback.csv"


if "logged_in" not in st.session_state:
    st.session_state.previous_page = st.Page(r"src\web_app_page\feedback_form.py")
    st.switch_page(st.Page(App.loging, title="Login",icon="🔓")) # Redirect to login
    st.rerun()

if not st.session_state.logged_in:
    st.session_state.previous_page = st.Page(r"src\web_app_page\feedback_form.py")
    st.switch_page(st.Page(App.loging)) # Redirect to login
    st.rerun()

if st.session_state.logged_in and st.session_state.Username:
    st.sidebar.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown(
    """
    <style>
    /* Remove margin at the top of the page */
    .main > div:first-child {
        padding-top: 60px;
    }
    .stForm p{
        color: navy;
    }
    .stFormSubmitButton > button:hover{
        background-color: white;
    }
    .stButton > button:hover {
    background-color: none;
    border-color: #D9D9D9;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    _,col,_ = st.columns(3)
    with col:
        st.markdown('<p style="font-size: 1em; color: black;">Feedback Form</p>',unsafe_allow_html=True)

    fun(App.home_page)
    #dataframe = pd.DataFrame()
    with st.form("feebback form"):
        st.markdown("All * fields are mandatory")
        username=st.markdown(f"Username: {st.session_state.Username}")
        Email = st.text_input("Email*",placeholder="Email Address")
        Address = st.text_input("Address*",placeholder="Address")
        gender = st.selectbox(label='Gender*',placeholder="Select",options=['Male', 'Female'], index=None)
        age = st.slider("Age*",min_value=18)
        review = st.select_slider("How is your experience?*",options=['Bad','Good','Very good','Excellent'])
        text = st.text_input("share your experience in few word*",placeholder= "write down here",max_chars=200)
        submitted = st.form_submit_button("Submit")
        field = [Email,Address,text,gender,age,review]
        if submitted:
            for f in field:
                if f:
                    df = pd.DataFrame(
                        {
                            "Username": [f"{st.session_state.Username}"],
                            "Email":[f"{Email}"],
                            "Address": [f"{Address}"],
                            "Gender":[f"{gender}"],
                            "Age":[f"{age}"],
                            "Review":[f"{review}"],
                            "avg_rating":[f"{st.session_state.avg_rating}"],
                            "Text_review": [f"{text}"]
                        }
                    )
            
                else:
                    st.error("Please fill all mandatory field and then click on Submit")
        
            save_feedback(df,filepath1)
            st.write("Thank you for your valuable feedback")