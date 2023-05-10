import logging
from dataclasses import dataclass, field

@dataclass
class Level:
    levels: dict = field(init=False)
    type: str

    def __post_init__(self):
        self.levels = {
                        "exception": logging.exception,
                        "info": logging.info,
                        "warning": logging.warning,
                        "error": logging.error,
                        "debug": logging.debug,
                        "critical": logging.critical
        }

    def parameterized_levels(self):
        for key, value in self.levels.items():
            if key == self.type:
                levels_updated = {key: value}
                self.levels.update(levels_updated)
        return self.levels
    
@dataclass
class Log(Level):
    filename: str
    message: str
    formated: str = "%(levelname)s:[%(asctime)s]: %(message)s"

    def record(self):
        for key, value in self.levels.items():
            if key == self.type:
                log_level = self.levels[key]
                logging.basicConfig(filename=self.filename, format=self.formated, level=log_level)
        raise ValueError(
            f'Error implementing the method "{self.record.__name__}" in class Logs.'
        )

if __name__ == '__main__':
   try:
       n1 = int(input("Digite o dividendo: "))
       n2 = int(input("Digite o divisor: "))
       result = f"O quociente é: {n1 / n2}"
       Log(filename="my_logs.log", type="info", message=result).record()
       print(result)
   except ZeroDivisionError as text:
       Log(filename="my_logs.log", type="info", message=text).record()
       raise