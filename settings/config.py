import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get('API_KEY')
        self.secret_key = os.environ.get('SECRET_KEY')
        self.SOCKET = 'wss://fstream.binance.com/ws/btcusdt@kline_1m'
