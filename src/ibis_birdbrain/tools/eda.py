# imports
import ibis

import polars as pl

import ibis.expr.datatypes as dt

from ibis.expr.schema import Schema
from ibis.expr.types.relations import Table

from ibis_birdbrain.tools import tool
from ibis_birdbrain.functions.code import (
    choose_table_name,
    gen_sql_query,
    fix_sql_query,
)

from ibis_birdbrain.utils import read_config

config = read_config(config_section="eda")

# setup Ibis
if "backend_uri" in config:
    con = ibis.connect(config["backend_uri"])
else:
    con = ibis.connect("duckdb://")


# tools
@tool
def get_table_schema(table_name: str) -> Schema:
    """Returns the schema of a table"""
    if table_name not in list_tables():
        raise ValueError(f"Table {table_name} not found in {list_tables()}")
    return con.table(table_name).schema()


@tool
def list_tables() -> list[str]:
    """Returns a list of available tables to query"""
    return sorted(list(set(con.list_tables())))


@tool
def read_delta_table(filepath: str) -> Table:
    """Reads a Delta Lake table directory from the full filepath

    filepath should be of the form: <path>/<table_name>
    """
    t = con.read_delta(filepath)
    view_name = t.get_name()
    # extract the table name from the filepath
    table_name = filepath.split("/")[-1]
    t = con.create_table(table_name, t, overwrite=True)
    con.drop_view(view_name)
    return t


@tool
def read_excel_file(filepath: str, sheet_name: str = "Sheet1") -> Table:
    """Reads an Excel file from the full filepath

    filepath should be of the form: <path>/<table_name>.<extension>
    """
    df = pl.read_excel(filepath, sheet_name=sheet_name)
    t = ibis.memtable(df.to_arrow())
    view_name = t.get_name()
    # extract the table name from the filepath
    file_name = filepath.split("/")[-1]
    table_name = file_name.split(".")[0]
    t = con.create_table(table_name, t, overwrite=True)
    con.drop_view(view_name)
    return t


@tool
def query_table(question: str) -> Table:
    """Queries the table in the database to answer the question"""
    table_name = choose_table_name(question, options=list_tables())
    table_schema = get_table_schema(table_name)
    if table_name not in list_tables():
        raise ValueError(f"Table {table_name} not found in {list_tables}")
    sql = gen_sql_query(table_name, table_schema, question).strip(";")
    try:
        res = con.table(table_name).sql(sql)
    except Exception as e:
        sql = fix_sql_query(table_name, table_schema, sql, str(e)).strip(";")
        try:
            res = con.table(table_name).sql(res)
        except Exception as e:
            raise ValueError(f"Could not execute SQL: {res} with error: {e}")

    return str(res)
