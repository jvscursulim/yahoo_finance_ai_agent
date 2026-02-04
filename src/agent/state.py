import operator

from langchain.messages import AnyMessage
from pydantic import BaseModel, Field
from typing import Annotated, List, TypedDict, Literal


class State(TypedDict):
    """
    Docstring for State
    """

    messages: Annotated[List[AnyMessage], operator.add]
    tickers: List[str]
    usr_wants_chart: bool
    usr_wants_news: bool
    usr_wants_balance: bool
    usr_wants_financials: bool
    usr_wants_summary: bool
    usr_wants_price_target: bool


class GetAssetsTickers(BaseModel):
    """
    Verify if in user message has assets tickers
    and if there are add them in a list.
    """

    tickers: List[str] = Field(
        default=[],
        description="""
        Check if in user message it is mentioned any assets tickers. 
        Tickers in gerenal are composed by upper case letters and can have numbers. 
        Return the assets tickers if there are any, otherwise return None
        """,
    )


class CheckIfUserWantsChart(BaseModel):
    """
    Verify if user message has any intetion
    to see or generate a chart.
    """

    usr_wants_chart: Literal[True, False] = Field(
        default=False,
        description="""
        Check if in user message there is a willing to generate a chart. 
        Return 'True' if positive or 'False' if negative
        """,
    )


class CheckIfUserWantsNews(BaseModel):
    """
    Docstring for CheckIfUserWantsNews
    """

    usr_wants_news: Literal[True, False] = Field(
        default=False,
        description="""
        Check if in user message there is a willing to known more
        about the news of the desired assets.
        """,
    )


class CheckIfUserWantsBalancesheet(BaseModel):
    """
    Docstring for CheckIfUserWantsBalancesheet
    """

    usr_wants_balance: Literal[True, False] = Field(
        default=False,
        description="""
        Check if in user message there is a willing to see
        assets balance sheet.
        """,
    )


class CheckIfUserWantsFinancials(BaseModel):
    """
    Docstring for CheckIfUserWantsFinancials
    """

    usr_wants_financials: Literal[True, False] = Field(
        default=False,
        description="""
        Check if in user message there is a willing to see
        assets financials.
        """,
    )


class CheckIfUserWantsDataSummary(BaseModel):
    """
    Docstring for CheckIfUserWantsDataSummary
    """

    usr_wants_summary: Literal[True, False] = Field(
        default=False,
        description="""
        Check if in user message there is a willing to
        know assets data summary.
        """,
    )


class CheckIfUserWantsPriceTargets(BaseModel):
    """
    Docstring for CheckIfUserWantsPriceTargets
    """

    usr_wants_price_target: Literal[True, False] = Field(
        default=False,
        description="""
        Check if in user message there is a willing to know
        the price target defined by analysts for the assets.
        """,
    )
