import uuid

import streamlit as st

from langchain.messages import HumanMessage

from agent import agent
from utils import stream_data

if "config" not in st.session_state:
    st.session_state.config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

if "charts" not in st.session_state:
    st.session_state.charts = {}

if "dfs" not in st.session_state:
    st.session_state.dfs = {}

st.set_page_config(
    page_icon=":robot:",
    page_title="Yahoo Finance AI Agent",
    layout="wide"
)

st.title(":dollar: Yahoo Finance AI Agent :robot:")

st.divider()

st.warning(
    body="""Important Notice:
    This system is an experimental AI agent developed solely for academic and learning purposes. 
    It is not a registered investment advisor and does not offer personalized or professional financial advice.
    Any financial analysis or commentary produced by this agent should be treated as hypothetical and illustrative only. 
    Users assume full responsibility for any actions taken based on its outputs.
    """,
    icon="⚠️"
)

st.divider()

tab1, tab2 = st.tabs(["Chat", "Agent graph"])

with tab1:
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        chat_container = st.container(border=True)
        message = st.chat_input()
        state = agent.get_state(config=st.session_state.config)

        if "messages" in state.values.keys():
            for m in state.values["messages"]:
                with chat_container.chat_message(name="human" if isinstance(m, HumanMessage) else "ai", width="content"):
                    st.write(m.content)

        if message:
            with chat_container.chat_message(name="human", width="content"):
                st.write(message)

            with chat_container.chat_message(name="ai"):
                with st.spinner(text="Processing your message..."):
                    state = agent.invoke(
                        {
                            "messages": [HumanMessage(content=message)]
                        },
                        config=st.session_state.config
                    )

                if not isinstance(state["messages"][-1], HumanMessage):
                    st.write_stream(stream_data(text=state["messages"][-1].content))
    with col2:

        if not st.session_state.charts == {}:
            st.header("Charts history")
            options = st.session_state.charts.keys()
            chart_selected = st.selectbox(
                label="Chart index", 
                options=options, 
                index=len(options)-1
            )
            st.plotly_chart(st.session_state.charts[chart_selected])

        if not st.session_state.dfs == {}:
            st.header("Data history")
            options = st.session_state.dfs.keys()
            df_selected = st.selectbox(
                label="Data index", 
                options=options, 
                index=len(options)-1
            )
            st.dataframe(st.session_state.dfs[df_selected])
            if st.button("Save data"):
                st.session_state.dfs[df_selected].to_csv(f"{df_selected}.csv")
                st.success("Data saved with success!", icon="✅")

    with st.expander(label="Debug", icon="🐞"):
        st.write(agent.get_state(config=st.session_state.config))

with tab2:
    st.image(agent.get_graph().draw_mermaid_png())


