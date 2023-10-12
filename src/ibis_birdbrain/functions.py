# imports
import os
import glob
import ibis
import marvin

import logging as log

from typing import Any
from itertools import islice

from ibis.expr.schema import Schema
from ibis.expr.types.relations import Table

from ibis_birdbrain.models import ProcessDocument, QueryType
from ibis_birdbrain.platforms import DataConnection

# functions


def ingest_docs(docs_path: str, docs: list[str], con: Any) -> None:
    for doc_dir in docs:
        if doc_dir in con.list_tables():
            log.warn(f"Table {doc_dir} already exists, skipping ingestion...")
            continue

        log.info(f"Processing {doc_dir}...")
        files = sorted(_find_docs(os.path.join(docs_path, doc_dir)))
        contents = [_read_doc(file) for file in files]
        data = {
            "filename": files,
            "content": contents,
        }

        t = ibis.memtable(data)
        t = t.mutate(token_estimate=t.content.length() // 4)

        log.info(f"Creating {doc_dir} table...")
        con.create_table(doc_dir, t)

    for table in con.list_tables():
        if table.startswith("_ibis"):
            log.info(f"Dropping {table}")
            con.drop_view(table)


# functions
def internet_query(
    query: str = "what is the Ibis project?", n_results: int = 8
) -> list[dict[str, str | None]]:
    """Searches the internet for the given query."""
    from duckduckgo_search import DDGS

    ddgs = DDGS()
    return [r for r in islice(ddgs.text(query, backend="lite"), n_results)]


def webpage_to_str(url: str = "https://ibis-project.org") -> str:
    """Reads a webpage link into a string. Useful for summarizing webpages."""
    import requests
    from html2text import html2text

    response = requests.get(url)
    return html2text(response.text)


def open_browser(url: str) -> str:
    """Opens the URL in a web browser."""
    try:
        import webbrowser

        webbrowser.open(url.strip("/"))
    except Exception as e:
        return str(e)

    return f"Opened {url} in the user's web browser."


def filter_docs(docs: list[str], text: str) -> list[str]:
    return _filter_docs(docs, text)


def process_doc(doc: str) -> ProcessDocument:
    return ProcessDocument(doc)  # type: ignore


def filter_cons(cons: dict[str, DataConnection], text: str) -> list[str]:
    return _filter_cons(cons, text)


def filter_tables(tables: dict[str, Schema], text: str) -> dict[str, Schema]:
    tables = {table: tables[table] for table in _filter_tables(tables, text)}
    return tables


def choose_query_types(text: str) -> QueryType:
    return QueryType(text)  # type: ignore


def data_query(con: Any, tables: dict[str, Schema], text: str) -> Table:
    tables = filter_tables(tables, text)
    log.info(f"tables: {tables}")
    sql = _write_sql_select(tables, text).strip(";")
    log.warning(f"sql: {sql}")
    return con.table(list(tables.keys())[0]).sql(sql)


# _functions
def _find_docs(path, extensions=None) -> list[str]:
    if extensions is None:
        extensions = ["md", "qmd", "txt", "py"]

    files = []
    for ext in extensions:
        files.extend(glob.glob(f"{path}/**/*.{ext}", recursive=True))

    return files


def _read_doc(doc: str) -> str:
    try:
        with open(doc, "r") as f:
            return f.read()
    except:
        return "Error reading file"


# _functions (AI)
@marvin.ai_fn
def _write_sql_select(tables: dict[str, Schema], text: str) -> str:  # type: ignore
    """Returns a SQL select statement string based on the text and available table."""


@marvin.ai_fn
def _filter_docs(docs: list[str], text: str) -> list[str]:  # type: ignore
    """Filters relevant documents from a list based on a text."""


@marvin.ai_fn
def _filter_cons(cons: dict[str, DataConnection], text: str) -> list[str]:  # type: ignore
    """Filters relevant connections from a list of connections."""


@marvin.ai_fn
def _filter_tables(tables: dict[str, Schema], text: str) -> list[str]:  # type: ignore
    """filter relevant  tables from a list of tables."""
