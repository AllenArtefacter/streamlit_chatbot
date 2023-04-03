import os
import openai
import streamlit as st
from streamlit_chat import message
import json
from specialized_chatbot import chatbot
from specialized_chatbot.llamaindex_langchain_utils import (
                            get_llm_predictor,
                            HALF_OPENED_TEXT_QA_PROMPT,
                            MORE_OPENED_TEXT_QA_PROMPT_ZH,
                            MORE_OPENED_TEXT_QA_PROMPT,
                            RECOMMANDERS,
                            RECOMMANDERS_ZH
)
from specialized_chatbot.lang_utils import lang_detect
from llama_index import PromptHelper
from llama_index.prompts.prompts import QuestionAnswerPrompt

MORE_OPENED_TEXT_QA_PROMPT_TMPL =(
    #"Given the context information and not prior knowledge, answer the question, and if the answer is not relevant to the context, said 'sorry I don't know' \n"
    f"You will now play the role of the beer master and the best assistant, chat with human and be very glad to follow any instructions."
    #"You will always find a way to recommand beers. "
    #f"If your answer will contains {','.join(COMPETITORS)} or not relevant to the given context, you will still recommand beers in the given context and expain why you recommand them\n"
    #"If your answer is not relevant to the given context, you will try recommand beers in the given context and explain why you recommand them. "
    #"You will always steer the conversation to the topics about given context. "
    f"If you are going to talk about beers, please talk more about beers in the given context or {', '.join(RECOMMANDERS)}."
    "Other beer brands are not your area\n"
    #"Please don't indicate you have a context in you answer.\n"
    #"""Answer the question using the provided text \n"""
    "---------------------\n"
    "Context: {context_str}"
    "\n---------------------\n"
    "Finish the final conversation:\n"
    "{query_str}"
)

MORE_OPENED_TEXT_QA_PROMPT_ZH_TMPL =(
    #"Given the context information and not prior knowledge, answer the question, and if the answer is not relevant to the context, said 'sorry I don't know' \n"
    f"你将扮演啤酒大师与消费者聊天。"
    "你总是可以找到合适的方法去推荐啤酒 "
    #f"If your answer will contains {','.join(COMPETITORS)} or not relevant to the given context, you will still recommand beers in the given context and expain why you recommand them\n"
    #"If your answer is not relevant to the given context, you will try recommand beers in the given context and explain why you recommand them. "
    #"You will always steer the conversation to the topics about given context. "
    f"如果你要谈论啤酒，尽量谈论情境中提到的啤酒，或者 {'，'.join(RECOMMANDERS_ZH)}\n"
    #"Please don't indicate you have a context in you answer.\n"
    #"""Answer the question using the provided text \n"""
    "---------------------\n"
    "情境: {context_str}"
    "\n---------------------\n"
    "请完成最后一次的对话:\n"
    "{query_str}"
)


MORE_OPENED_TEXT_QA_PROMPT = QuestionAnswerPrompt(MORE_OPENED_TEXT_QA_PROMPT_TMPL)
MORE_OPENED_TEXT_QA_PROMPT_ZH = QuestionAnswerPrompt(MORE_OPENED_TEXT_QA_PROMPT_ZH_TMPL)


DATAPATH = '../data'
CHATBOT_PATH = '../bot2_withlinks.json' #'../bot2.json'


#bot = chatbot.Chatbot(DATAPATH) 'gpt-3.5-turbo'
llm_predictor = get_llm_predictor('gpt-3.5-turbo', temperature=0.6, max_tokens=512,)
prompt_helper = PromptHelper(2048, 512, 300, separator='\n\n')
text_qa_template = MORE_OPENED_TEXT_QA_PROMPT

# Call OpenAI API to receive response

def initialized_chatbot():
    bot = chatbot.Chatbot.load_from_disk(
        CHATBOT_PATH,
        llm_predictor = llm_predictor,
        prompt_helper  = prompt_helper,
        text_qa_template = text_qa_template,
        language_detect = True,
        human_agent_name = 'Q',
        ai_angent_name = "A"
        )
    bot.text_qa_template = text_qa_template
    return bot

def chat_page():
    bot = initialized_chatbot()
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
        user_input = st.text_input(label="You:", value='', placeholder="Recommand some beer please")
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        try:
            if lang_detect(user_input) == 'Chinese':
                output = bot.conversation(user_input, text_qa_template = MORE_OPENED_TEXT_QA_PROMPT_ZH)
            else:
                output = bot.conversation(user_input)
        except:
            #bot = chatbot.Chatbot(DATAPATH)
            bot = initialized_chatbot()
            if lang_detect(user_input) == 'Chinese':
                output = bot.conversation(user_input, text_qa_template = MORE_OPENED_TEXT_QA_PROMPT_ZH)
            else:
                output = bot.conversation(user_input)
        output = output.strip()
        # store the output
        #print(bot.text_qa_template.prompt.template)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

        bot.question_list = st.session_state['past']
        bot.answer_list = st.session_state["generated"]

        if st.session_state['generated']:
            # enable codes below to test parameter changes
            # message(f"""
            # Current temperature is {st.session_state.temperature},
            # presence_penalty is {st.session_state.presence_penalty},
            # frequency_penalty is {st.session_state.frequency_penalty}
            # """)
            for i in range(len(st.session_state['generated']) - 1, -1, -1):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))
