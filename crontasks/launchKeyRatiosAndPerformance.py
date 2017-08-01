# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/ubuntu/venv/lib/python2.7/site-packages')
import pandas as pd
from bs4 import BeautifulSoup
import pdfkit
import numpy as np
import datetime,time,random,re
from dbfeeder import updatedb
from chromeseleniumscraper import scraperSelenium,closetools
import signal
import psutil
import pickle
from keyRatiosScraper import keyratios
from performanceScraper import performance
import subprocess

VERBOSE = True
LOGGING = False

def log(message):
    message = str(message)
    if VERBOSE:
        print datetime.datetime.now().strftime('[%d-%m-%y %H:%M:%S] ') + message
    if LOGGING:
        pass

class setTimeout:
    def __init__(self,seconds = 4, error_message = "Timeout"):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self,signum,frame):
        raise Exception(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM,self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self,type,value,traceback):
        signal.alarm(0)

def findStocks():
    table_obj = updatedb()
    stocks = table_obj.getValues("stock","data_stocks_names")
    stocks = sorted(stocks, key=lambda *args: random.random())
    stocks = list(set(stocks))
    log("Number of Stocks: {0}".format(len(stocks)))
    return stocks

def main(stocks):

    starting_point = time.time()
    start_date = datetime.datetime.now()
    log("Starting Date : {0}".format(start_date))
    for x,stock in enumerate(stocks):
        log("Stock: {0} . Position {1}".format(stock,x))
        wait_seconds = 480
        error_message = "Violated timeout of {0} seconds".format(wait_seconds)
        try:
            with setTimeout(seconds = wait_seconds,error_message = error_message):
                today = datetime.datetime.now()
                log("Time: {0}".format(today))
                if x % 3 == 0:
                    driver = None
                    display = None
                    log("Calling bash function to kill old processes...")
                    subprocess.call("/home/ubuntu/crontasks/bashkiller.sh", shell=True)
                perf_obj = performance(stock,driver = driver, display = display)
                try:
                    driver = perf_obj.driver
                    display = perf_obj.display
                except Exception as e:
                    log(e)
                    driver = None
                    display = None
                keyr_obj = keyratios(stock,driver = driver, display = display)
                try:
                    driver = keyr_obj.driver
                    display = keyr_obj.display
                except Exception as e:
                    log(e)
                    driver = None
                    display = None
        except Exception as e:
            log(e)
            closetools(driver,display)
            driver = None
            display = None
            log("Calling bash function to kill old processes...")
            subprocess.call("./bashkiller.sh", shell=True)
    closetools(driver,display)
    log("Starting Date: {0}".format(start_date))
    log("Scraper ran {0} stocks".format(len(stocks)))
    log("It took {0} seconds".format(time.time()-starting_point))
    log("It took {0} seconds per stock".format(float(time.time()-starting_point)/len(stocks)))

#stocks = findStocks()
#stocks = ["MSFT","ARI","AAPL","BTX"]
#main(stocks)
