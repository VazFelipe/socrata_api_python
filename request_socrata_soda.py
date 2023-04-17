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
bucketname = "socrata-vaz-data"

def extract_list_of_dates(start_date, number_of_days):
    list_of_dates=[]
    for day in range(day_range):
        if day <= day_range:
            if day <= number_of_days-1:
                list_of_dates.append((datetime(year=start_date.year,month=start_date.month,day=start_date.day) + timedelta(day, hours=23,minutes=59,seconds=59,microseconds=999999)).isoformat())
    return list_of_dates

def extract_load_data(bucketname, start_date, number_of_days):
    storage_client = storage.Client.from_service_account_json('C:\\Users\\144553\\OneDrive - Localiza\\Vaz\\PDI\\GCP\\credentials\\vaz-data-1f9278fd0828.json')
    bucket = storage_client.bucket(bucket_name=bucketname)
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
        # filename = os.path.abspath(os.curdir) + "\\files\\" + str(config.get('dataset').get('san_francisco_data')) + "-" + str(time.time_ns()) + ".json"
        filename = str(config.get('dataset').get('san_francisco_data')) + "-" + str(time.time_ns()) + ".json"
        # os.makedirs(os.path.dirname(filename), exist_ok=True)
        blob = bucket.blob(filename)
        with blob.open("w") as write_file:
            json.dump(r.json(), write_file, indent=4)

    json_str = json.dumps(r.json(), indent=4)
    # json_obj = r.json()
    return json_str

extract_load_data(bucketname=bucketname, start_date=start_date, number_of_days=4)

def list_buckets_blobs(bucket_name):
    """Lists all buckets."""

    storage_client = storage.Client.from_service_account_json('C:\\Users\\144553\\OneDrive - Localiza\\Vaz\\PDI\\GCP\\credentials\\vaz-data-1f9278fd0828.json')
    buckets = storage_client.list_buckets()
    blobs = storage_client.list_blobs(bucket_name)

    for bucket in buckets:
        print(bucket.name)
    for blob in blobs:
        print(blob.name)

list_buckets_blobs("socrata-vaz-data")

def bucket(bucket_name):
    """Write and read a blob from GCS using file-like IO"""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your new GCS object
    # blob_name = "storage-object-name"

    storage_client = storage.Client.from_service_account_json('C:\\Users\\144553\\OneDrive - Localiza\\Vaz\\PDI\\GCP\\credentials\\vaz-data-1f9278fd0828.json')
    bucket = storage_client.bucket(bucket_name)
    # blob = bucket.blob(blob_name)

    return bucket

    # Mode can be specified as wb/rb for bytes mode.
    # See: https://docs.python.org/3/library/io.html
    with blob.open("w") as f:
        f.write("Hello world")

    with blob.open("r") as f:
        print(f.read())

# write_read("socrata-vaz-data", "first_commit")
