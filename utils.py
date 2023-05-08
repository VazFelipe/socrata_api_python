import logging
from datetime import timedelta
from dataclasses import dataclass

@dataclass
class Log:
    log = str

    def __post_init__(self):
         self.log = logging.getLogger(__name__)
         return self.log

@dataclass
class Utils(Log):
    args_dict: dict

    def modify_entry_params(self):
            my_log = self.log

            for key, value in self.args_dict.items():
            
                my_log.debug("args_dict.items(): {0}".format(key, value))
            
                if key.endswith("date"):
            
                    my_log.debug("args_dict.items() == date: {0}".format(key))
            
                    args_dict_updated = {key: (value + timedelta(days=0, hours=23, minutes=59, seconds=59, microseconds=999999)).isoformat()}
            
                    my_log.debug("args_dict_updated: {0}".format(args_dict_updated))
                    self.args_dict.update(args_dict_updated)

            my_log.debug("args_dict_updated: {0}".format(args_dict_updated))
            my_log.debug("args_dict: {0}".format(self.args_dict))
            my_log.info("args_dict: {0}".format(self.args_dict))

            return self.args_dict

if __name__ == '__main__':
    Utils