import logging
from dataclasses import dataclass, field

@dataclass
class Log:
    filename: str = field(default='./socrata_log.log', init=False)
    format: str = field(default='%(asctime)s - %(name)s - %(levelname)s - %(message)s', init=False)

    def configure_log(self):
            logging.basicConfig(
                filename=self.filename, 
                format=self.format,
                level=logging.INFO,
                filemode='a'
                )

@dataclass
class StartRecord(Log):
    type: str
    message: str
      
    def record(self):
            return logging.log(getattr(logging, self.type), self.message)

if __name__ == '__main__':
    log = Log().configure_log()

    try:
        n1 = int(input("Digite o dividendo: "))
        n2 = int(input("Digite o divisor: "))
        result = f"O quociente é: {n1 / n2}"
        StartRecord(type='INFO', message=result).record()
        print(result)
    except ZeroDivisionError as error:
        StartRecord(type='WARNING', message=error).record()
        raise