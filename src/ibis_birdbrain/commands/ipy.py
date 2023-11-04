def ipy_run(interactive=False):
    # imports
    import IPython

    import ibis
    from ibis_birdbrain.app import bot

    # config
    ibis.options.interactive = True
    ibis.options.repr.interactive.max_rows = 20
    ibis.options.repr.interactive.max_columns = 20

    # start IPython
    IPython.embed(colors="neutral")
