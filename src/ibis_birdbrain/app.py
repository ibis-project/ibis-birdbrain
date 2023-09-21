# imports
import os
import toml
import typer
import marvin

from dotenv import load_dotenv
from typing_extensions import Annotated

from ibis_birdbrain.commands.ai import ai_run
from ibis_birdbrain.commands.testing import testing_run

# load .env file
load_dotenv(os.path.expanduser("~/.birdbrain/.env"))
marvin.settings.llm_model = "azure_openai/gpt-4-32k"

# load config
try:
    config = toml.load(os.path.expanduser("~/.birdbrain/config.toml"))
except FileNotFoundError:
    config = {}

# typer config
app = typer.Typer(no_args_is_help=True)

# global state
state = {"config": config}


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
def ai(
    interactive: Annotated[
        bool, typer.Option("--interactive", "-i", help="run ai in interactivce mode")
    ] = False,
    learn_spanish: Annotated[
        bool, typer.Option("--learn-spanish", "-l", help="run in learn Spanish mode")
    ] = False,
):
    """
    ai
    """
    ai_run(state=state, interactive=interactive, learn_spanish=learn_spanish)


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
