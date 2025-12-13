import streamlit as st
from backend_tools import workflow
from langchain_core.messages import HumanMessage
import uuid
from give_name_conversation import chatNameResponse
from backend_tools import get_all_thread_id
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
    thread_id= str(uuid.uuid4())
    # st.session_state['thread_name'].append({thread_id:'New Chat'})
    return thread_id

def load_conversation(thread_id):
    state = workflow.get_state(config={'configurable':{'thread_id':thread_id}})
    if state.values and 'message' in state.values:
        return state.values['message']
    return []
    


if 'message' not in st.session_state:
    st.session_state['message'] = []

if 'thread_history' not in st.session_state:
    st.session_state['thread_history'] = get_all_thread_id()

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = st.session_state['thread_history'][-1] if st.session_state['thread_history'] else generate_thread_id()
    
if 'thread_name' not in st.session_state:
    st.session_state['thread_name'] = []

# ******************* Sidebar UI *************************

st.sidebar.title('Langgraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.title('My conversations')

add_threadid(st.session_state['thread_id'])

for thread in st.session_state['thread_history']:
    # threadName = 'New Chat'
    # for name in st.session_state['thread_name']:
    #     if thread in name:
    #         threadName = name[thread]
    if st.sidebar.button(str(thread),key=thread):
        msg = load_conversation(thread)
        formate_msg =[]
        for i in msg:
            if isinstance(i, HumanMessage):
                formate_msg.append({'role':'user','content':i.content})
            else:
                formate_msg.append({'role':'assistant','content':i.content})
            
        st.session_state['message'] = formate_msg
        st.session_state['thread_id'] = thread
        st.rerun()
        

for i in st.session_state['message']:
    with st.chat_message(i['role']):
        st.text(i['content'])


inp = st.chat_input('ask anything')

configer = {'configurable':{'thread_id':st.session_state['thread_id']}}

if inp:
    # if st.session_state['message'] ==[]:
    #     st.session_state['thread_name'].append({st.session_state['thread_id']:chatNameResponse.invoke({'message':inp})['message']})
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

