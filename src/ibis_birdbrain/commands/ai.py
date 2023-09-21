def ai_run(state={}, interactive=False, learn_spanish=False):
    from ibis_birdbrain import Console
    from ibis_birdbrain.ai import bot
    from ibis_birdbrain.systems import LearnSpanishSystem

    if learn_spanish:
        bot.ai.additional_prompts.append(LearnSpanishSystem())

    console = Console()
    console.print(f"ibis_birdbrain: ", style="bold violet blink")
    console.print(f"access to: {bot.name}")
    console.print(f"state: {state}")

    if interactive:
        import ibis
        import IPython

        from rich import print

        from ibis_birdbrain.tools.birdbrain import con, tables

        ibis.options.interactive = True

        IPython.embed(colors="neutral")
