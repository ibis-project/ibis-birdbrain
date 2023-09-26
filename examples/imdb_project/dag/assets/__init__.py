# imports
from dagster import load_assets_from_modules

from dag.assets import bronze, silver, gold
from dag.constants import BRONZE, SILVER, GOLD

# load assets
bronze_assets = load_assets_from_modules([bronze], group_name=BRONZE)
silver_assets = load_assets_from_modules([silver], group_name=SILVER)
gold_assets = load_assets_from_modules([gold], group_name=GOLD)

assets = [*bronze_assets, *silver_assets, *gold_assets]
