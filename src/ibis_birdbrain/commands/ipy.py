def ipy_run(interactive=False):
    # imports
    import ibis
    import IPython

    # config
    ibis.options.interactive = True
    ibis.options.repr.interactive.max_rows = 20
    ibis.options.repr.interactive.max_columns = 20

    # start IPython
    IPython.embed(colors="neutral")
