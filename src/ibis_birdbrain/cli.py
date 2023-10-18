"""
Ibis Birdbrain CLI.
"""

# imports
import typer

from typing_extensions import Annotated

from ibis_birdbrain.commands.ipy import ipy_run
from ibis_birdbrain.commands.testing import testing_run

# typer config
app = typer.Typer(no_args_is_help=True)


# subcommands
@app.command()
def test():
    """
    test
    """
    testing_run()


@app.command()
def ipy():
    """
    ipy
    """
    ipy_run()


# main
@app.callback()
def cli():
    return


## main
if __name__ == "__main__":
    typer.run(cli)
