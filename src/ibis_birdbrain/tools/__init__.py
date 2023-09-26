# imports
from marvin.tools import tool

from ibis_birdbrain.tools.internet import (
    open_browser,
    search_internet,
    webpage_to_str,
)
from ibis_birdbrain.tools.text import summarize_text, translate_text
from ibis_birdbrain.tools.code import text_to_python, fix_python_error, run_python_code
from ibis_birdbrain.tools.filesystem import read_file, list_files_and_dirs, write_file
from ibis_birdbrain.tools.ibis import (
    list_tables,
    query_table,
    get_table_schema,
    read_delta_table,
    read_excel_file
)
from ibis_birdbrain.tools.advanced import (
    read_files_and_summarize,
    read_webpage_and_summarize,
)
from ibis_birdbrain.tools.github import use_github_cli


# tools
tools = [
    # internet
    open_browser,
    search_internet,
    webpage_to_str,
    # text
    summarize_text,
    translate_text,
    # filesystem
    read_file,
    list_files_and_dirs,
    write_file,
    # code
    text_to_python,
    fix_python_error,
    run_python_code,
    # Ibis
    list_tables,
    query_table,
    get_table_schema,
    read_delta_table,
    read_excel_file,
    # advanced
    read_files_and_summarize,
    read_webpage_and_summarize,
    # github
    # use_github_cli,
]

__all__ = ["tool", "tools"]
