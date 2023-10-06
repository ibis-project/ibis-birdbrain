# imports
import os
import fnmatch

from ibis_birdbrain.tools import tool
from ibis_birdbrain.tools.filesystem import (
    read_gitignore,
    is_ignored,
    list_files_and_dirs,
    read_file,
    write_file,
)

from ibis_birdbrain.functions.docs import choose_relevant_files

# tools
@tool
def get_relevant_docs(text: str) -> list[str]:
    """Returns a list of relevant files (docs)
    that the system has access to.

    Update the relevant docs in state if docs are found.
    """
    docs = list_files_and_dirs("data/docs")
    docs = choose_relevant_files(docs, text)
    return docs
