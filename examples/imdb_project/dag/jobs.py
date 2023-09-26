from dagster import define_asset_job, AssetSelection

from dag.assets import BRONZE, SILVER, GOLD

all_job = define_asset_job("all_assets")
bronze_job = define_asset_job("bronze_assets", selection=AssetSelection.groups(BRONZE))
silver_job = define_asset_job("silver_assets", selection=AssetSelection.groups(SILVER))
gold_job = define_asset_job("gold_assets", selection=AssetSelection.groups(GOLD))
jobs = [all_job, bronze_job, silver_job, gold_job]
