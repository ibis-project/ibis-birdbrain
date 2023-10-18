# imports
import marvin

from dotenv import load_dotenv

from ibis.expr.schema import Schema


# config
load_dotenv()
marvin.settings.llm_model = "azure_openai/gpt-4"


# functions
@marvin.ai_fn
def choose_con(text: str, cons: list[str]) -> str:
    """Chooses a connection from a list of connections based on a language query"""


@marvin.ai_fn
def choose_tables(text: str, tables: dict[str, Schema]) -> list[str]:
    """Chooses a table from a list of tables based on a language query"""


@marvin.ai_fn
def generate_search_terms(text: str) -> list[str]:
    """Generates search semantic terms from text to improve results from major search engines"""


@marvin.ai_fn
def generate_sql_select(
    query: str,
    table_names: list[str],
    schema: list[Schema],
    dialect: str = "duckdb (postgres)",
) -> str:
    """Generates a SQL SELECT statement from a language query, list of table names, and list of table schemas.

    Includes 'LIMIT 1000' unless otherwise specified in the query."""


@marvin.ai_fn
def generate_plotly_express_figure(
    query: str,
    table_variable: str = "t",
    table_schema: Schema = None,
    x_variable: str = "x",
    y_variable: str = "y",
):
    """Generates a Plotly Express figure from a language query, table variable, x variable, and y variable
    j
For instance, generate_plotly_express_figure("bar of species by count", "t", t.schema(), "species", "count") should return the string:

'px.bar(t.group_by("species").agg(ibis._.count().name('count'))'
"""
    