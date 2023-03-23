import os
import openai
import streamlit as st
from streamlit_chat import message
import json
import sys
sys.path.append("../specialized_chatbot/")
sys.path.append("../specialized_chatbot/specialized_chatbot")
from specialized_chatbot import chatbot
# from streamlit.report_thread import get_report_ctx

DATAPATH = '../data'
CHATBOT_PATH = '../bot.json'


#bot = chatbot.Chatbot(DATAPATH)

# Call OpenAI API to receive response



def chat_page():
    if 'bot' not in st.session_state:
        st.session_state['bot'] = chatbot.Chatbot.load_from_disk(CHATBOT_PATH)

    try:
        openai.api_key = st.secrets['OPENAI_API_KEY']
        model_engine = st.secrets['MODEL_ENGINE']
    except:
        openai.api_key = os.environ['OPENAI_API_KEY']
        model_engine = os.environ['MODEL_ENGINE']

    # Page setup
    # Disable hamburger & footer
    hide_menu_style = """
            <style>
            MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after{
                content: "Copyright @ 2023 Artefact. All Rights Reserved";
                visibility: visible;
                display: block;
                position: relative;
                color: #66CCCC;
                padding: 5px;
                top: 2px;
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    # Header setup
    header = """
            <h1 style="color:#ff0066;font-size:43px;">
            Artefact ChatBot
            </h1>
            """
    st.markdown(header, unsafe_allow_html=True)

    # Sidebar setup, with About, Parameter sliders & Doc reference
    with st.sidebar:
        st.image('artefact.png', use_column_width='always')
        st.write('\n')
        header1 = """
                <h1 style="color:#ff0066;font-size:20px;">
                About
                </h1>
                """
        st.markdown(header1, unsafe_allow_html=True)
        st.write(f'This is a ChatBot powered by OpenAI & Streamlit for Artefact internal use. Currently, the model engine it loads is {model_engine}.')
        header2 = """
                <h1 style="color:#ff0066;font-size:20px;">
                Available Parameters
                </h1>
                """
        st.markdown(header2, unsafe_allow_html=True)
        temp_inst= """
                <h2 style="color:#66CCCC;font-size:17px;">
                Temperature
                </h2>
                """
        st.markdown(temp_inst, unsafe_allow_html=True)
        temperature = st.slider(
        "Increase to generate more random responses. Default = 0.4", 0.0, 2.0, 0.4, 0.01, key="temperature")
        pres_inst= """
                <h2 style="color:#66CCCC;font-size:17px;">
                Presence penalty
                </h2>
                """
        st.markdown(pres_inst, unsafe_allow_html=True)
        presence_penalty = st.slider(
        "Increase to encourage model to talk about new topic. Default = 0", -2.0, 2.0, 0.0, 0.01, key="presence_penalty")
        freq_inst= """
                <h2 style="color:#66CCCC;font-size:17px;">
                Frequency penalty
                </h2>
                """
        st.markdown(freq_inst, unsafe_allow_html=True)
        frequency_penalty = st.slider(
        "Increase to penalize model for repeating the same line verbatim. Default = 0", -2.0, 2.0, 0.0, 0.01, key="frequency_penalty")
        header3 = """
                <h1 style="color:#ff0066;font-size:20px;">
                Help
                </h1>
                """
        st.markdown(header3, unsafe_allow_html=True)
        st.write("Please refer to [OpenAI API documentation](https://platform.openai.com/docs/api-reference/completions/create) for detailed information about the parameters.",
                 unsafe_allow_html=True)

    # Storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if 'return_text' not in st.session_state:
        st.session_state['return_text'] = ''

    # Chat now!
    text_form = st.form(key='my_form', clear_on_submit=True)
    with text_form:
        user_input = st.text_input(label="You:", value='', placeholder="Please enter your Question.")
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        try:
            # st.session_state['bot'].question_list = st.session_state['past'].copy()
            # bot.answer_list = st.session_state["generated"].copy()
            output = st.session_state['bot'].continue_conversation(user_input)
        except Exception as e:
            print(e)
            # bot = chatbot.Chatbot(DATAPATH)
            st.session_state['bot'] = chatbot.Chatbot.load_from_disk(CHATBOT_PATH)
            # bot.question_list = st.session_state['past'].copy()
            # bot.answer_list = st.session_state["generated"].copy()
            output = st.session_state['bot'].continue_conversation(user_input)
        output = output.strip()

        # print(st.session_state.past)
        # print(user_input)
        # print(output)
        # print('-'*10)
        # print(bot.question_list)
        # print('-'*10)

        # store the output
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

        # bot.question_list = st.session_state['past']
        # bot.answer_list = st.session_state["generated"]

        if st.session_state['generated']:
            # enable codes below to test parameter changes
            # message(f"""
            # Current temperature is {st.session_state.temperature},
            # presence_penalty is {st.session_state.presence_penalty},
            # frequency_penalty is {st.session_state.frequency_penalty}
            # """)
            for i in range(len(st.session_state['generated']) - 1, -1, -1):
                message(st.session_state["generated"][i], key=str(i))
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
