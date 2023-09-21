# imports
from typing import Callable

from ibis_birdbrain.tools import tool
from ibis_birdbrain.tools.internet import webpage_to_str
from ibis_birdbrain.tools.text import summarize_text, Summary
from ibis_birdbrain.tools.filesystem import read_file, write_file


# tools
@tool
def read_webpage_and_summarize(url: str = "https://ibis-project.org") -> Summary:
    """Read a webpage and summarize it."""
    return summarize_text(webpage_to_str(url))


@tool
def read_file_and_summarize(
    path: str,
    file_write: bool = True,
    filename: str = "notes.md",
    file_overwrite: bool = False,
) -> Summary:
    """Read a file and summarize it."""
    summary = summarize_text(read_file(path))
    if file_write:
        return write_file(filename, str(summary), overwrite=file_overwrite)

    return summary


@tool
def read_files_and_summarize(
    files: list[str],
    file_write: bool = True,
    filename: str = "notes.md",
    file_overwrite: bool = False,
) -> str:
    """Read a list of files and summarize them."""
    for file in files:
        summary = summarize_text(read_file(file))
        if summary is None:
            continue
        if file_write:
            write_file(filename, f"filename: {file}")
            write_file(filename, str(summary), overwrite=file_overwrite)

    return f"Files {files} summarized and written to {filename}."


@tool
def run_on_each_file(
    files: list[str],
    func: Callable,
) -> str:
    """Run a function on each file in a list of files."""
    return "\n".join([func(file) for file in files])
