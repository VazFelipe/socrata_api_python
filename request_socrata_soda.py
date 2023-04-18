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
bucket_name = "socrata-vaz-data"

def storage_client():
    storage_client = storage.Client.from_service_account_json(config.get('gcp').get('credentials').get('folder'))
    return storage_client

def bucket_blob(bucket_name, blob_name):
    """Get ready to write and read a blob from GCS using file-like IO
    The ID of your GCS bucket
    bucket_name = "your-bucket-name"

    The ID of your new GCS object
    blob_name = "storage-object-name"
    """
    client = storage_client() #storage.Client.from_service_account_json(config.get('gcp').get('credentials').get('folder'))
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    return bucket, blob

def fetch_max_date_from_bucket(bucket_name):
    client = storage_client()
    return client

def extract_list_of_dates(start_date, number_of_days):
    list_of_dates=[]
    for day in range(day_range):
        if day <= day_range:
            if day <= number_of_days-1:
                list_of_dates.append((datetime(year=start_date.year,month=start_date.month,day=start_date.day) + timedelta(day, hours=23,minutes=59,seconds=59,microseconds=999999)).isoformat())
    return list_of_dates

def extract_load_data(bucket_name, start_date, number_of_days):
    # filename = os.path.abspath(os.curdir) + "\\files\\" + str(config.get('dataset').get('san_francisco_data')) + "-" + str(time.time_ns()) + ".json"
    # os.makedirs(os.path.dirname(filename), exist_ok=True)

    if number_of_days == 0:
        message = "Require the number_of_days greater than or equal to 1 to extract data"
    else: 
        for date in extract_list_of_dates(start_date=start_date, number_of_days=number_of_days):
            
            params = {'$limit': 10,
                    '$where': 'incident_datetime <=' + "'" + str(date) + "'"
            }
                
            r = requests.get(config.get('api').get('domain').get('url') + config.get('api').get('dataset').get('san_francisco_data') + '.json', 
                            params=params, 
                            headers=config.get('headers')
                            )
            if r.status_code != 200:
                raise RuntimeError('Can''t retrieve latest timestamp.' + r.text)
            else:
                json.dumps(r.json(), indent=4)
            
            blob_name = "socrata/" + "dataset_" + str(config.get('api').get('dataset').get('san_francisco_data')) + "_crimes_" + str(datetime.fromisoformat(date).strftime("%Y-%m-%d")) + "_loaded_" + str(time.time_ns()) + ".json"
            blob = bucket_blob(bucket_name=bucket_name, blob_name=blob_name)[1]
            
            with blob.open("w") as write_file:
                json.dump(r.json(), write_file, indent=4)
            message = f'{number_of_days} day(s) loaded in the {bucket_name} bucket'
    
    return message

def list_buckets_blobs(bucket_name):
    """Lists all buckets."""
    client = storage_client() #storage.Client.from_service_account_json(config.get('gcp').get('credentials').get('folder'))
    buckets = client.list_buckets()
    blobs = client.list_blobs(bucket_name)

    for bucket in buckets:
        bucket = bucket.name
    storage_dict = dict(bucket = bucket)

    blob_str = []
    for blob in blobs:
        blob_str.append(blob.name)

    # for a, b in enumerate(blob):
    #     storage_dict[a] = b

    return blob_str #storage_dict # bucket, blob

# print(extract_load_data(bucket_name=bucket_name, start_date=start_date, number_of_days=3))
print(list_buckets_blobs(bucket_name))
