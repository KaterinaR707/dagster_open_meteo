from dagster import graph_multi_asset, AssetOut
from .op import load_data_from_api, insert_data_in_sqlite
import constants
import yaml

@graph_multi_asset(
    outs={
        "weather_archive": AssetOut(),
        "weather_forecast": AssetOut(),
        "air_conditions": AssetOut()
    },
    can_subset=True
)
def raw_data():
    
    with open(constants.CITY_CONFIG, "r") as file:
        data = yaml.safe_load(file)
    PARAMS_EU_CAPITALS = data['PARAMS_EU_CAPITALS']
    
    for city_data in PARAMS_EU_CAPITALS:
        
        weather_archive = insert_data_in_sqlite(
            load_data_from_api(
                url = constants.OPEN_METEO_URL_ARCHIVE,
                city_data=city_data,
                config_path=constants.WEATHER_CONFIG,
                type=constants.TYPES[1],
                period=constants.PERIOD_ARCHIVE
            ),
            table_name =constants.TABLE_NAME,
            data_schema_path=constants.WEATHER_DATA_SCHEMA,
            type=constants.TYPES[1],
            config_path=constants.WEATHER_CONFIG
        )
        
        weather_forecast = insert_data_in_sqlite(
            load_data_from_api(
                url = constants.OPEN_METEO_URL_FORECAST,
                city_data=city_data,
                config_path=constants.WEATHER_CONFIG,
                type=constants.TYPES[0],
                period=constants.PERIOD_ARCHIVE
            ),
            table_name =constants.TABLE_NAME,
            data_schema_path=constants.WEATHER_DATA_SCHEMA,
            type=constants.TYPES[0],
            config_path=constants.WEATHER_CONFIG
        )
        
        air_conditions = insert_data_in_sqlite(
            load_data_from_api(
                url = constants.OPEN_METEO_AIR_QUALITY,
                city_data=city_data,
                config_path=constants.WEATHER_CONFIG,
                type=constants.TYPES[3],
                period=constants.PERIOD_AIR
            ),
            table_name =constants.TABLE_NAME,
            data_schema_path=constants.AIR_DATA_SCHEMA,
            type=constants.TYPES[3],
            config_path=constants.AIR_DATA_SCHEMA
        )
    