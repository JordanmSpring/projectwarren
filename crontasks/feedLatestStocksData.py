# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/ubuntu/venv/lib/python2.7/site-packages')
import random
import time
from dbfeeder import updatedb
import datetime
import psutil
import signal
import os
import pandas as pd
import subprocess
import signal

VERBOSE = True
LOGGING = False

def log(message):
    try:
        message = str(message)
        if VERBOSE:
            print datetime.datetime.now().strftime('[%d-%m-%y %H:%M:%S] ') + message
        if LOGGING:
            pass
    except Exception:
        pass

class timeoutLimit:
    def __init__(self,seconds = 8*60, error_message = "Timeout"):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self,signum,frame):
        raise Exception(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM,self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self,type,value,traceback):
        signal.alarm(0)

def getExchanges():
    path = os.path.dirname(os.path.abspath(__file__)) + "/exchanges.csv"
    exchanges_dict = {}
    df = pd.read_csv(path)
    for code,exchange in zip(df["code"],df["exchange"]):
        exchanges_dict[code] = exchange
    return exchanges_dict

def findStocks(table_obj):
    stocks = table_obj.getValues("stock","data_stocks_names")
    random.shuffle(stocks)
    stocks = list(set(stocks))
    log("Number of Stocks: {0}".format(len(stocks)))
    return stocks

#stocks = ['msft','yhoo']

def feedLatestData():
    log("Starting feeding latest data from stocks...")
    table_obj = updatedb()
    stocks = findStocks(table_obj)
    for stock in stocks:
        try:
            #(self,table,column,value)
            table_obj.deleteRecord("data_stockslastdata","stock",stock)
        except Exception as e:
            log(e)
        try:
            data=table_obj.getLastValueUsingField("data_stocks","stock",stock)
            if data:
                columns = data.keys()
                values = data.values()
                table_obj.update("(" + ", ".join(columns) + ")","data_stockslastdata",*values)        
        
        except Exception as e:
            log(e)
            log(stock)

    log("All stocks uploaded on the table Latest Stocks Data")
