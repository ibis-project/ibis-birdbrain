# imports
import os
import toml
import typer
import marvin

from typing_extensions import Annotated

from ibis_birdbrain.commands.ipy import ipy_run
from ibis_birdbrain.commands.testing import testing_run

# typer config
app = typer.Typer(no_args_is_help=True)


# global options
def version(value: bool):
    if value:
        version = toml.load("pyproject.toml")["project"]["version"]
        typer.echo(f"{version}")
        raise typer.Exit()


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
def cli(
    version: bool = typer.Option(
        None, "--version", help="Show version.", callback=version, is_eager=True
    ),
):
    version = version
    # Do other global stuff, handle other global options here
    return


## main
if __name__ == "__main__":
    typer.run(cli)
