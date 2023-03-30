#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata
from datetime import datetime

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
# client = Socrata("data.sfgov.org", None)

# Example authenticated client (needed for non-public datasets):
client = Socrata(domain="data.sfgov.org",
                 app_token="Ax7ks1Cmr0r6TEssy44yJj4ts",
                 username="2osd2wzioj43v7iymmfnt74x3",
                 password="4x7f0iwwas0wppj8szt7n6ddln8ni1s52tn17q492ju0s5pku1")

initial_date = datetime(year=2018, month=1, day=1, hour=00, minute=00, second=00)



query = f'select count(*) where incident_datetime < "{initial_date.isoformat()}"' # f'select count(*) where incident_number="210061105"'

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("wg3w-h783", query=query)

#select="count(*)", where="incident_datetime <= '2018-01-02T23:59:59'")  # 'select incident_number where incident_number = "210061105"') #limit=10, offset=0, order="incident_id") # query=query) #"SELECT max(incident_datetime)") #, 

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

# print(results_df.info())

# print(results_df.loc[:, ["incident_number","incident_id"]])
# results_df_selection = results_df[results_df["incident_number"] == '210061105']

# print(results_df_selection.T)

# print(type(results_df), results_df)
# print(query)