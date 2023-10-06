# imports
import os
import ibis

import ibis.expr.datatypes as dt

from ibis.expr.schema import Schema
from ibis.expr.types.relations import Table

from ibis_birdbrain.tools import tool
from ibis_birdbrain.functions.code import (
    choose_table_names,
    gen_sql_query,
    fix_sql_query,
)

from ibis_birdbrain.utils import read_config

config = read_config(config_section="eda")


# configure Ibis
ibis.options.interactive = True
ibis.options.repr.interactive.max_rows = 20
ibis.options.repr.interactive.max_columns = 20
ibis.options.repr.interactive.max_length = 20
ibis.options.repr.interactive.max_string = 100
ibis.options.repr.interactive.max_depth = 3


# setup Ibis
if "backend_uri" in config:
    con = ibis.connect(config["backend_uri"])
else:
    con = ibis.connect("duckdb://")


# tools
@tool
def generate_tpch_data(sf: float = 1.0) -> None:
    """Generates TPCH data at scale factor sf (default 1.0)"""
    con.raw_sql(f"call dbgen(sf={sf});")


@tool
def clear_tables() -> None:
    """Clears all tables from the database"""
    for table in list_tables():
        con.drop_table(table, force=True)


@tool
def get_table_schemas(table_names: list[str]) -> list[Schema]:
    """Returns the schemas of a list of tables (all tables if empty list)"""
    if table_names == []:
        return get_table_schemas(table_names=list_tables())
    return [con.table(table_name).schema() for table_name in table_names]


@tool
def list_tables() -> list[str]:
    """Returns a list of available tables to query"""
    return sorted(list(set(con.list_tables())))


@tool
def write_tables_to_parquet(table_names: list[str]) -> None:
    """Writes tables to parquet files"""
    os.makedirs("data", exist_ok=True)
    if table_names == []:
        table_names = list_tables()
    for table_name in table_names:
        con.table(table_name).to_parquet(f"data/{table_name}.parquet")


@tool
def generate_sql(text: str) -> str:
    """Generates SQL SELECT statement as a string for the tables in the database to answer the text"""
    table_names = choose_table_names(text, options=list_tables())
    table_schemas = get_table_schemas(table_names)
    sql = gen_sql_query(table_names, table_schemas, text).strip(";")
    return sql, table_names


@tool
def execute_sql(
    text: str | None = None,
    sql: str | None = None,
    table_names: list[str] = list_tables(),
) -> (str, Table):
    """Executes (and optionally generates if no sql input) SQL SELECT statement for the tables in the database to answer the text"""
    if sql is None:
        sql, table_names = generate_sql(text)
    try:
        res = con.table(table_names[0]).sql(sql)
    except Exception as e:
        sql = fix_sql_query(sql, str(e)).strip(";")
        try:
            res = con.table(table_names[0]).sql(res)
        except Exception as e:
            raise ValueError(f"Could not execute SQL: {res} with error: {e}")
    return sql, res
