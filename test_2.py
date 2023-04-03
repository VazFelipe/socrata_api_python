from datetime import date, datetime, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2023, 4, 1)
end_date = date.today()

def myfunc():
    for single_date in daterange(start_date, end_date):
        mydate = datetime(year=single_date.year,month=single_date.month,day=single_date.day) + timedelta(hours=23,minutes=59,seconds=59,microseconds=999999)
        yield mydate.isoformat()
    
for value in myfunc():
    print(value)