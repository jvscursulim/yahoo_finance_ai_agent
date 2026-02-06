from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

from .nodes import (
    chat,
    get_assets_tickers,
    generate_chart,
    generate_news,
    balance_sheet,
    financials,
    # data_summary,
    # price_targets,
    check_if_user_wants_a_chart,
    check_if_user_wants_news,
    check_if_user_wants_balance,
    check_if_user_wants_financials,
    # check_if_user_wants_price_target,
    # check_if_user_wants_summary,
    router1,
    router2,
    router3,
    router4,
    # router5,
    # router6,
)
from .state import State

graph = StateGraph(State)

# Nodes
graph.add_node("chat", chat)
graph.add_node("get_assets_tickers", get_assets_tickers)
graph.add_node("generate_chart", generate_chart)
graph.add_node("generate_news", generate_news)
graph.add_node("balance_sheet", balance_sheet)
graph.add_node("financials", financials)
# graph.add_node("data_summary", data_summary)
# graph.add_node("price_targets", price_targets)
graph.add_node("check_if_user_wants_a_chart", check_if_user_wants_a_chart)
graph.add_node("check_if_user_wants_news", check_if_user_wants_news)
graph.add_node("check_if_user_wants_balance", check_if_user_wants_balance)
graph.add_node("check_if_user_wants_financials", check_if_user_wants_financials)
# graph.add_node("check_if_user_wants_price_target", check_if_user_wants_price_target)
# graph.add_node("check_if_user_wants_summary", check_if_user_wants_summary)

# Edges
graph.add_edge(START, "get_assets_tickers")
graph.add_edge("get_assets_tickers", "check_if_user_wants_a_chart")
graph.add_conditional_edges(
    "check_if_user_wants_a_chart",
    router1,
    {
        "check_if_user_wants_news": "check_if_user_wants_news",
        "generate_chart": "generate_chart",
    },
)
graph.add_edge("generate_chart", END)
graph.add_conditional_edges(
    "check_if_user_wants_news",
    router2,
    {
        "check_if_user_wants_balance": "check_if_user_wants_balance",
        "generate_news": "generate_news",
    },
)
graph.add_edge("generate_news", END)
graph.add_conditional_edges(
    "check_if_user_wants_balance",
    router3,
    {
        "check_if_user_wants_financials": "check_if_user_wants_financials",
        "balance_sheet": "balance_sheet",
    },
)
graph.add_edge("balance_sheet", END)
graph.add_conditional_edges(
    "check_if_user_wants_financials",
    router4,
    {
        "financials": "financials",
        "chat": "chat",
    },
)
graph.add_edge("financials", END)
# graph.add_conditional_edges(
#     "check_if_user_wants_price_target",
#     router5,
#     {
#         "check_if_user_wants_summary": "check_if_user_wants_summary",
#         "price_targets": "price_targets",
#     },
# )
# graph.add_edge("price_targets", END)
# graph.add_conditional_edges(
#     "check_if_user_wants_summary",
#     router6,
#     {"chat": "chat", "data_summary": "data_summary"},
# )
# graph.add_edge("price_targets", END)
graph.add_edge("chat", END)

memory = MemorySaver()
agent = graph.compile(checkpointer=memory)
