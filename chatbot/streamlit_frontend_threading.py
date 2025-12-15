import streamlit as st
from backend_tools import chatbot
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
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
    state = chatbot.get_state(config={'configurable':{'thread_id':thread_id}})
    if state.values and 'messages' in state.values:
        return state.values['messages']
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

configer = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_turn",
    }

if inp:
    # if st.session_state['message'] ==[]:
    #     st.session_state['thread_name'].append({st.session_state['thread_id']:chatNameResponse.invoke({'message':inp})['message']})
    st.session_state['message'].append({'role':'user','content':inp})
    with st.chat_message('user'):
        st.text(inp)
    
    with st.chat_message("assistant"):
        # Use a mutable holder so the generator can set/modify it
        status_holder = {"box": None}

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=inp)]},
                config=configer,
                stream_mode="messages",
            ):
                # Lazily create & update the SAME status container when any tool runs
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}` …", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}` …",
                            state="running",
                            expanded=True,
                        )

                # Stream ONLY assistant tokens
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

        # Finalize only if a tool was actually used
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished", state="complete", expanded=False
            )

    # Save assistant message
    st.session_state["message"].append(
        {"role": "assistant", "content": ai_message}
    )