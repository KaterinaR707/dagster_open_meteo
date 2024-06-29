from dagster import asset, graph_asset, op, Out, OpExecutionContext
from ..resources.resources import ConnectionOpenMeteo
from typing import Tuple
import constants
import sqlite3
import yaml


@op(out={"weather_data": Out(), "city_data": Out()},)
def load_data_from_api(
    url: str,
    city_data:dict, 
    connection: ConnectionOpenMeteo,
    type: str,
    period: str,
    config_path:str
) -> Tuple[dict, dict]:
    
    weather_data = connection.request(
        url=url,
        params_city=city_data,
        config_path=config_path,
        period=period,
        type=type
    )
    
    return (weather_data, city_data)
    
@op
def insert_data_in_sqlite(
    context: OpExecutionContext,
    city_data,
    weather_data,
    table_name: str,
    data_schema_path: str,
    type: str,
    config_path: str
):
    table_name = f"{table_name}_{type}"
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()

    with open(f"{data_schema_path}", "r") as sql_file:
        sql_script = sql_file.read()
    
    sql_script = sql_script.replace("weather_replace", f"{table_name}")
    
    cursor.executescript(sql_script)
    
    with open(config_path, 'r') as f:
        data = yaml.safe_load(f)
        
    if type in ["forecast", "archive"]:
        columns = constants.PARAMS_KEYS + data['required_variables_forecast_archive']
    
    else:
        columns = constants.PARAMS_KEYS + data['required_variables_air_conditions']
        
    values = list()
    for column in columns:
        if columns.index(column) == 0:
            values.append(city_data[column])
        elif columns.index(column) < 5:
            values.append(city_data["params"][column])
        else:
            values.append(weather_data[column])
    
    table_columns = ", ".join(columns)
    placeholders = ", ".join(["?"] * len(columns))
    
    try:
        cursor.execute(
            f"INSERT INTO {table_name} ({table_columns}) VALUES ({placeholders});",
            tuple(values)
        )
        conn.commit()
        
        context.log.info(f"Succesfully insert data for {weather_data["date"]} in {table_name}")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        
    finally:
        conn.close()
        