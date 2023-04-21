import requests
import json
import os
from datetime import date, datetime, timedelta, time
import time
from google.cloud import storage

# storage.Client.from_service_account_json(config.get('gcp').get('credentials').get('folder'))
# filename = os.path.abspath(os.curdir) + "\\files\\" + str(config.get('dataset').get('san_francisco_data')) + "-" + str(time.time_ns()) + ".json"
# os.makedirs(os.path.dirname(filename), exist_ok=True)

with open('config.json', 'r') as f:
    config = json.load(f)

start_date = date(2018, 1, 9) 
end_date = date.today()
day_range = int((end_date - start_date).days)+1
number_of_days = 1
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
    client = storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    return bucket, blob

def extract_list_of_dates(start_date, number_of_days, bucket_name):
    """ Return a list of dates from start_date to end_date. 
        
        If the bucket has N blobs then gets from fetch_max_date_from_bucket() 
        the max_date from the name of blob and return the list_of_dates from that max_date  
    """

    list_of_dates=[]
    if number_of_days == 1:
        number_of_days = 2
    
    for day in range(day_range):
        if day <= day_range:
            if day <= number_of_days-1:
                list_of_dates.append((datetime(year=start_date.year,month=start_date.month,day=start_date.day) + timedelta(day, hours=23,minutes=59,seconds=59,microseconds=999999)).isoformat())
                if number_of_days == 0:
                    list_of_dates = []
    # last_day_list_of_dates = str(list_of_dates[-1])[:10]
    # list_of_dates_before = list_of_dates
    # date_in_bucket = fetch_max_date_from_bucket(bucket_name)
    if list_of_dates == []:
        list_of_dates = []

    # if the bucket has no blobs return the list_of_dates
    if fetch_max_date_from_bucket(bucket_name) == {}:
        list_of_dates
    
    # if the bucket has blobs and the max_date is equal to the last_day of the range return an empty list_of_dates
    if list_of_dates != [] and fetch_max_date_from_bucket(bucket_name) == str(list_of_dates[-1])[:10]:
        list_of_dates = []

    # if the bucket has blobs and the max_date is less than the last day of the range return the list_of_dates from that
    else:
        list_of_dates = [dates for dates in list_of_dates if dates > fetch_max_date_from_bucket(bucket_name)]
        list_of_dates = list_of_dates[1:]
    
    count_of_dates = len(list_of_dates)

    return list_of_dates, count_of_dates #, last_day_list_of_dates, date_in_bucket

def extract_load_data(bucket_name, start_date, number_of_days):
    """ Define """
    if extract_list_of_dates(start_date, number_of_days, bucket_name)[0] == [] and number_of_days == 0:
        message = "Require the number_of_days greater than or equal to 1 to extract data"
        # pass
    if extract_list_of_dates(start_date, number_of_days, bucket_name)[0] == [] and number_of_days != 0:
        message = f"The max_incident_date in the bucket is {fetch_max_date_from_bucket(bucket_name)}. There's already this range of dates {number_of_days}, from {start_date} to {start_date + timedelta(days=number_of_days-1)}. Try a start_date greater than this."
    else:
        count_of_files_loaded = 0 
        for date in extract_list_of_dates(start_date, number_of_days, bucket_name)[0]:

            params = {#'$limit': 10,
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
            
            blob_name = "socrata/" + str(datetime.fromisoformat(date).strftime("%Y-%m-%d")) + "_dataset_" + str(config.get('api').get('dataset').get('san_francisco_data')) + "_crimes_in_loaded_" + str(time.time_ns()) + ".json"
            blob = bucket_blob(bucket_name=bucket_name, blob_name=blob_name)[1]
            
            with blob.open("w") as write_file:
                json.dump(r.json(), write_file, indent=4)
            count_of_files_loaded += 1
            message = f'{count_of_files_loaded} day(s) loaded in the {bucket_name} bucket'
    
    return message

def fetch_max_date_from_bucket(bucket_name):
    """Return the max incident_date from blob.name in the bucket, otherwise an empty dict"""
    client = storage_client()
    buckets = client.list_buckets()
    blobs = client.list_blobs(bucket_name)

    blob_list = []
    for blob in blobs:
        blob_name = blob.name
        blob_adjusted = blob_name[8:18]
        blob_list.append(blob_adjusted)
    
    blob_dict = dict(enumerate(blob_list))

    for max_value in sorted(blob_dict, key=blob_dict.get, reverse=True):
        return blob_dict[max_value]

    return blob_dict

print(f"The max date in the bucket is {fetch_max_date_from_bucket(bucket_name)}")
print(f"The list_of_dates to load into the bucket is {extract_list_of_dates(start_date,number_of_days=number_of_days,bucket_name=bucket_name)}")
print(extract_load_data(bucket_name=bucket_name, start_date=start_date, number_of_days=number_of_days))
