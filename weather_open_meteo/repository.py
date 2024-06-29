from dagster import repository, ScheduleDefinition
from weather_open_meteo.jobs.jobs import raw_data_job
from weather_open_meteo.schedules import raw_data_update_schedule

@repository
def weather_repository():
    return [raw_data_job, raw_data_update_schedule]