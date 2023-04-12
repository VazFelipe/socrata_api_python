import requests
import json
import os
from datetime import date, datetime, timedelta, time
import time
from google.cloud import storage

with open('config.json', 'r') as f:
    config = json.load(f)

start_date = date(2018, 1, 1) 
end_date = date.today()
day_range = int((end_date - start_date).days)+1
number_of_days = 3

def extract_list_of_dates(start_date, number_of_days):
    list_of_dates=[]
    for day in range(day_range):
        if day <= day_range:
            if day <= number_of_days-1:
                list_of_dates.append((datetime(year=start_date.year,month=start_date.month,day=start_date.day) + timedelta(day, hours=23,minutes=59,seconds=59,microseconds=999999)).isoformat())
    return list_of_dates

def extract_load_data():
    for date in extract_list_of_dates(start_date=start_date, number_of_days=number_of_days):
        params = {'$limit': 10,
                '$where': 'incident_datetime <=' + "'" + str(date) + "'"
        }
        r = requests.get(config.get('domain').get('url') + config.get('dataset').get('san_francisco_data') + '.json', 
                        params=params, 
                        headers=config.get('headers')
                        )
        if r.status_code != 200:
            raise RuntimeError('Can''t retrieve latest timestamp.' + r.text)
        
        filename = os.path.abspath(os.curdir) + "\\files\\" + str(config.get('dataset').get('san_francisco_data')) + "-" + str(time.time_ns()) + ".json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as write_file:
            json.dump(r.json(), write_file, indent=4)

    json_str = json.dumps(r.json(), indent=4)
    # json_obj = r.json()
    return json_str

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "socrata-vaz-data"

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    # Note: The call returns a response only when the iterator is consumed.
    for blob in blobs:
        print(blob.name)

list_blobs("socrata-vaz-data")
