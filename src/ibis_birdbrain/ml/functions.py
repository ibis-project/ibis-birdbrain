# imports
import marvin

from dotenv import load_dotenv

from ibis.expr.schema import Schema

from ibis_birdbrain.messages import Email
from ibis_birdbrain.attachments import DatabaseAttachment, TableAttachment


# config
load_dotenv()
marvin.settings.llm_model = "azure_openai/gpt-4"


# functions
@marvin.ai_fn
def generate_response(
    e: Email,
    instructions: str = "",
    additional_instructions: str = "",
    additional_context: str = "",
) -> str:
    """Generates a response from an email."""


@marvin.ai_fn
def filter_docs(docs: list[str], instructions: str) -> list[str]:  # type: ignore
    """Filters relevant documents from a list based on instructions."""


# @marvin.ai_fn
# def filter_cons(cons: dict[str, DatabaseAttachment], text: str) -> list[str]:  # type: ignore
#    """Filters relevant connections from a list of connections."""
#

# @marvin.ai_fn
# def filter_tables(tables: dict[str, Schema], text: str) -> list[str]:  # type: ignore
# """filter relevant  tables from a list of tables."""


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

    For instance, generate_plotly_express_figure("bar of species by count", "t", t.schema(), "species", "count") should return the string:

    'px.bar(t.group_by("species").agg(ibis._.count().name('count'))'"""
