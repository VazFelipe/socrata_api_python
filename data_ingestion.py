import json
import argparse
import logging.config
import time
import re
from sys import argv
from datetime import date, datetime
from dataclasses import dataclass, field
from collections import defaultdict
from socrata import *
from utils import *
from storage import *

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

with open('config.json', 'r') as f:
    config = json.load(f)

parser = argparse.ArgumentParser(description="Extract the dataset named Police Department Incident Reports: 2018 to Present \
                                 from The City and Condado of San Francisco. Socrata Open Data API have been used to programmatically \
                                 return the dataset.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
type_modes = ["LAST_DATE", "REFRESH"]
parser.add_argument("-m", "--mode", type=str, choices=type_modes, default=type_modes[0], required=True, help="the reference is the last date")
# parser.add_argument("-s", "--start_date", type=datetime.fromisoformat, default="2018-01-01", required=("--mode="+type_modes[1] in argv), help="used with refresh mode: from the desired date since 2018-01-01")
# parser.add_argument("-e", "--end_date", type=datetime.fromisoformat, default="2018-01-01", required=("--mode="+type_modes[1] in argv), help="used with refresh mode: from the desired date since 2018-01-01")
args = vars(parser.parse_args())
#date.today()
#2018-01-01

@dataclass
class Data:
    args: "defaultdict[dict]" = field(default_factory=lambda: defaultdict(dict), init=False)
    blob_list_inter: list = field(default_factory=list, init=False)
    blob_dict: "defaultdict[dict]" = field(default_factory=lambda: defaultdict(dict), init=False)
    date_list: list = field(default_factory=list, init=False)
    date_dict: "defaultdict[dict]" = field(default_factory=lambda: defaultdict(dict), init=False)
    day_range: int = field(init=False)
    end_date: str = field(init=False)
    get_url: str = field(init=False)
    get_headers: str = field(init=False)
    params: str = field(init=False)
    start_date: str = field(init=False)
     
    def __post_init__(self):
        # self.end_date = args["end_date"]
        self.get_url = config.get('api').get('domain').get('url') + config.get('api').get('dataset').get('san_francisco_data') + '.json'
        self.get_headers = config.get('api').get('headers')
        self.params = config.get('api').get('params')
        # self.start_date = args["start_date"]
    
    def list_dates(self):
        # self.day_range = int((datetime.strptime(str(self.end_date), "%Y-%m-%d %H:%M:%S") - datetime.strptime(str(self.start_date), "%Y-%m-%d %H:%M:%S")).days)
        self.blob_list = Blob().list_blobs()
        pattern = "([0-9]{4}\-[0-9]{2}\-[0-9]{2})"
        
        # for day in range(self.day_range):
        #     if day <= self.day_range:
        #         date = (datetime.fromisoformat(str(self.start_date)) + timedelta(days=day+1, hours=0,minutes=0,seconds=0)).strftime("%Y-%m-%dT%H:%M:%S")
        #         self.date_list.append(date)
        # self.date_list.append((datetime.fromisoformat(str(self.start_date)) + timedelta(days=0, hours=0,minutes=0,seconds=0)).strftime("%Y-%m-%dT%H:%M:%S"))
        
        # self.date_dict["refresh"] = self.date_list 

        for date in self.blob_list:
            dates = str(re.findall(pattern=pattern, string=date)).replace('[','').replace(']','').strip("'")
            self.blob_list_inter.append((datetime.fromisoformat(str(dates)) + timedelta(days=0, hours=0,minutes=0,seconds=0)).strftime("%Y-%m-%dT%H:%M:%S"))
            max_date = max(self.blob_list_inter)
        
        self.blob_dict["last_date"] = max_date
        # self.date_dict.update(self.blob_dict)
        return self.blob_dict

    def ingestion(self):

       
    #    connection_start_time = time.time()
    #    connection_timeout = 1
    #    day_range = int((datetime.fromisoformat(self.end_date) - datetime.fromisoformat(self.start_date)).days)+1
    #    loop_counter = 0
        if args["mode"] == 'LAST_DATE':
            dates = Data().list_dates()
            for key, dates in dates.items():
                if key == 'last_date':
                    connection = Socrata(url=self.get_url, headers=self.get_headers, parameters=self.params, start_date=dates).api_connection()
                return connection
        


    #    while day_range > loop_counter:
    #        try:
    #            logger.info('From {cls} starting connection on Socrata API with attr: {attr}'.format(cls=self.params.__class__.__name__, attr=self.params), exc_info=True)

    #            connection = Socrata(url=self.get_url, headers=self.get_headers, parameters=self.params, start_date=self.start_date).api_connection()
                
    #             # print(json.dumps(connection.json(), indent=4))

    #            loop_counter += 1
    #            break 
    #        except TimeoutError:
    #            if time.time() > connection_start_time + connection_timeout:
    #                logger.error('From {cls} unable to get connection after {attr} seconds of TimeoutError'.format(cls=type(connection_timeout).__name__, attr=connection_timeout))
                   
    #                raise Exception('From {cls} unable to get connection after {attr} seconds of TimeoutError'.format(cls=type(connection_timeout).__name__, attr=connection_timeout))
    #            else:
    #                logger.info('From {cls} starting retry logic every {attr} second'.format(cls=type(connection_timeout).__name__, attr=connection_timeout))
    #                time.sleep(1)
    #        finally:
    #            logger.info("From {cls} ending connection on Socrata API with attr: {attr}".format(cls=type(connection).__name__, attr=connection.ok))

if __name__ == '__main__':
        Data
        # print(Data().ingestion())
        print(Data().list_dates())
        # print(Params(parameters=config.get('api').get('params'), start_date=args["start_date"]))
