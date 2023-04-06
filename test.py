
from datetime import date, datetime, timedelta
import pandas as pd
import pandas as pd
from sodapy import Socrata
import json
from time import perf_counter

# context manager opens the config.json and close it as soon as the end of the process
with open('config.json', 'r') as f:
    config = json.load(f)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

initial_date = date(2022,1,1)
today_date = date(2022,1,10)

def extract_list_of_dates():
    for single_date in daterange(initial_date, today_date):
        yield (datetime(year=single_date.year,month=single_date.month,day=single_date.day) + timedelta(hours=23,minutes=59,seconds=59,microseconds=999999)).isoformat()
            
def extract_data():
    output = []
    for dates in extract_list_of_dates():

        days_for_processing = (today_date - initial_date).days+1

        yesterday = datetime.strptime(dates,"%Y-%m-%dT%H:%M:%S.%f") - timedelta(1)
        
        start_counter, start_time = perf_counter(), datetime.now()
        
        client = Socrata(domain="data.sfgov.org",
                    app_token=config.get('credentials').get('app_token'),
                    username=config.get('credentials').get('username'),
                    password=config.get('credentials').get('password'))
        
        
        results = client.get("wg3w-h783", query=f'select date_trunc_ymd(incident_datetime) AS incident_datetime, count(incident_datetime) AS row_count where incident_datetime between "{yesterday.isoformat()}" and "{dates}" group by date_trunc_ymd(incident_datetime) order by incident_datetime')
        results_df = pd.DataFrame.from_records(results)
        
        stop_counter, stop_time = perf_counter(), datetime.now()
        elapsed_seconds = round(stop_counter - start_counter, 4)
        
        output.append(results_df) 
        
        results_df['start_time'] = str(start_time)
        results_df['stop_time'] = str(stop_time)
        results_df['elapsed_seconds'] =  str(elapsed_seconds)
        
        results_df = pd.concat(output)

        f_csv = results_df.to_csv(f'dataset_wg3w-h783_socrata_{str(stop_time.strftime("%Y%m%d-%H%M%S"))}.csv', encoding='utf-8', index=False)
    return results_df, days_for_processing, 


print(extract_data())