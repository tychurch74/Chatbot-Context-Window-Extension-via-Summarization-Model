import streamlit as st
import os
from streamlit_chat import message
from modules.chatGPT import ChatGPT

openai_api_key = os.environ["OPENAI_API_KEY"]
enable_json_output = True
num_iterations = 5
chunk_size = 4
completion_file_path = "testing_data/json_data/semantic_search_test-1_completion.json"
message_history_file_path = "testing_data/json_data/semantic_search_test-1_message_history.json"
    
chat_gpt = ChatGPT(openai_api_key, enable_json_output=enable_json_output, chunk_size=chunk_size, completion_file_path=completion_file_path)

def get_initial_message():
    messages=[]

    return messages


if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Query: ", key="input")

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        response = chat_gpt.chat(query)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

    with st.expander("Show Messages"):
        st.write(messages)


