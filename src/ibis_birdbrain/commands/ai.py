def ai_run(state={}, interactive=False):
    from ibis_birdbrain import Console
    from ibis_birdbrain.ai import bot

    console = Console()
    console.print(f"birdbrain: ", style="bold violet blink")
    console.print(f"access to: {bot.name}")
    console.print(f"state: {state}")

    if interactive:
        import ibis
        import IPython

        from rich import print

        from ibis_birdbrain.tools.ibis import con, tables

        ibis.options.interactive = True

        IPython.embed(colors="neutral")
