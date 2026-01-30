import operator

from langchain.messages import AnyMessage
from typing import Annotated, TypedDict


class State(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


    