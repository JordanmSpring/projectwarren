# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/ubuntu/venv/lib/python2.7/site-packages')
import yahoopage
import yahooapi
import morningstarpage
import morningstarratio
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
from feedLatestStocksData import feedLatestData

VERBOSE = True
LOGGING = False

def log(message):
    message = str(message)
    if VERBOSE:
        print datetime.datetime.now().strftime('[%d-%m-%y %H:%M:%S] ') + message
    if LOGGING:
        pass

starting_point = time.time()
start_date = datetime.datetime.now()
log(start_date)

table_obj = updatedb()
#stocks = ['msft','yhoo']

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

def findStocks():
    stocks = table_obj.getValues("stock","data_stocks_names")
    random.shuffle(stocks)
    stocks = list(set(stocks))
    log("Number of Stocks: {0}".format(len(stocks)))
    return stocks

def updateUnworkingStocks(stock):
    table = "data_unworkingstocks"
    date = datetime.datetime.now()
    columns = "(stock, date)" 
    table_obj.update(columns,table,stock,date)

def main():
    table = "data_stocks"
    columns = """(stock, date, scraperError, scraperApi, bookValue, debtEquitity, priceEarning, operatingCashFlow, 
                  leveredCashFlow, priceEarningGrowth, roic, capitalmarket, freecashflow, freecashflowpercent, 
                  exchange, name, price, dcf_value, safety_margin)"""

    stocks = findStocks()
    #stocks = ['msft','yhoo']#,'rtpjne']
    
    driver = None
    display = None
    
    freezingStocks = []

    exchanges_dictionary = getExchanges()
    
    log("Calling bash function to kill old processes...")
    subprocess.call("/home/ubuntu/crontasks/bashkiller.sh", shell=True)

    for x,stock in enumerate(stocks):
        log("Stock: {0} . Position {1}".format(stock,x))
        try:
            with timeoutLimit(error_message="Reinitiating an unresponsive socket after waiting 8 minutes"):
                today = datetime.datetime.now()
                today_num = int(today.strftime("%j"))
                yesterday_num = today_num - 1
                init_time = time.time()
                time.sleep(random.uniform(2.5,4.2))
                if x % 20 == 0 and x != 0:
                    time.sleep(random.uniform(3.3,15.27))
                    yahoopage.closetools(driver,display)
                    driver = None
                    display = None
                    log("Calling bash function to kill old processes...")
                    subprocess.call("/home/ubuntu/crontasks/bashkiller.sh", shell=True)
                data = yahooapi.getStock(stock,exchanges_dictionary,data={})
                data,driver,display = yahoopage.getStock(stock,driver,display,data=data)
                a_dict = table_obj.getLastValueUsingField(table,"stock",stock)
                if not data["working"]:
                    try:
                        log("Not Working Stock")
                        log(data)
                        updateUnworkingStocks(data["Stock"])
                    except Exception as e:
                        log(e) 
                else:       
                    if a_dict == {} or today_num % 70 == 0 or yesterday_num % 70 == 0:
                        log("Accessing Morningstar")
                        data,driver,display = morningstarpage.getStock(stock,driver,display,data=data)
                        if data["working"]:
                            data,driver,display = morningstarratio.getStock(stock,driver,display,data=data)
                    else:
                        time.sleep(random.uniform(0.5,7.27))
                        try:
                            data['Free Cash Flow'] = a_dict["freecashflow"]
                            data['Free Cash Flow %'] = a_dict["freecashflowpercent"]
                            data['Return on Invested Capital %'] = a_dict["roic"]
                        except Exception as e:
                            log(e)
                            data,driver,display = morningstarpage.getStock(stock,driver,display,data=data)
                            if data["working"]:
                                data,driver,display = morningstarratio.getStock(stock,driver,display,data=data)
                    log(data)
                    memory = psutil.virtual_memory().__dict__
                    log("Memory usage : {0}".format(memory))
                    if float(memory['percent']) > 80:
                        log("Not enough memory")
                    data["Date"] = today.strftime("%Y-%m-%d %H:%M")

                    log(time.time() - init_time)
                    
                    try:
                        guru_table = "data_guru_and_dividends"
                        guru_data = table_obj.getLastValueUsingField(guru_table,"stock",stock)
                    except Exception as e:
                        log(e)
                    try:
                        dcf_val = guru_data['intrinsic_value']
                    except Exception as e:
                        log(e)
                        dcf_val = "N/A"
                    try:
                        safety_margin = guru_data['safety_margin']
                    except Exception as e:
                        log(e)
                        safety_margin = "N/A"

                    try:
                        if data["working"]:
                            table_obj.update(columns,table,data['Stock'],data['Date'],data['Error Scraper'],data['Error API'],
                                             data['Book Value to Price'],data['Debt Equitity Ratio'],data['Price Earnings Ratio'],
                                             data['Operating Cash Flow'],data['Levered Free Cash Flow'],data['Price Earnings Growth Ratio'],
                                             data['Return on Invested Capital %'],data['Market Capitalization'],data['Free Cash Flow'],
                                             data['Free Cash Flow %'],data["Exchange"],data["Name"],data["Price"],dcf_val,safety_margin)
                        else:
                            updateUnworkingStocks(data["Stock"])
                    except Exception as e:
                        log(e)
        except Exception as e:
            time.sleep(random.uniform(1,5))
            log(e)
            log(stock)
            freezingStocks.append(stock)
            try:
                yahoopage.closetools(driver,display)
            except Exception as e:
                log(e)
            driver = None
            display = None
            log("Calling bash function to kill old processes...")
            subprocess.call("/home/ubuntu/crontasks/bashkiller.sh", shell=True)
    yahoopage.closetools(driver,display)

    feedLatestData()

    total_time = time.time() - starting_point
    time_per_query = total_time/float(len(stocks))

    end_date = datetime.datetime.now()
    log("Starting date : {0}".format(start_date))
    log("Ending date : {0}".format(end_date))
    log("There were {0} freezing stocks: {1}".format(len(freezingStocks),freezingStocks))
    log("It took {0} seconds per query and a total of {1} seconds for all queries.".format(time_per_query,total_time))
    log("Done")

main()
