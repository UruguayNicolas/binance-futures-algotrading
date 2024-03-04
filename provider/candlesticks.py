import json
import datetime
import websocket
import pandas as pd
from settings import logger
from settings import Config
from settings import Storage


class Candlesticks(Config):
    def __init__(self):
        super().__init__()
        self.candles = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
        self.storage = Storage()

    def __on_open__(self, _):
        logger.info('Candlesticks socket opened.')

    def __on_close__(self, _):
        logger.info('Candlesticks socket closed.')

    def __on_message__(self, _, message):
        json_message = json.loads(message)

        candle = json_message['k']
        is_candle_closed = candle['x']

        _open = candle['o']
        _high = candle['h']
        _low = candle['l']
        _close = candle['c']
        _volume = candle['v']

        # Add the current date and time as a new column 'date'
        # Convert the date in milliseconds to a datetime object
        timestamp_ms = int(candle['t']) / 1000  # Convert miliseconds to seconds
        current_datetime = datetime.datetime.fromtimestamp(timestamp_ms)

        if self.candles.empty:
            # If the DataFrame is empty, create a new DataFrame
            # with the data of the current candlestick and add a row.
            self.candles.loc[current_datetime] = {'open': _open,
                                                  'high': _high,
                                                  'low': _low,
                                                  'close': _close,
                                                  'volume': _volume}
            self.storage.save(self.candles.tail(1))
        else:
            if is_candle_closed:
                # If the candlestick is closed
                # assign all the new values and add a new empty row.
                self.candles.loc[current_datetime] = {'open': _open,
                                                      'high': _high,
                                                      'low': _low,
                                                      'close': _close,
                                                      'volume': _volume}
                self.storage.save(self.candles.tail(1))

                self.candles.loc[current_datetime + datetime.timedelta(seconds=60)] = {'open': None,
                                                                                       'high': None,
                                                                                       'low': None,
                                                                                       'close': None,
                                                                                       'volume': None}
            else:
                # If the candlestick is not closed, update the current row (the last row).
                self.candles.loc[current_datetime] = {'open': _open,
                                                      'high': _high,
                                                      'low': _low,
                                                      'close': _close,
                                                      'volume': _volume}
                self.storage.update(self.candles.tail(1))

        self.candles.index.name = 'date'  # Set 'date' as the name of the index.
        print(self.candles)

    def subscribe(self):
        ws = websocket.WebSocketApp(self.SOCKET,
                                    on_open=self.__on_open__,
                                    on_close=self.__on_close__,
                                    on_message=self.__on_message__)
        ws.run_forever()
