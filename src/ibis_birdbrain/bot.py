# imports
import marvin
import logging as log

from typing import Any

from ibis.expr.schema import Schema
from ibis.expr.types.relations import Table

from ibis_birdbrain.platforms import DataConnection
from ibis_birdbrain.functions import (
    filter_docs,
    filter_cons,
    filter_tables,
    choose_query_types,
    query,
)


# classes
class Bot:
    """
    Ibis Birdbrain bot.
    """

    name: str
    description: str
    system: str
    docs_con: DataConnection
    data_cons: dict[str, DataConnection] = {}

    def __init__(
        self,
        name: str = "birdbrain",
        description: str = "the portable Python AI-powered data bot",
        system: str = "a bot",
        docs_con: Any = None,
        data_cons: list[Any] = [],
    ) -> None:
        """
        Initialize a bot.
        """
        self.name = name
        self.description = description
        self.system = system

        for con in data_cons:
            self.add_data_connection(con)

        self.docs_con = DataConnection(
            con=docs_con,
            name="docs",
            description="docs",
        )

    def query(self, text: str) -> dict:
        """
        Query the bot.
        """
        query_types = choose_query_types(text)

        results = {}
        if query_types.is_docs_query:
            tables = filter_tables(self.docs_con.tables, text)
            docs: list[str] = []
            for t in tables:
                docs.extend(self.docs_con.con.table(t).filename.to_pandas().to_list())
            docs = filter_docs(docs, text)
            results["docs"] = docs

        if query_types.is_data_query:
            cons = filter_cons(self.data_cons, text)
            for con in cons:
                tables = filter_tables(self.data_cons[con].tables, text)
                t = query(self.data_cons[con].con, tables, text)
                results[con] = t

        return results

    def __call__(self, text: str) -> Any:
        return self.query(text)

    def __str__(self):
        pass

    def __repr__(self) -> str:
        return f"""
name: {self.name}
description: {self.description}
system: {self.system}

docs connection: {self.docs_con}

data connections: {self.data_cons}
""".strip()

    def use_gpt_35(self) -> None:
        """
        Use GPT-3.5-turbo-16k.
        """
        marvin.settings.llm_model = "openai/gpt-3.5-turbo-16k"

    def use_gpt_4(self) -> None:
        """
        Use GPT-4.
        """
        marvin.settings.llm_model = "openai/gpt-4"

    def add_data_connection(self, con: Any) -> None:
        """
        Add a data connection to the bot.
        """
        database_name = con.current_database
        schema_name = con.current_schema

        description = ""

        connection_name = f"{database_name}.{schema_name}"

        self.data_cons[connection_name] = DataConnection(
            con=con,
            name=connection_name,
            description=description,
        )
