from datetime import date, datetime, timedelta
import json
from time import perf_counter

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2023, 4, 1)
end_date = date.today()
end_of_processing = datetime.now()

def myfunc():
    for single_date in daterange(start_date, end_date):
        mydate = datetime(year=single_date.year,month=single_date.month,day=single_date.day) + timedelta(hours=23,minutes=59,seconds=59,microseconds=999999)
        yield mydate.isoformat()

def mynewfunc():
    for dates in myfunc():
        print(datetime.strptime(dates,"%Y-%m-%dT%H:%M:%S.%f") - timedelta(1), dates)

start_count = perf_counter()
stop_count = perf_counter()
end_of_processing_unix = end_of_processing.timestamp()*1e3
# end_of_processing_datetime = datetime.fromtimestamp(end_of_processing_unix)


elapsed = str(stop_count - start_count)

print(end_of_processing, end_of_processing_unix, type(end_of_processing_unix), datetime.fromtimestamp(end_of_processing_unix / 1000))#, end_of_processing_datetime)


# mynewfunc()

# for value in myfunc():
#     print(value)

# with open('config.json', 'r') as f:
#     config = json.load(f)

# print(config["credentials"]["app_token"])