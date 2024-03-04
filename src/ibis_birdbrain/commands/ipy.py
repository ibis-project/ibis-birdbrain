def ipy_run(interactive=False):
    # imports
    import ibis
    import IPython

    from ibis_birdbrain import Bot

    # config
    ibis.options.interactive = True
    ibis.options.repr.interactive.max_rows = 20
    ibis.options.repr.interactive.max_columns = None

    # start IPython
    IPython.embed(colors="neutral")
