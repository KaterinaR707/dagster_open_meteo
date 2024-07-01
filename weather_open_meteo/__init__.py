from dagster import Definitions
from weather_open_meteo.resources.resources import connection_resource
from weather_open_meteo.assets.weather_data import city_data, raw_data
from weather_open_meteo.assets import others



all_assets = [raw_data, city_data]

defs = Definitions(
    assets=all_assets,
    resources={
        "connection": connection_resource
    }
)
