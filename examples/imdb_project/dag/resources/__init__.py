# imports
from dag.resources import table_io_managers

# load resources
resources = {"io_manager": table_io_managers.DeltaIOManager()}
# resources = {"io_manager": table_io_managers.DuckDBIOManager()}
