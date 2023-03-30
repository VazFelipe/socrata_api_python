
from datetime import datetime
import pandas as pd
import pandas as pd
from sodapy import Socrata

initial_date = datetime(year=2023, month=3, day=28, hour=23, minute=59, second=59)
today_date = datetime.now()
delta_date = today_date - initial_date

def fetch_next_day(days):
    next_day = initial_date + pd.Timedelta(days=days)
    return next_day

def extract_list_of_dates(next_day):
    list = fetch_next_day(next_day)
    list_of_dates = [list[i] for i in range(delta_date.days+1)]
    return list_of_dates
            
def extract_data(list_of_dates):
    client = Socrata(domain="data.sfgov.org",
                 app_token="",
                 username="",
                 password="")
    query = f'select count(*) where incident_datetime < "{[list_of_dates[i] for i in range(list_of_dates)]}]"'
    # requests = client.get("wg3w-h783", query=[])
    # results = client.get("wg3w-h783", query=query)
    return query

print(extract_data(list_of_dates=extract_list_of_dates(fetch_next_day())))
# print(fetch_next_day(1), delta_date.days+1, next_day, type(next_day))

# print(initial_date.isoformat(), next_day.isoformat())
# print(initial_date, today_date, delta_date.days)