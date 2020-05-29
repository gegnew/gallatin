import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries
import os
import pandas as pd
import numpy as np
from datetime import datetime
import pytz
import dateutil
from timezonefinder import TimezoneFinder
import requests
from bs4 import BeautifulSoup

from utils import (
    get_routes_for_lat_long,
    get_route,
    get_routes,
    get_html,
    get_mp_ticks_for_route,
    get_station_metadata_for_area,
    date_range,
    get_weather_data_chunks
)

from queries import *


# Artificially limit this to one location:
LAT = 45.42
LON = -111.23

# Timezones
TIMEZONE = TimezoneFinder().timezone_at(lat=canyon_coords[0], lng=canyon_coords[1])
tz = pytz.timezone(TIMEZONE)
datetime.today().replace(tzinfo=tz)
TODAY = datetime.today().replace(tzinfo=tz)

# Mountain Project API
mp_base_url = "https://www.mountainproject.com"
MP_KEY = os.environ["MP_PRIVATE_KEY"]

# Synoptic weather station API
weather_base = "https://api.mesowest.net/v2/stations"
SYNOPTIC_TOKEN = "fec44906eebc49e5947a38b784e8907d"

# Get climbing routes for area
routes = get_routes_for_lat_long(LAT, LON, max_distance=50, max_results=500)
name_id_tuples = [(route["namegallatin_"], route["id"]) for route in routes["routes"]]


# Scrape MountainProject for climb ticks
parsed = []
for name, _id in name_id_tuples:
    parsed.append(get_mp_ticks_for_route(name, _id))
    
ticks_df = pd.DataFrame(parsed)

EARLIEST_DATE = dateutil.parser.parse(ticks_table.date.min())


# Get weather stations
metadata = get_station_metadata_for_area(SYNOPTIC_TOKEN, LAT, LON)
df_station_metadata = pd.DataFrame(metadata["STATION"])
station_df = df_station_metadata[df_station_metadata["STATUS"]=="ACTIVE"].drop(columns="STATUS")
station_df.columns = [col.lower() for col in station_df.columns]

station_df = station_df[["id", "stid", "elevation", "distance", "longitude", "latitude", "state", "timezone"]]


# Get weather data
weather_data = get_weather_data_chunks(EARLIEST_DATE, TODAY, LAT, LON)
weather_df = pd.DataFrame(weather_data)


# Save data

# TODO: load data to S3, saving with boto3
