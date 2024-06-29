from dagster import Definitions, load_asset_checks_from_modules
from weather_open_meteo.resources.resources import ConnectionOpenMeteo
from weather_open_meteo.assets import weather_data
from weather_open_meteo.assets import others
from weather_open_meteo.jobs.jobs import raw_data_job
from weather_open_meteo.schedules import raw_data_update_schedule


all_assets = load_asset_checks_from_modules([weather_data, others])
all_jobs = [raw_data_job]

defs = Definitions(
    assets=all_assets,
    resources={
        "connection_open_meteo": ConnectionOpenMeteo()
    },
    jobs=all_jobs,
    schedules=raw_data_update_schedule
)
