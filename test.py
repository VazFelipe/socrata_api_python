
from datetime import date, datetime, timedelta
import pandas as pd
import pandas as pd
from sodapy import Socrata
import json

with open('config.json', 'r') as f:
    config = json.load(f)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

initial_date = date(2023,4,1)
today_date = date.today()

def extract_list_of_dates():
    # next_day = fetch_next_day()
    for single_date in daterange(initial_date, today_date):
        yield (datetime(year=single_date.year,month=single_date.month,day=single_date.day) + timedelta(hours=23,minutes=59,seconds=59,microseconds=999999)).isoformat()
            
def extract_data():
    for dates in extract_list_of_dates():
        client = Socrata(domain="data.sfgov.org",
                    app_token=config.get('app_token'),
                    username=config.get('username'),
                    password=config.get('password'))
        results = client.get("wg3w-h783", query=f'select count(*) where incident_datetime <= "{dates}"')
        results_df = pd.DataFrame.from_records(results)
    return results_df

# for value in extract_list_of_dates():
#     print(value)

print(extract_data())

# print(type(results_df), results_df)
# print(fetch_next_day(1), delta_date.days+1, next_day, type(next_day))

# print(initial_date.isoformat(), next_day.isoformat())
# print(initial_date, today_date, delta_date.days)