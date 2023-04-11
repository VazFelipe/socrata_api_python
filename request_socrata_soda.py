import requests
import json
import os
from datetime import date, datetime, timedelta, time
import time

with open('config.json', 'r') as f:
    config = json.load(f)


start_date = date(2018, 1, 1) 
end_date = date.today()
day_range = int((end_date - start_date).days)+1

print(end_date)

def extract_list_of_dates(start_date, number_of_days):
    list_of_dates=[]
    for day in range(day_range):
        if day <= day_range:
            if day <= number_of_days-1:
                list_of_dates.append((datetime(year=start_date.year,month=start_date.month,day=start_date.day) + timedelta(day, hours=23,minutes=59,seconds=59,microseconds=999999)).isoformat())
    return list_of_dates
print(extract_list_of_dates(start_date=start_date, number_of_days=3))

for date in extract_list_of_dates(start_date=start_date, number_of_days=3):
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
json_obj = r.json()

