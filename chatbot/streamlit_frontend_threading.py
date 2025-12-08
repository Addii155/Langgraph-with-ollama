import streamlit as st
from backend import workflow
from langchain_core.messages import HumanMessage
import uuid

# ******************* Utility Func *************************

def reset_chat():
    thread_id= generate_thread_id()
    st.session_state['thread_history'].append(thread_id)
    st.session_state['thread_id'] = thread_id
    st.session_state['message'] = []

def add_threadid(thread_id):
    if thread_id not in st.session_state['thread_history']:
        st.session_state['thread_history'].append(thread_id)


def generate_thread_id():
    thread_id= uuid.uuid4()
    return thread_id



if 'message' not in st.session_state:
    st.session_state['message'] = []

if 'thread_history' not in st.session_state:
    st.session_state['thread_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()


# ******************* Sidebar UI *************************

st.sidebar.title('Langgraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.title('My conversations')

add_threadid(st.session_state['thread_id'])

for thread in st.session_state['thread_history']:
    st.sidebar.write(f"Thread ID: {thread}")




for i in st.session_state['message']:
    with st.chat_message(i['role']):
        st.text(i['content'])


inp = st.chat_input('ask anything')

configer = {'configurable':{'thread_id':st.session_state['thread_id']}}

if inp:
    st.session_state['message'].append({'role':'user','content':inp})
    with st.chat_message('user'):
        st.text(inp)
    
    with st.chat_message('assistant'):
        aimsg = st.write_stream(
               message_chunk.content for message_chunk,metadata in  workflow.stream({'message':[HumanMessage(content=inp)]},
                config=configer,
                stream_mode='messages'
                )
        )
    st.session_state['message'].append({'role':'assistant','content':aimsg})

