from dagster import ScheduleDefinition
from weather_open_meteo.jobs.jobs import raw_data_job

raw_data_update_schedule = ScheduleDefinition(
    job=raw_data_job,
    cron_schedule="0 0 * * *",
)

