from dagster import ConfigurableResource, resource
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from weather_open_meteo.assets import constants 
import yaml

class ConnectionOpenMeteo(ConfigurableResource):

    def request(
        self, 
        url_path, 
        params_city: dict, 
        config_path: str, 
        period:str, 
        type_op: str
    ) -> dict:
        
        params = params_city["params"]
        params["start_date"] = constants.START_DATE
        params["end_date"] = constants.END_DATE
        
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
            
        if type_op in ["forecast", "archive"]:
            config = data['required_variables_forecast_archive']
            if type_op == "forecast": params["forecast_days"] = 1
            
        else:
            config = data ["required_variables_air_conditions"]
        
        params[period] = config
        
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)
        responses = openmeteo.weather_api(url_path, params=params)
        response = responses[0]
        
        if type in ["forecast", "archive"]:
            daily = response.Daily()
        else:
            daily = response.Current()
       
        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
            ).strftime('%Y-%m-%d').tolist(),
            "latitude": params["latitude"],
            "longitude": params["longitude"],
            "timezone": params["timezone"],
            "city": params_city["city"]
        }
            
            
        for i, var_name in enumerate(config):
            daily_data[var_name] = daily.Variables(i).ValuesAsNumpy().tolist()

        return daily_data
    