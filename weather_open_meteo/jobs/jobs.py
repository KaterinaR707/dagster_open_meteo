from dagster import AssetSelection, define_asset_job
from ..partitions.partitions import daily_partitions


raw_data_daily = AssetSelection.assets('raw_data')

raw_data_job = define_asset_job(
    name="raw_data_daily_update",
    selection=raw_data_daily,
    partitions_def=daily_partitions
)

