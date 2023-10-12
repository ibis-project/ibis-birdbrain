def ipy_run():
    import time
    import ibis
    import marvin
    import IPython

    from rich import print

    from rich.console import Console

    from ibis_birdbrain import bot

    # configure Ibis
    ibis.options.interactive = True
    ibis.options.repr.interactive.max_rows = 20
    ibis.options.repr.interactive.max_columns = 20
    ibis.options.repr.interactive.max_length = 20
    ibis.options.repr.interactive.max_string = 100
    ibis.options.repr.interactive.max_depth = 3

    # start IPython
    IPython.embed(colors="neutral")
