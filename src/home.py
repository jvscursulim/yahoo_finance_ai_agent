import uuid

import streamlit as st

from langchain.messages import HumanMessage

from agent import agent
from utils import stream_data

if not "config" in st.session_state:
    st.session_state.config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

st.set_page_config(
    page_icon=":robot:",
    page_title="Yahoo Finance AI Agent",
    layout="wide"
)

st.title(":dollar: Yahoo Finance AI Agent :robot:")

st.divider()

tab1, tab2 = st.tabs(["Chat", "Agent graph"])

with tab1:
    chat_container = st.container(border=True)
    message = st.chat_input()
    state = agent.get_state(config=st.session_state.config)

    if "messages" in state.values.keys():
        for m in state.values["messages"]:
            with chat_container.chat_message(name="human" if isinstance(m, HumanMessage) else "ai"):
                st.write(m.content)

    if message:
        with chat_container.chat_message(name="human"):
            st.write(message)

        state = agent.invoke({"messages": [HumanMessage(content=message)]}, config=st.session_state.config)

        with chat_container.chat_message(name="ai"):
            st.write_stream(stream_data(text=state["messages"][-1].content))

with tab2:
    st.image(agent.get_graph().draw_mermaid_png())


