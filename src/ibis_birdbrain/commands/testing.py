def testing_run():
    from rich.console import Console

    console = Console()
    console.print(f"testing: ", style="bold violet", end="")
    console.print(f"done...")
