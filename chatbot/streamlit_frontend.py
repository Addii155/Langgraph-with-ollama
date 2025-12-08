import streamlit as st
from backend import workflow
from langchain_core.messages import HumanMessage

configer = {'configurable':{'thread_id':'thread_1'}}

if 'message' not in st.session_state:
    st.session_state['message'] = []

for i in st.session_state['message']:
    with st.chat_message(i['role']):
        st.text(i['content'])


inp = st.chat_input('ask anything')

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

