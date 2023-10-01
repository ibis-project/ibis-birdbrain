def ai_run(interactive=False):
    import marvin

    from ibis_birdbrain.ai import Console
    from ibis_birdbrain.bots.birdbrain import bot

    # aliases
    ai = bot
    birdbrain = ai

    # output
    console = Console()
    console.print(f"access to: ", end="")
    console.print(f"{bot.name}", style="bold violet blink")
    console.print(f"model: {marvin.settings.llm_model}", style="bold blue")

    if interactive:
        import ibis
        import IPython

        from rich import print

        from ibis_birdbrain.tools.eda import con

        ibis.options.interactive = True

        IPython.embed(colors="neutral")
