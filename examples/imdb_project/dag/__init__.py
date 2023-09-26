# imports
from dagster import Definitions

from dag.jobs import jobs
from dag.assets import assets
from dag.resources import resources

# config
defs = Definitions(
    assets=assets,
    resources=resources,
    jobs=jobs,
)
