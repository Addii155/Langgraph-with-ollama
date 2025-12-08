import streamlit as st
from backend import workflow
from langchain_core.messages import HumanMessage

configer = {'configurable':{'thread_id':'1'}}

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
    res = workflow.invoke({'message':[HumanMessage(content=inp)]},config=configer)
    st.session_state['message'].append({'role':'assistant','content':res['message'][-1].content})
    with st.chat_message('assistant'):
        st.text(res['message'][-1].content)

