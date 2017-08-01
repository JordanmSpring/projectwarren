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

class keyratios:
    def __init__(self,stock,driver=None,display=None):
        self.stock = stock
        self.driver = driver
        self.display = display
        self.fiver_years_avg_val = None
        self.one_year_avg_val = None
        self.start()
    def start(self):
        try:
            time.sleep(4)
            self.url = r"http://financials.morningstar.com/ratios/r.html?t={0}&region=usa&culture=en-US".format(self.stock.upper())
            log(self.url)
            memory_usage = float(psutil.virtual_memory().__dict__['percent'])
            log("Memory Usage at {0}".format(memory_usage))
            if not self.driver or memory_usage > 60:
                if memory_usage > 60:
                    log("Detected a high memory usage")
                    self.waithelper()
                    time.sleep(35)
                self.accessSelenium(False)
            else:
                log("We have driver already")
                self.accessSelenium(True)
            if self.checkPage():
                time.sleep(2)
                self.getData()
        except Exception as e:
            log(e)
            log(self.stock)
    def accessSelenium(self,flag):
        if flag:
            try:
                wait_seconds = 70
                error_message = "Violated timeout of {0} seconds".format(wait_seconds)
                with setTimeout(seconds = wait_seconds,error_message = error_message):
                    self.driver.get(self.url)
            except Exception as e:
                log(e)
                self.waithelper()
        else:
            selenium_obj = scraperSelenium(self.url,False)
            self.driver,self.display = selenium_obj.scrap()
    def waithelper(self):
        try:
            time.sleep(random.uniform(1,4))
            closetools(self.driver,self.display)
            log("Calling bash function to kill old processes...")
            subprocess.call("./bashkiller.sh", shell=True)
        except Exception as e:
            log(e)
            time.sleep(random.uniform(2,8))
    def checkPage(self):
        loading_page = 0
        self.working_flag = False
        while True:
            log("Number of loads : {0}".format(loading_page))
            try:
                wait_seconds = 50
                error_message = "Violated timeout of {0} seconds".format(wait_seconds)
                with setTimeout(seconds = wait_seconds,error_message = error_message):
                    time.sleep(2)
                    time.sleep(random.uniform(1,3))
                    soup = BeautifulSoup(self.driver.page_source,"html.parser")
                    if len(soup.findAll("table")) > 3:
                        self.working_flag = True
                        break
                    else:
                        log("Something failed on key ratios. Raising the number of Loads ...")
                        loading_page += 1
                        time.sleep(random.uniform(2.5,4.5))
                        if loading_page > 2:
                            waithelper(self.driver,self.display,url)
                            self.accessSelenium(False)
                        if loading_page > 3: 
                            time.sleep(random.uniform(4.5,8.5))
                            self.working_flag = True
                            break
            except Exception as e:
                log(e)
                loading_page += 1
                try:
                    self.driver.get_screenshot_as_file("tmp/" + str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M")) + ".png")
                except Exception as e:
                    log(e)
                time.sleep(random.uniform(3.5,5.5))
                if loading_page > 2:
                    self.waithelper()
                    self.accessSelenium(False)
                    time.sleep(2)
                if loading_page > 4:
                    log("Page Not Working")
                    break
        return self.working_flag
    def getData(self):
        soup = BeautifulSoup(self.driver.page_source,"html.parser")
        tables = soup.findAll("table")
        dfs = []
        for y,table in enumerate(tables):
            try:
                headers = []
                for header in table.find("thead").find_all("th"):
                    if header.text == u"":
                        headers.append(u"Financials")
                    else:
                        headers.append(header.text)
                rows = []
                for body in table.find("tbody").find_all("tr"):
                    lines = []
                    try:
                        row = body.find("th").text
                        lines.append(row)
                        td_lines = body.find_all("td")
                        if td_lines:
                            for item in body.find_all("td"):
                                lines.append(item.text)
                            rows.append(lines)
                        else:
                            while True:
                                if len(lines) == len(headers):
                                    break
                                else:
                                    time.sleep(0.1)
                                    log("looping..")
                                    log(len(lines))
                                    lines.append("--")
                                    if safe_number > 10000:
                                        log("Inside a Loop. Breaking loop...")
                                        log(self.stock)
                                        break
                            rows.append(lines)
                    except Exception as e:
                        pass
                data = {}
                for x,header in enumerate(headers):
                    data[header] = []
                    log("{0} {1}".format(x,header))
                    for row in rows:
                        data[header].append(row[x])
                df = pd.DataFrame()

                for header in data.keys():
                    df[header] = data[header]
                dfs.append(df)
            except Exception as e:
                log(e)
        path = r"/home/ubuntu/pickles/"
        with open(path + self.stock.upper() + ".pickle","w") as f:
            pickle.dump(dfs, f, protocol=pickle.HIGHEST_PROTOCOL)

