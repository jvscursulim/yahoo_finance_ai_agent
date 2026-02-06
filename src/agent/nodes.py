import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

from langchain.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from .state import (
    State,
    GetAssetsTickers,
    CheckIfUserWantsChart,
    CheckIfUserWantsNews,
    CheckIfUserWantsBalancesheet,
    # CheckIfUserWantsDataSummary,
    CheckIfUserWantsFinancials,
    # CheckIfUserWantsPriceTargets,
)

llm = ChatOllama(model="llama3.1:8b", temperature=1e-1)


def check_if_user_wants_a_chart(state: State):
    """
    Docstring for check_if_user_wants_a_chart

    :param state: Description
    :type state: State
    """

    prompt = """ 
    Verify if in user message the word 'chart' is mentioned in the
    sentence. The word chart can appears in expressions like: I would like to see a chart.
    """
    user_msg = state["messages"][-1].content
    response = llm.with_structured_output(CheckIfUserWantsChart).invoke(
        [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}]
    )

    return {"usr_wants_chart": response.usr_wants_chart}


def check_if_user_wants_news(state: State):
    """
    Docstring for check_if_user_wants_news

    :param state: Description
    :type state: State
    """

    prompt = """ You are a financial advisor and you
    need to verify if in user message the word 'news' is mentioned.
    Example: bring me the news about...
    """
    user_msg = state["messages"][-1].content
    response = llm.with_structured_output(CheckIfUserWantsNews).invoke(
        [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}]
    )

    return {"usr_wants_news": response.usr_wants_news}


def check_if_user_wants_balance(state: State):
    """
    Docstring for check_if_user_wants_balance

    :param state: Description
    :type state: State
    """

    prompt = """ You are a financial advisor and you need to verify if in user message the term 'balance sheet'
    is mentioned. Example: I would like to see the balance sheet of...
    """
    user_msg = state["messages"][-1].content
    response = llm.with_structured_output(CheckIfUserWantsBalancesheet).invoke(
        [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}]
    )

    return {"usr_wants_balance": response.usr_wants_balance}


def check_if_user_wants_financials(state: State):
    """
    Docstring for check_if_user_wants_financials

    :param state: Description
    :type state: State
    """

    prompt = """ You are an AI agent that behaves like a financial advisor. Your role here is to
    check if in user message the word 'financials' is mentioned, because we want to know if the
    user wants to see the financials of the company.
    """
    user_msg = state["messages"][-1].content
    response = llm.with_structured_output(CheckIfUserWantsFinancials).invoke(
        [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}]
    )

    return {"usr_wants_financials": response.usr_wants_financials}


# def check_if_user_wants_summary(state: State):
#     """
#     Docstring for check_if_user_wants_summary

#     :param state: Description
#     :type state: State
#     """

#     prompt = """ You need to verify if in user message it is a willing
#     to see a summary of the negociation day of the assets mentioned.
#     """
#     user_msg = state["messages"][-1].content
#     response = llm.with_structured_output(CheckIfUserWantsDataSummary).invoke(
#         [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}]
#     )

#     return {"usr_wants_summary": response.usr_wants_summary}


# def check_if_user_wants_price_target(state: State):
#     """
#     Docstring for check_if_user_wants_price_target

#     :param state: Description
#     :type state: State
#     """

#     prompt = """ You need to verify if in user message it is a willing
#     to see the price target for the assets mentioned.
#     """
#     user_msg = state["messages"][-1].content
#     response = llm.with_structured_output(CheckIfUserWantsPriceTargets).invoke(
#         [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}]
#     )

#     return {"usr_wants_price_target": response.usr_wants_price_target}


def chat(state: State):
    """
    Docstring for chat

    :param state: Description
    :type state: State
    """

    prompt = """ You are an AI agent that behaves like a financial
    advisor. If the user wants to talk about a topic that is not related
    with finance, you should say that you are not allowed to respond questions
    or talk about topics that are beyond finance scope.
    """

    system_message = [SystemMessage(content=prompt)]

    return {"messages": [llm.invoke(system_message + [state["messages"][-1]])]}


def get_assets_tickers(state: State):
    """
    Docstring for get_assets_tickers

    :param state: Description
    :type state: State
    """

    prompt = """ You need to verify if in user message it is mentioned
    any assets tickers. An asset ticker can be composed by numbers and letters.
    In general, the letters are in upper case.
    """
    user_msg = state["messages"][-1].content
    response = llm.with_structured_output(GetAssetsTickers).invoke(
        [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}]
    )

    return {"tickers": response.tickers}


def generate_chart(state: State):
    """
    Docstring for generate_chart

    :param state: Description
    :type state: State
    """

    try:
        data = yf.download(tickers=state["tickers"], period="1y")
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=data.index, y=data["Close"][asset], mode="lines", name=f"{asset}"
                )
                for asset in data.Close.columns
            ]
        )

        key = ""
        for ticker in state["tickers"]:
            key = key + " " + ticker 
        st.session_state.charts[key] = fig

        prompt = """ You are an AI agent that behaves like a financial
        advisor. You should prepare a message for the user telling that you are preparing
        a chart with the prices of the assets mentioned. The chart is generated with 1 year data
        obtained from Yahoo Finance API. You don't need to specify the timeframe.
        """

        system_message = [SystemMessage(content=prompt)]

        return {"messages": [llm.invoke(system_message + [state["messages"][-1]])]}
    except ValueError as _e:
        st.error(_e, icon="🚨")


def generate_news(state: State):
    """
    Docstring for generate_news

    :param state: Description
    :type state: State
    """

    try:
        prompt = """ You are an AI agent that behaves like a financial
        advisor. You should give a summary of the news available for the asset
        and explain them for the user. At the end of the message you should to
        mention that the news were obtained in Yahoo Finance API.
        """

        system_message = [SystemMessage(content=prompt)]

        context = ""
        for ticker in state["tickers"]:
            ticker_data = yf.Ticker(ticker=ticker)
            for news in ticker_data.news:
                aux = f"""\n
                Title: {news["content"]["title"]}
                Summary: {news["content"]["summary"]}
                \n
                """
                context = context + aux

        msg = [HumanMessage(content=context)]

        return {"messages": [llm.invoke(system_message + msg)]}
    except ValueError as _e:
        st.error(_e, icon="🚨")


def balance_sheet(state: State):
    """
    Docstring for balance_sheet
    
    :param state: Description
    :type state: State
    """
    
    try:
        prompt = """ You are an AI agent that behaves like a financial
        advisor. You should prepare a message for the user telling that balance sheet
        data will be available soon.
        """

        system_message = [SystemMessage(content=prompt)]

        for ticker in state["tickers"]:
            ticker_data = yf.Ticker(ticker=ticker)
            st.session_state.dfs["balance sheet "+ticker] = ticker_data.balance_sheet

        return {"messages": [llm.invoke(system_message + [state["messages"][-1]])]}
    except ValueError as _e:
        st.error(_e, icon="🚨")


def financials(state: State):
    """
    Docstring for financials
    
    :param state: Description
    :type state: State
    """
    
    try:
        prompt = """ You are an AI agent that behaves like a financial
        advisor. You should prepare a message for the user telling that financials data
        will be available soon.
        """

        system_message = [SystemMessage(content=prompt)]

        for ticker in state["tickers"]:
            ticker_data = yf.Ticker(ticker=ticker)
            st.session_state.dfs["financials "+ticker] = ticker_data.financials

        return {"messages": [llm.invoke(system_message + [state["messages"][-1]])]}
    except ValueError as _e:
        st.error(_e, icon="🚨")


# def price_targets(state: State):
#     """
#     Docstring for price_targets
    
#     :param state: Description
#     :type state: State
#     """
    
#     try:
#         prompt = """ You are an AI agent that behaves like a financial
#         advisor. You should prepare a message for the user telling that you are preparing
#         a chart with the prices of the assets mentioned.
#         """

#         system_message = [SystemMessage(content=prompt)]

#         context = ""
#         for ticker in state["tickers"]:
#             ticker_data = yf.Ticker(ticker=ticker)
#             for news in ticker_data.news:
#                 aux = f"""\n
#                 Title: {news["content"]["title"]}
#                 Summary: {news["content"]["summary"]}
#                 \n
#                 """
#                 context = context + aux

#         msg = [HumanMessage(content=context)]

#         return {"messages": [llm.invoke(system_message + msg)]}
#     except ValueError as _e:
#         st.error(_e, icon="🚨")


# def data_summary(state: State):
#     """
#     Docstring for data_summary
    
#     :param state: Description
#     :type state: State
#     """

#     try:
#         prompt = """ You are an AI agent that behaves like a financial
#         advisor. You should give a summary of the news available for the asset
#         and explain them for the user. At the end of the message you should to
#         mention that the news were obtained in Yahoo Finance API.
#         """

#         system_message = [SystemMessage(content=prompt)]

#         context = ""
#         for ticker in state["tickers"]:
#             ticker_data = yf.Ticker(ticker=ticker)
#             for news in ticker_data.news:
#                 aux = f"""\n
#                 Title: {news["content"]["title"]}
#                 Summary: {news["content"]["summary"]}
#                 \n
#                 """
#                 context = context + aux

#         msg = [HumanMessage(content=context)]

#         return {"messages": [llm.invoke(system_message + msg)]}
#     except ValueError as _e:
#         st.error(_e, icon="🚨")


def router1(state: State):
    """
    Docstring for router1

    :param state: Description
    :type state: State
    """

    if state["usr_wants_chart"]:
        return "generate_chart"
    else:
        return "check_if_user_wants_news"


def router2(state: State):
    """
    Docstring for router2

    :param state: Description
    :type state: State
    """

    if state["usr_wants_news"]:
        return "generate_news"
    else:
        return "check_if_user_wants_balance"


def router3(state: State):
    """
    Docstring for router3

    :param state: Description
    :type state: State
    """

    if state["usr_wants_balance"]:
        return "balance_sheet"
    else:
        return "check_if_user_wants_financials"


def router4(state: State):
    """
    Docstring for router4

    :param state: Description
    :type state: State
    """

    if state["usr_wants_financials"]:
        return "financials"
    else:
        return "chat"


# def router5(state: State):
#     """
#     Docstring for router5

#     :param state: Description
#     :type state: State
#     """

#     if state["usr_wants_price_target"]:
#         return "price_targets"
#     else:
#         return "check_if_user_wants_summary"


# def router6(state: State):
#     """
#     Docstring for router6

#     :param state: Description
#     :type state: State
#     """

#     if state["usr_wants_summary"]:
#         return "data_summary"
#     else:
#         return "chat"
