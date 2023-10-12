# imports
import logging as log

from typing import Any

from ibis.expr.schema import Schema
from ibis.expr.types.relations import Table


# classes
class DataConnection:
    """
    Ibis data platform connection.
    """

    con: Any = None
    name: str = ""
    description: str = ""
    tables: dict[str, Schema] = {}

    def __init__(
        self,
        con: Any,
        name: str,
        description: str,
    ) -> None:
        """
        Initialize a data connection.
        """
        # set stuff
        self.con = con
        self.name = name
        self.description = description

        # compute stuff
        self.tables = self.get_tables()

    def __repr__(self) -> str:
        """
        String representation.
        """
        return f"""
\tname: {self.name}
\tdescription: {self.description}
\tcon: {self.con}
\tcon_type: {self.con.name}
\ttables: {list(self.tables.keys())}
"""

    def list_tables(self) -> list[str]:
        """
        List tables.
        """
        return self.con.list_tables()

    def table(self, name: str) -> Table:
        """
        Get a table.
        """
        return self.con.table(name)

    def insert(self, name: str, t: Table) -> None:
        """
        Insert a table.
        """
        self.con.insert(name, t)

    def create_table(self, name: str, t: Table) -> None:
        """
        Create a table.
        """
        self.con.create_table(name, t)

    def get_tables(self) -> dict[str, Schema]:
        """
        Get tables.
        """
        tables = {}
        for table in self.list_tables():
            tables[table] = self.con.table(table).schema()
        return tables

    def query(self, text) -> Table:
        """
        Query the data into a table.
        """
        t = self.con.table(text)
        return t
