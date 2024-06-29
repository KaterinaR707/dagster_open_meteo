from dagster import DailyPartitionsDefinition
from weather_open_meteo.assets import constants

start_date = constants.START_DATE
end_date = constants.END_DATE

daily_partitions = DailyPartitionsDefinition(
    start_date=start_date,
    end_date=end_date
)
