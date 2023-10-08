# imports
import os
import ibis
import glob

from typing import Any

import logging as log


# functions
def _find_docs(path, extensions=None) -> list[str]:
    if extensions is None:
        extensions = ["md", "qmd", "txt", "py"]

    files = []
    for ext in extensions:
        files.extend(glob.glob(f"{path}/**/*.{ext}", recursive=True))

    return files


def _read_doc(doc: str) -> str:
    try:
        with open(doc, "r") as f:
            return f.read()
    except:
        return "Error reading file"


def ingest_docs(docs_path: str, docs: list[str], con: Any) -> None:
    for doc_dir in docs:
        log.info(f"Processing {doc_dir}")
        files = _find_docs(os.path.join(docs_path, doc_dir))
        for file in files:
            log.info(f"Processing {file}")
            content = _read_doc(file)
            data = {
                "filename": [file],
                "content": [content],
                "token_estimate": [len(content) // 4],
            }
            if doc_dir not in con.list_tables():
                log.info(f"Creating {doc_dir}")
                con.create_table(doc_dir, ibis.memtable(data))
            elif file not in con.table(doc_dir).filename.to_pandas().to_list():
                log.info(f"Adding {file} to {doc_dir}")
                con.insert(doc_dir, ibis.memtable(data))

    for table in con.list_tables():
        if table.startswith("_ibis"):
            log.info(f"Dropping {table}")
            con.drop_view(table)
