from dagster import Definitions, load_asset_checks_from_modules
from .resources.resources import ConnectionOpenMeteo
from .assets import weather_data
from .jobs.jobs import raw_data_job
from .schedules import raw_data_update_schedule


all_assets = load_asset_checks_from_modules([weather_data])
all_jobs = [raw_data_job]

defs = Definitions(
    assets=all_assets,
    resources={
        "connection_open_meteo": ConnectionOpenMeteo()
    },
    jobs=all_jobs,
    schedules=raw_data_update_schedule
)
