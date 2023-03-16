import os
from dotenv.main import load_dotenv
load_dotenv()
import streamlit as st
import streamlit_authenticator as stauth
from chatgpt import chat_page


try:
    auth = {'credentials': {'usernames': {st.secrets['username']: {
        'name': st.secrets['username'],
        'password': st.secrets['password']}}}}

    authenticator = stauth.Authenticate(
        auth['credentials'],
        st.secrets['cookie']['name'],
        st.secrets['cookie']['key'],
        st.secrets['cookie']['expiry_days'],
        st.secrets['preauthorized']
    )
except:
    auth = {'credentials': {'usernames': {os.environ['username_bot']: {
        'name': os.environ['username_bot'],
        'password': os.environ['password_bot']}}}}

    authenticator = stauth.Authenticate(
        auth['credentials'],
        os.environ['cookie_name_bot'],
        os.environ['cookie_key_bot'],
        int(os.environ['cookie_expiry_days'])
    )

name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    col1, col2 = st.columns([6, 1])
    with col1:
        chat_page()
        # st.subheader('Under maintenance......will be back soon')
    with col2:
        authenticator.logout('Logout', 'main')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
