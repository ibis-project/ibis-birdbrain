"""
Ibis Birdbrain CLI.
"""

# imports
import typer

from typing_extensions import Annotated, Optional

from ibis_birdbrain.commands import ipy_run, ingest_docs_run, testing_run

# typer config
app = typer.Typer(no_args_is_help=True)


# subcommands
@app.command()
def ipy():
    """
    ipy
    """
    ipy_run()


@app.command()
def test():
    """
    test
    """
    testing_run()


@app.command()
def ingest_docs(clear: Annotated[bool, typer.Option()] = False):
    """
    ingest docs
    """
    ingest_docs_run(clear=clear)


# main
@app.callback()
def cli():
    return


## main
if __name__ == "__main__":
    typer.run(cli)
