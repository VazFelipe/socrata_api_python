from datetime import date, datetime, timedelta
import json
# from time import perf_counter
import time
import pandas as pd
import itertools

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

start_count = time.perf_counter()
stop_count = time.perf_counter()
unix_seconds = int(end_of_processing.timestamp())
unix_milliseconds = int(end_of_processing.timestamp()*1e3)
unix_microseconds = end_of_processing.timestamp()
unix_nanoseconds = time.time_ns()
unix = time.time()
end_of_processing_unix = end_of_processing.timestamp()*1e3
teste_4 = int(round((end_of_processing.timestamp()*1e3)/1000,0))


elapsed = str(stop_count - start_count)


# print(unix)
# print(unix_seconds)
print(unix_milliseconds)
print(unix_microseconds)
print(unix_nanoseconds)
print(pd.Timestamp(unix_nanoseconds))
print(time.time_ns())
# print(end_of_processing)
# print(end_of_processing_unix)
# print(teste_4)
# print(datetime.fromtimestamp(teste_4))
# print(datetime.fromtimestamp(end_of_processing_unix / 1000))


# mynewfunc()

# for value in myfunc():
#     print(value)

# with open('config.json', 'r') as f:
#     config = json.load(f)

# print(config["credentials"]["app_token"])

day_range = int((end_date - start_date).days)+1

def extract_list_of_dates(start_date, number_of_days):
    list_of_dates=[]
    for day in range(day_range):
        if day <= day_range:
            if day <= number_of_days-1:
                list_of_dates.append((datetime(year=start_date.year,month=start_date.month,day=start_date.day) + timedelta(day, hours=23,minutes=59,seconds=59,microseconds=999999)).isoformat())
    return list_of_dates
print(extract_list_of_dates(start_date=start_date, number_of_days=3))
# for i in range(1,date_range+1):
#     print(i)
# print(date_range))
    # output.append((datetime(year=list_of_dates.year,month=list_of_dates.month,day=list_of_dates.day) + timedelta(day, hours=23,minutes=59,seconds=59,microseconds=999999)).isoformat())
