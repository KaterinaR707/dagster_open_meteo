OPEN_METEO_URL_ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"
OPEN_METEO_URL_FORECAST = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_AIR_QUALITY = "https://air-quality-api.open-meteo.com/v1/air-quality"

WEATHER_CONFIG = "weather_open_meteo/resources/weather_config.yaml"
CITY_CONFIG = "weather_open_meteo/resources/config_city.yaml"

START_DATE = "2024-04-30"
END_DATE = "2024-04-30"

PERIOD_ARCHIVE = "daily"
PERIOD_AIR = "current"

TABLE_NAME = "weather"
 
TYPES = ["forecast", "archive", "air_condition"]

WEATHER_DATA_SCHEMA = "weather_open_meteo/data_schema/weather_data_schema.sql"
AIR_DATA_SCHEMA = "weather_open_meteo/data_schema/air_quality_data_schema.sql"

PARAMS_KEYS = ["city", "latitude", "longitude", "timezone", "date" ]

