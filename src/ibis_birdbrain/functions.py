# imports
import marvin

import logging as log

from ibis.expr.schema import Schema
from ibis.expr.types.relations import Table

from ibis_birdbrain.models import ProcessDocument, QueryType
from ibis_birdbrain.platforms import DataConnection
from ibis_birdbrain.classifiers import IsRelevantDataConnection

from typing import Any


# functions
def filter_docs(docs: list[str], text: str) -> list[str]:
    return _filter_docs(docs, text)


def process_doc(doc: str) -> ProcessDocument:
    return ProcessDocument(doc)  # type: ignore


def filter_cons(cons: dict[str, DataConnection], text: str) -> list[str]:
    relevant_cons = []
    for con in cons:
        if IsRelevantDataConnection(f"text: {text}\n\ncons:\n{cons[con].tables}").value:
            relevant_cons.append(con)

    return _filter_cons(cons, text)


def filter_tables(tables: dict[str, Schema], text: str) -> dict[str, Schema]:
    tables = {table: tables[table] for table in _filter_tables(tables, text)}
    return tables


def choose_query_types(text: str) -> QueryType:
    return QueryType(text)  # type: ignore


def query(con: Any, tables: dict[str, Schema], text: str) -> Table:
    tables = filter_tables(tables, text)
    log.info(f"tables: {tables}")
    sql = _write_sql_select(tables, text).strip(";")
    log.warning(f"sql: {sql}")
    return con.table(list(tables.keys())[0]).sql(sql)


# _functions
@marvin.ai_fn
def _write_sql_select(tables: dict[str, Schema], text: str) -> str:  # type: ignore
    """Returns a SQL select statement string based on the text and available table."""


@marvin.ai_fn
def _filter_docs(docs: list[str], text: str) -> list[str]:  # type: ignore
    """Filters relevant documents from a list based on a text."""


@marvin.ai_fn
def _filter_cons(cons: dict[str, DataConnection], text: str) -> list[str]:  # type: ignore
    """filter cons from a list of connections."""


@marvin.ai_fn
def _filter_tables(tables: dict[str, Schema], text: str) -> list[str]:  # type: ignore
    """filter relevant  tables from a list of tables."""
