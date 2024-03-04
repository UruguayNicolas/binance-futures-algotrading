import os
import time
from pathlib import Path
from provider import Candlesticks


class Main:
    def __init__(self):
        self.path = 'provider/data/'
        data = Path(self.path + 'candlesticks.csv')

        # If candlesticks.csv aready exists remove it
        if data.is_file():
            print("Cleaning logs..")
            os.remove(data)
            time.sleep(3)

        self.candlesticks = Candlesticks()

    def start(self):
        self.candlesticks.subscribe()


if __name__ == "__main__":
    main = Main()
    main.start()
