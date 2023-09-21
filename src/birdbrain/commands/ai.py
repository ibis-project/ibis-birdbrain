def ai_run(state={}, interactive=False, learn_spanish=False):
    from birdbrain import Console
    from birdbrain.ai import bot
    from birdbrain.systems import LearnSpanishSystem

    if learn_spanish:
        bot.ai.additional_prompts.append(LearnSpanishSystem())

    console = Console()
    console.print(f"birdbrain: ", style="bold violet blink")
    console.print(f"access to: {bot.name}")
    console.print(f"state: {state}")

    if interactive:
        import ibis
        import IPython

        from rich import print

        from birdbrain.tools.birdbrain import con, tables

        ibis.options.interactive = True

        IPython.embed(colors="neutral")
