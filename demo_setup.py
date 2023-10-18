import os
import glob
import ibis

import logging as log

from ibis.backends.base import BaseBackend


def ingest_docs(docs_path: str, con: BaseBackend) -> None:
    for doc_dir in os.listdir(docs_path):
        if doc_dir in con.list_tables():
            log.warning(f"Table {doc_dir} already exists, skipping ingestion...")
            continue

        log.info(f"Processing {doc_dir}...")
        files = sorted(_find_docs(os.path.join(docs_path, doc_dir)))
        contents = [_read_doc(file) for file in files]
        data = {
            "filename": files,
            "content": contents,
        }

        t = ibis.memtable(data)
        t = t.mutate(token_estimate=t.content.length() // 4)

        log.info(f"Creating {doc_dir} table...")
        con.create_table(doc_dir, t)

    for table in con.list_tables():
        if table.startswith("_ibis"):
            log.info(f"Dropping {table}")
            con.drop_view(table)


# _functions
def _find_docs(path, extensions=None) -> list[str]:
    if extensions is None:
        extensions = ["md", "qmd", "txt", "py", "rst"]

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


if __name__ == "__main__":
    import toml
    from dotenv import load_dotenv

    load_dotenv()

    config = toml.load("config.toml")

    docs_con = ibis.connect(f"{config['docs']['backend_uri']}", read_only=False)
    ingest_docs("data/docs", docs_con)
