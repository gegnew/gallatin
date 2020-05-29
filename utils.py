from requests import RequestException
import os
import pandas as pd
import numpy as np
from datetime import datetime
import pytz
import dateutil
from timezonefinder import TimezoneFinder
import requests
from bs4 import BeautifulSoup

# MountainProject funcs

def get_routes_for_lat_long(key, lat, long, max_distance=None, max_results=None, min_diff=None, max_diff=None):
    params = {
        "lat": lat,
        "lon": long,
        "maxDistance": max_distance,
        "maxResults": max_results,
        "minDiff": min_diff,
        "maxDiff": max_diff,
        "key": key
    }
    params = {k: params[k] for k in params if params[k] is not None}
    res = requests.get(f"{mp_base_url}/data/get-routes-for-lat-lon", params=params)
    res.raise_for_status()
    return res.json()
    
    
def get_route(route_id):
    res = requests.get(f"{mp_base_url}/data/get-routes/", params={"routeIds": route_id, "key": KEY})
    res.raise_for_status()
    return res.json()
    
def get_routes(route_ids):
    res = requests.get(f"{mp_base_url}/data/get-routes/", params={"routeIds": route_ids, "key": KEY})
    res.raise_for_status()
    return res.json()



# Scraping funcs
def get_html(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        resp = requests.get(url, stream=True)
        if is_good_response(resp):
            return resp.content
        else:
            return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
    
def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """Print this because I don't want to deal with logging"""
    print(e)


def get_mp_ticks_for_route(name, _id):
    try:
        url = f"{mp_base_url}/route/stats/{_id}"
        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        ticks = tables[3]
        data = ticks.find_all("tr")[0].find_all("td")
        date_string = " ".join(data[1].string.split(" ")[:3])
        date = datetime.strptime(date_string, "%b %d, %Y").replace(tzinfo=tz).isoformat()
        user_name = data[0].find("a").string
        user_id = data[0].find("a")["href"].split("/")[-2]
        return {"route_id": _id, "name": name, "date": date, "user_name": user_name, "user_id": user_id}
    except IndexError as e:
        print(f"Couldn't get that thing you wanted, skipping: {tables} \n Original error: {e}")
        

# Synoptic API funcs
def get_station_metadata_for_area(token, lat, lon):
    params = {
        "radius": ",".join([str(LAT), str(LON), str(50)]),
        "token": token
    }
    res = requests.get(f"{weather_base}/metadata", params=params)
    res.raise_for_status()
    return res.json()

def date_range(start, end, intv):
    diff = (end - start ) / intv
    for i in range(intv):
        yield (start + diff * i)
    yield end
        
def get_weather_data_chunks(start_datetime, end_datetime, lat, long):
    data = []
    for dt in date_range(start_datetime, end_datetime, 10):
        params = {
            "radius": ",".join([str(canyon_coords[0]), str(canyon_coords[1]), str(3)]),
            "start": start_datetime,
            "end": dt,
            "token": TOKEN
        }
        res = requests.get(f"{weather_base}/timeseries", params=params)
        res.raise_for_status()
        start_datetime = dt
        data.append(res.json())