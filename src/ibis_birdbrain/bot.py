# imports
import os
import uuid
import ibis
import marvin
import datetime

import pyarrow as pa
import logging as log

from typing import Any
from dotenv import load_dotenv
from rich.console import Console

from ibis.expr.schema import Schema
from ibis.expr.types.relations import Table

from ibis_birdbrain.systems import default
from ibis_birdbrain.platforms import DataConnection
from ibis_birdbrain.functions import (
    ingest_docs,
    filter_docs,
    filter_cons,
    filter_tables,
    choose_query_types,
    data_query,
    internet_query,
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
    system_con: DataConnection

    session_id = str(uuid.uuid4())
    session_timestamp = datetime.datetime.now()

    def __init__(
        self,
        name: str = "birdbrain",
        description: str = "the portable Python AI-powered data bot",
        system: str = "a bot",
        docs_con: Any = None,
        data_cons: list[Any] = [],
        system_con: Any = None,
    ) -> None:
        """
        Initialize a bot.
        """

        self._marvin_setup()

        self.name = name
        self.description = description
        self.system = system
        self.tui = Console().print

        for con in data_cons:
            self.add_data_connection(con)

        self.docs_con = DataConnection(
            con=docs_con,
            name="docs",
            description="docs",
        )

        self.system_con = DataConnection(
            con=system_con,
            name="birdbrain",
            description="birdbrain system",
        )

        text_record = self._text_record(
            "---session start---",
            call_id=self.session_id,
            text_to="birdbrain",
            text_from="Ibis developers",
        )

        if "text_history" not in self.system_con.list_tables():
            self.system_con.create_table("text_history", text_record)
        else:
            self.system_con.insert("text_history", text_record)

    def _marvin_setup(self):
        # load .env
        load_dotenv()

        # ai platform
        marvin.settings.azure_openai.api_type = "azure"
        marvin.settings.azure_openai.api_key = os.getenv("MARVIN_AZURE_OPENAI_API_KEY")
        marvin.settings.azure_openai.api_base = os.getenv(
            "MARVIN_AZURE_OPENAI_API_BASE"
        )
        marvin.settings.azure_openai.deployment_name = os.getenv(
            "MARVIN_AZURE_OPENAI_DEPLOYMENT_NAME"
        )
        marvin.settings.llm_model = "azure_openai/gpt-4-32k"

    def query(self, text: str, call_id: str) -> dict:
        """
        Query the bot.
        """
        query_types = choose_query_types(text)

        results = {}
        if query_types.is_docs_query:
            tables = filter_tables(self.docs_con.tables, text)
            docs: list[str] = []
            for t in tables:
                docs.extend(self.docs_con.table(t).filename.to_pandas().to_list())
            docs = filter_docs(docs, text)
            results["docs"] = docs

        if query_types.is_data_query:
            cons = filter_cons(self.data_cons, text)
            for con in cons:
                tables = filter_tables(self.data_cons[con].tables, text)
                t = data_query(self.data_cons[con].con, tables, text)
                results[con] = t

        if query_types.is_internet_query:
            results["internet"] = internet_query(text)

        return results

    def __call__(self, text: str) -> Any:
        call_id = str(uuid.uuid4())

        text_record = self._text_record(text, call_id=call_id, text_from="user")
        self.system_con.insert("text_history", text_record)

        self.tui(f"{self.name}: ", style="bold violet blink", end="")
        self.tui(f"working...", style="bold blue", end="")

        res = self.query(text, call_id=call_id)
        text_record = self._text_record(str(res), call_id=call_id, text_to="user")
        self.system_con.insert("text_history", text_record)

        self.tui(f"done!", style="bold blue")
        self.tui(f"{res}", style="bold violet")

        return res

    def _text_record(
        self, text: str, call_id, text_to="birdbrain", text_from="birdbrain"
    ) -> Table:
        text_id = str(uuid.uuid4())
        text_timestamp = datetime.datetime.now()

        return ibis.memtable(
            pa.Table.from_pydict(
                {
                    "session_id": [self.session_id],
                    "session_timestamp": [self.session_timestamp],
                    "call_id": [call_id],
                    "text_timestamp": [text_timestamp],
                    "text_from": [text_from],
                    "text_to": [text_to],
                    "text": [text],
                    "text_id": [text_id],
                }
            )
        )

    def __str__(self):
        pass

    def __repr__(self) -> str:
        return f"""
name: {self.name} ({self.description})
session_id: {self.session_id}
session_start: {self.session_timestamp}

docs connection:
{self.docs_con}

data connections:
{self.data_cons}

system connection:
{self.system_con}
""".strip()

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


# system data
bb_con = ibis.connect("duckdb://data/ddbs/birdbrain.ddb")

# data platforms
tpch_con = ibis.connect("duckdb://data/ddbs/tpch_100.ddb")
imdb_con = ibis.connect("duckdb://data/ddbs/imdb.ddb")
local_con = ibis.connect("duckdb://")

data_cons = [tpch_con, imdb_con, local_con]

# docs data
docs_path = "data/docs/"
docs = os.listdir(docs_path)
log.warning(f"docs: {docs}")

# ingest docs into docs con to use like any data con!
docs_con = ibis.connect("duckdb://data/ddbs/birdbrain_docs.ddb")
ingest_docs(docs_path=docs_path, docs=docs, con=docs_con)

# bots
bot = Bot(docs_con=docs_con, data_cons=data_cons, system_con=bb_con, system=default)
