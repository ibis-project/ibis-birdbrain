def ipy_run(interactive=False, tpch=False):
    import ibis
    import marvin
    import IPython

    from rich import print

    from ibis_birdbrain.ai import Console

    if tpch:
        from ibis_birdbrain.bots.tpch3000 import bot
        from ibis_birdbrain.tools.tpch3000 import con
    else:
        from ibis_birdbrain.bots.birdbrain import bot
        from ibis_birdbrain.tools.eda import con

    # aliases
    ai = bot
    birdbrain = ai

    # output
    console = Console()
    console.print(f"access to: ", end="")
    console.print(f"{bot.name}", style="bold violet blink")
    console.print(f"model: {marvin.settings.llm_model}", style="bold blue")

    # configure Ibis
    ibis.options.interactive = True
    ibis.options.repr.interactive.max_rows = 20
    ibis.options.repr.interactive.max_columns = 20
    ibis.options.repr.interactive.max_length = 20
    ibis.options.repr.interactive.max_string = 100
    ibis.options.repr.interactive.max_depth = 3

    # configure Ibis Birdbrain
    bot.interactive = True

    # start IPython
    IPython.embed(colors="neutral")
