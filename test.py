
from datetime import date, datetime, timedelta
import pandas as pd
import pandas as pd
from sodapy import Socrata
import json
from time import perf_counter

with open('config.json', 'r') as f:
    config = json.load(f)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

initial_date = date(2022,1,1)
today_date = date(2022,1,2)
# date.today()

def extract_list_of_dates():
    # next_day = fetch_next_day()
    for single_date in daterange(initial_date, today_date):
        yield (datetime(year=single_date.year,month=single_date.month,day=single_date.day) + timedelta(hours=23,minutes=59,seconds=59,microseconds=999999)).isoformat()
            
def extract_data():
    output = []
    elapsed = []
    for dates in extract_list_of_dates():
        start_time = perf_counter()
        client = Socrata(domain="data.sfgov.org",
                    app_token=config.get('credentials').get('app_token'),
                    username=config.get('credentials').get('username'),
                    password=config.get('credentials').get('password'))
        yesterday = datetime.strptime(dates,"%Y-%m-%dT%H:%M:%S.%f") - timedelta(1)
        results = client.get("wg3w-h783", query=f'select date_trunc_ymd(incident_datetime) AS incident_datetime, count(incident_datetime) AS countReg where incident_datetime between "{yesterday.isoformat()}" and "{dates}" group by date_trunc_ymd(incident_datetime) order by incident_datetime')
        results_df = pd.DataFrame.from_records(results)
        stop_time = perf_counter()
        elapsed_time = str(stop_time - start_time)
        elapsed_time_df = pd.DataFrame.from_records(elapsed_time, columns=['elapsed_time'])
        output.append(results_df) 
        results_df['elapsed_time'] =  elapsed_time_df
        results_df = pd.concat(output)
    return results_df

# for value in extract_list_of_dates():
#     print(value)

print(extract_data())

# print(type(results_df), results_df)
# print(fetch_next_day(1), delta_date.days+1, next_day, type(next_day))

# print(initial_date.isoformat(), next_day.isoformat())
# print(initial_date, today_date, delta_date.days)