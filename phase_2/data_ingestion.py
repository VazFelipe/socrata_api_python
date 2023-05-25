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
        self.get_url = config.get('api').get('domain').get('url') + config.get('api').get('dataset').get('san_francisco_data') + '.json'
        self.get_headers = config.get('api').get('headers')
        self.params = config.get('api').get('params')

    def list_dates(self):
        self.blob_list = Blob().list_blobs()
        pattern = "([0-9]{4}\-[0-9]{2}\-[0-9]{2})"

        for date in self.blob_list:
            dates = str(re.findall(pattern=pattern, string=date)).replace('[','').replace(']','').strip("'")
            self.blob_list_inter.append((datetime.fromisoformat(str(dates)) + timedelta(days=1, hours=0,minutes=0,seconds=0)).strftime("%Y-%m-%dT%H:%M:%S"))
            max_date = max(self.blob_list_inter)
        
        self.blob_dict["last_date"] = max_date
        logger.info('From {cls} the attr: {attr}'.format(cls=type(self.blob_dict).__name__, attr=self.blob_dict), exc_info=True)
        return self.blob_dict["last_date"]

    def ingestion(self):
        if args["mode"] == 'LAST_DATE':
            max_date = Data().list_dates()
            request = Socrata(url=self.get_url, headers=self.get_headers, parameters=self.params, start_date=max_date).api_connection()
            
            logger.info('From {cls} the attr: {attr}'.format(cls=type(request).__name__, attr=request), exc_info=True)
                
            if request.status_code != 200:
                logger.info('From {cls} the attr: {attr}'.format(cls=type(request.status_code).__name__, attr=request.status_code), exc_info=True)
                raise RuntimeError('Can''t retrieve latest timestamp.' + request.text)
            else:
                json.dumps(request.json(), indent=4)
                logger.info('From {cls} the attr: {attr}'.format(cls=type(request.json()).__name__, attr=request.json()[-1:]), exc_info=True)
            
            blob_name = str(datetime.fromisoformat(max_date).strftime("%Y-%m-%d")) + "_dataset_" + str(config.get('api').get('dataset').get('san_francisco_data')) + "_crimes_in_loaded_" + str(time.time_ns()) + ".json"
            blob = Blob_obj(blob_name=blob_name).blob_obj()

            logger.info('From {cls} the attr: {attr}'.format(cls=type(blob).__name__, attr=blob), exc_info=True)
            
            with blob.open("w") as write_file:
                json.dump(request.json(), write_file, indent=4)
            message = f'{max_date} loaded in the {Bucket().bucket_name} bucket'

            logger.info('From {cls} the attr: {attr}'.format(cls=type(message).__name__, attr=message), exc_info=True)
    
        return message
            

if __name__ == '__main__':
        Data