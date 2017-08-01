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
from guruScraper import guru
from valuationsScraper import valuations
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
    table = "data_guru_and_dividends"
    columns = """(stock, date, cost_of_capital, dividend, dividend_five_years,intrinsic_value,safety_margin)"""
    table_obj = updatedb()

    starting_point = time.time()
    start_date = datetime.datetime.now()
  
    driver = None
    display = None
    log("Starting Date : {0}".format(start_date))
    log("Calling bash function to kill old processes...")
    subprocess.call("/home/ubuntu/crontasks/bashkiller.sh", shell=True)

    for x,stock in enumerate(stocks):
        log("Stock: {0} . Position {1}".format(stock,x))
        wait_seconds = 360
        error_message = "Violated timeout of {0} seconds".format(wait_seconds)
        try:
            with setTimeout(seconds = wait_seconds,error_message = error_message):
                today = datetime.datetime.now()
                log("Time: {0}".format(today))
                if x % 4 == 0 and x != 0:
                    closetools(driver,display)
                    time.sleep(5)
                    driver = None
                    display = None
                    log("Calling bash function to kill old processes...")
                    subprocess.call("/home/ubuntu/crontasks/bashkiller.sh", shell=True)
                try:
                    valu_obj = valuations(stock,driver = driver, display = display)

                except Exception as e:
                    time.sleep(2)
                    log(e)
                        
                    closetools(driver,display)
                    driver = None
                    display = None
                try:
                    if valu_obj.fiver_years_avg_val:
                        fiver_years_avg_val = valu_obj.fiver_years_avg_val
                    else:
                        fiver_years_avg_val = "N/A"
                except Exception as e:
                    fiver_years_avg_val = "N/A"
                try:
                    if valu_obj.one_year_avg_val:
                        one_year_avg_val = valu_obj.one_year_avg_val
                    else:
                        one_year_avg_val = "N/A"
                except Exception as e:
                    one_year_avg_val = "N/A"
                try:
                    driver = valu_obj.driver
                    display = valu_obj.display
                except Exception as e:
                    log(e)
                    closetools(driver,display)
                    driver = None
                    display = None

                url = r"http://www.gurufocus.com/term/wacc/{0}/Weighted-Average-Cost-Of-Capital-WACC/".format(stock.upper())
                guru_obj = None
                try:
                    guru_obj = guru(stock,url,driver = driver, display = display)

                except Exception as e:
                    time.sleep(2)
                    log(e)
                    closetools(driver,display)
                    driver = None
                    display = None
                try:
                    if guru_obj.main_val:
                        capital_cost_val = guru_obj.main_val
                    else:
                        capital_cost_val = "N/A"
                except Exception as e:
                    capital_cost_val = "N/A"
                try:
                    driver = guru_obj.driver
                    display = guru_obj.display
                except Exception as e:
                    log(e)
                    closetools(driver,display)
                    driver = None
                    display = None

                url = r"http://www.gurufocus.com/term/Intrinsic+Value+(DCF)/{0}/Intrinsic%2BValue%2B%2528DCF%2529/".format(stock.upper())
                guru_obj = None
                try:
                    guru_obj = guru(stock,url,driver = driver, display = display)

                except Exception as e:
                    time.sleep(2)
                    log(e)
                    closetools(driver,display)
                    driver = None
                    display = None
                try:
                    if guru_obj.main_val:
                        intrinsic_value_val = guru_obj.main_val
                    else:
                        intrinsic_value_val = "N/A"
                except Exception as e:
                    intrinsic_value_val = "N/A"
                try:
                    if guru_obj.safety_margin:
                        safety_margin_val = guru_obj.safety_margin
                    else:
                        safety_margin_val = "N/A"
                except Exception as e:
                    safety_margin_val = "N/A"
                try:
                    driver = guru_obj.driver
                    display = guru_obj.display
                except Exception as e:
                    log(e)
                    closetools(driver,display)
                    driver = None
                    display = None
                try:
                    table_obj.update(columns,table,stock,today.strftime("%Y-%m-%d %H:%M"),
                                     capital_cost_val,one_year_avg_val,fiver_years_avg_val,
                                     intrinsic_value_val,safety_margin_val)

                except Exception as e:
                    log(e)
        except Exception as e:
            log(e)
            closetools(driver,display)
            driver = None
            display = None
            log("Calling bash function to kill old processes...")
            subprocess.call("/home/ubuntu/crontasks/bashkiller.sh", shell=True)
    closetools(driver,display)
    log("Starting Date: {0}".format(start_date))
    log("Scraper ran {0} stocks".format(len(stocks)))
    log("It took {0} seconds".format(time.time()-starting_point))
    log("It took {0} seconds per stock".format(float(time.time()-starting_point)/len(stocks)))

stocks = findStocks()
#stocks = ["AAPL","BTX"]
main(stocks)
log("Done.")
