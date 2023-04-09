#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata
from datetime import datetime
import json

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
# client = Socrata("data.sfgov.org", None)

with open('config.json', 'r') as f:
    config = json.load(f)

# Example authenticated client (needed for non-public datasets):
client = Socrata(domain="data.sfgov.org",
            app_token=config.get('credentials').get('app_token'),
            username=config.get('credentials').get('username'),
            password=config.get('credentials').get('password'))
initial_date = datetime(year=2018, month=1, day=1, hour=23, minute=59, second=59, microsecond=999999)



query = f'select count(*) where incident_datetime < "{initial_date.isoformat()}"' # f'select count(*) where incident_number="210061105"'

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("wg3w-h783", content_type="CSV", select="incident_datetime", where='incident_datetime < "2018-01-02T00:00:00.000"')

#select="count(*)", where="incident_datetime <= '2018-01-02T23:59:59'")  # 'select incident_number where incident_number = "210061105"') #limit=10, offset=0, order="incident_id") # query=query) #"SELECT max(incident_datetime)") #, 

# Convert to pandas DataFrame
# results_df = pd.DataFrame.from_records(results)
json_obj = json.loads(results)

print(type(json_obj))

# print(results_df.info())

# print(results_df.loc[:, ["incident_number","incident_id"]])
# results_df_selection = results_df[results_df["incident_number"] == '210061105']

# print(results_df_selection.T)

# print(type(results_df), results_df)
# print(query)