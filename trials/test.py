
from datetime import date, datetime, timedelta
import pandas as pd
import pandas as pd
from sodapy import Socrata
import json
import time
import ast
import re
import os

# context manager opens the config.json and close it as soon as the end of the process
with open('config.json', 'r') as f:
    config = json.load(f)

initial_date = date(2022,1,1)
end_date = date(2022,1,10)
number_of_days_for_batch = 2

def extract_list_of_dates(start_date, end_date, number_of_days_for_batch):
    list_of_dates=[]
    max_number_of_days_for_processing = int((end_date - start_date).days)+1
    for day in range(max_number_of_days_for_processing):
        if day < number_of_days_for_batch:
            list_of_dates.append((datetime(year=start_date.year,month=start_date.month,day=start_date.day) + timedelta(day, hours=23,minutes=59,seconds=59,microseconds=999999)).isoformat())
    return list_of_dates
            
def extract_data(start_date, end_date, number_of_days_for_batch):
    output = []
    for dates in extract_list_of_dates(start_date=start_date, end_date=end_date, number_of_days_for_batch=number_of_days_for_batch):

        yesterday = datetime.strptime(dates,"%Y-%m-%dT%H:%M:%S.%f") - timedelta(1)
        
        start_counter, start_time = time.perf_counter(), datetime.now()
        
        client = Socrata(domain="data.sfgov.org",
                    app_token=config.get('credentials').get('app_token'),
                    username=config.get('credentials').get('username'),
                    password=config.get('credentials').get('password'))
        
        
        results = client.get("wg3w-h783", content_type="json", query=f'select date_trunc_ymd(incident_datetime) AS incident_datetime, count(incident_datetime) AS row_count where incident_datetime between "{yesterday.isoformat()}" and "{dates}" group by date_trunc_ymd(incident_datetime) order by incident_datetime')
        
        # p = re.compile('(?<!\\\\)\'')
        # results = p.sub('\"', str(results))
        
        # results = str(results).replace("'", '"')
        # results = results.replace("'[", "").replace("]'", "")
        
        # output.append(results)

        # stop_counter, stop_time = time.perf_counter(), datetime.now()
        # elapsed_seconds = round(stop_counter - start_counter, 4)
        # # parsed_json = ast.literal_eval(str(output))
        json_obj = json.loads(results)
        json_obj.update(results)
    return json_obj
data = extract_data(start_date=initial_date, end_date=end_date, number_of_days_for_batch=number_of_days_for_batch)

# json_obj = json.dumps(data, indent=4, sort_keys=True)

# print(data["incident_datetime"])
print(data)

# c:\Users\144553\Downloads
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# c:\Users\144553\Downloads\projectTest
ROOT_DIR_2 = os.path.abspath(os.curdir)

print(ROOT_DIR, ROOT_DIR_2)