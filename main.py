import argparse
from sys import argv
from datetime import date, datetime, timedelta, time
from socrata import *

with open('config.json', 'r') as f:
    config = json.load(f)

get_url = config.get('api').get('domain').get('url') + config.get('api').get('dataset').get('san_francisco_data') + '.json'
get_headers = config.get('api').get('headers')
params = config.get('api').get('params')


parser = argparse.ArgumentParser(description="Extract the dataset named Police Department Incident Reports: 2018 to Present \
                                 from The City and Condado of San Francisco. Socrata Open Data API have been used to programmatically \
                                 return the dataset.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
type_modes = ["LAST_DATE", "REFRESH"]
parser.add_argument("-m", "--mode", type=str, choices=type_modes, default=type_modes[0], required=True, help="the reference is the last date")
parser.add_argument("-s", "--start_date", type=datetime.fromisoformat, default="2018-01-01", required=("--mode="+type_modes[1] in argv), help="used with refresh: from the desired date since 2018-01-01")
args = vars(parser.parse_args())

start_date = args["start_date"]
start_date_iso = (datetime(start_date.year, start_date.month, start_date.day) + timedelta(0, hours=23,minutes=59,seconds=59,microseconds=999999)).isoformat()
print("--mode="+type_modes[1] in argv, argv, start_date, start_date_iso)

Socrata(get_url,get_headers,params)