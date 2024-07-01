from dagster import multi_asset, AssetOut, asset, AssetKey
from weather_open_meteo.assets.others import load_data_from_api, insert_data_in_sqlite
from weather_open_meteo.assets import constants 
import yaml


@asset(
    name="geodata_about_capitals",
    description="Geodata about capital's in Europe"
)
def city_data():
    with open(constants.CITY_CONFIG, "r") as file:
        data = yaml.safe_load(file)
    return data['PARAMS_EU_CAPITALS']
    
    

@multi_asset(
    outs={
        "weather_archive": AssetOut(),
        "weather_forecast": AssetOut(),
        "air_conditions": AssetOut()
    },
    can_subset=True
)
def raw_data( geodata_about_capitals):
    weather_archive =[]
    weather_forecast = []
    air_conditions = []
    
    for city_data in geodata_about_capitals:
        
        weather_archive_data, city_data = load_data_from_api(
            url_path=constants.OPEN_METEO_URL_ARCHIVE,
            city_data=city_data,
            type_op=constants.TYPES[1],
            period=constants.PERIOD_ARCHIVE,
            config_path=constants.WEATHER_CONFIG
        )
        
        weather_archive.append(
                insert_data_in_sqlite(
                city_data=city_data,
                weather_data=weather_archive_data,
                table_name=constants.TABLE_NAME,
                data_schema_path=constants.WEATHER_DATA_SCHEMA,
                type=constants.TYPES[1],
                config_path=constants.WEATHER_CONFIG
            )
        )
        
        weather_forecast_data, city_data = load_data_from_api(
            url_path=constants.OPEN_METEO_URL_FORECAST,
            city_data=city_data,
            type_op=constants.TYPES[0],
            period=constants.PERIOD_ARCHIVE,
            config_path=constants.WEATHER_CONFIG
        )
        
        weather_forecast.append(
            insert_data_in_sqlite(
                city_data=city_data,
                weather_data=weather_forecast_data,
                table_name=constants.TABLE_NAME,
                data_schema_path=constants.WEATHER_DATA_SCHEMA,
                type_op=constants.TYPES[0],
                config_path=constants.WEATHER_CONFIG
            )
        )
        
        air_conditions_data, city_data = load_data_from_api(
            url_path=constants.OPEN_METEO_AIR_QUALITY,
            city_data=city_data,
            type_op=constants.TYPES[3],
            period=constants.PERIOD_AIR,
            config_path=constants.AIR_DATA_SCHEMA
        )
        
        air_conditions.append(
                insert_data_in_sqlite(
                city_data=city_data,
                weather_data=air_conditions_data,
                table_name=constants.TABLE_NAME,
                data_schema_path=constants.AIR_DATA_SCHEMA,
                type=constants.TYPES[3],
                config_path=constants.AIR_DATA_SCHEMA
            )
        )
        
    return weather_archive, weather_forecast, air_conditions