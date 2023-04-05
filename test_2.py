from datetime import date, datetime, timedelta
import json

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2023, 4, 1)
end_date = date.today()

def myfunc():
    for single_date in daterange(start_date, end_date):
        mydate = datetime(year=single_date.year,month=single_date.month,day=single_date.day) + timedelta(hours=23,minutes=59,seconds=59,microseconds=999999)
        yield mydate.isoformat()

def mynewfunc():
    for dates in myfunc():
        print(datetime.strptime(dates,"%Y-%m-%dT%H:%M:%S.%f") - timedelta(1), dates)

mynewfunc()

# for value in myfunc():
#     print(value)

# with open('config.json', 'r') as f:
#     config = json.load(f)

# print(config["credentials"]["app_token"])