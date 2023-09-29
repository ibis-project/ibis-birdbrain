# imports
from marvin import ai_fn


# functions
@ai_fn
def choose_table_name(text: str, options: list[str]) -> str:
    """Given text, returns the table name to query."""
    text, options = text, options
    return ""


@ai_fn
def gen_sql_query(
    table_name: str, table_schema: str, question: str = "how many rows are there?"
) -> str:
    """Given a question about a table in a database, returns the SQL query
    string. MUST ONLY use SELECT and a single table of the input tablename."""
    table_name, table_schema, question = table_name, table_schema, question
    return ""


@ai_fn
def fix_sql_query(table_name: str, table_schema: str, query: str, error: str) -> str:
    """Given a SQL query and an error, returns the fixed SQL query."""
    table_name, table_schema, query, error = table_name, table_schema, query, error
    return ""


@ai_fn
def gen_python_code(description: str) -> str:
    """Generates a Python code for the input description. Keep it simple,
    type-annotated, and using minimal external dependencies. It may be fine to
    install a few dependencies.

    If a function is generated, ensure the function is called.
    """
    description = description
    return ""


@ai_fn
def fix_python_code(code: str, error: str) -> str:
    """Given a Python code and an error, returns the fixed Python
    function."""
    code, error = code, error
    return ""
