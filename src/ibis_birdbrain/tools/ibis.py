# imports
import ibis

from ibis_birdbrain.tools import tool
from ibis_birdbrain.functions import choose_table_name, gen_sql_query, fix_sql_query

# setup Ibis
con = ibis.connect("duckdb://imdb.ddb")
tables = sorted(list(set(con.list_tables())))


# tools
@tool
def get_table_schema(table_name: str) -> str:
    """Returns the schema of a table"""
    if table_name not in tables:
        raise ValueError(f"Table {table_name} not found in {tables}")
    return str(con.table(table_name).schema())


@tool
def list_tables() -> list[str]:
    """Returns a list of available tables to query"""
    return sorted(list(set(con.list_tables())))


@tool
def query_table(question: str) -> str:
    """Queries the table in the database to answer the question"""
    table_name = choose_table_name(question, options=tables)
    table_schema = get_table_schema(table_name)
    if table_name not in tables:
        raise ValueError(f"Table {table_name} not found in {tables}")
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
