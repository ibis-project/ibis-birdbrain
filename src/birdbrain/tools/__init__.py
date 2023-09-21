# imports
from marvin.tools import tool

from birdbrain.tools.internet import (
    open_browser,
    search_internet,
    webpage_to_str,
)
from birdbrain.tools.text import summarize_text, translate_text
from birdbrain.tools.code import text_to_python, fix_python_error, run_python_code
from birdbrain.tools.filesystem import read_file, list_files_and_dirs, write_file
from birdbrain.tools.birdbrain import list_tables, query_table, get_table_schema
from birdbrain.tools.advanced import (
    read_files_and_summarize,
    read_webpage_and_summarize,
)
from birdbrain.tools.github import use_github_cli


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
    # data
    list_tables,
    query_table,
    get_table_schema,
    # advanced
    read_files_and_summarize,
    read_webpage_and_summarize,
    # github
    # use_github_cli,
]

__all__ = ["tool", "tools"]
