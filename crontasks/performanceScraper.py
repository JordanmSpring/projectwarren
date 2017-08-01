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
     
class performance:
    def __init__(self,stock,driver=None,display=None):
        self.stock = stock
        self.driver = driver
        self.display = display
        self.path = "/home/ubuntu/docs/"
        self.working_flag = False
        self.links = {"Income Statement":"http://financials.morningstar.com/income-statement/is.html?t=",
                      "Balance Sheet":"http://financials.morningstar.com/balance-sheet/bs.html?t=",
                      "Cash Flow":"http://financials.morningstar.com/cash-flow/cf.html?t="}
        self.start()
    def start(self):
        for key in self.links.keys():
            try:
                time.sleep(4)
                self.url = self.links[key] + self.stock.upper()
                log(self.url)
                self.key = key
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
                self.waithelper()
                log("Performance : {0} . Stock : {1}".format(key,self.stock))
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
                    if len(soup.select(".lbl")) > 5:
                        self.working_flag = True
                        break
                    else:
                        log("Less than 5 div with 'lbl' classes")
                        loading_page += 1
                        time.sleep(random.uniform(2.5,4.5))
                        if loading_page > 2:
                            self.waithelper()
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
                    log("Not Working")
                    break
        return self.working_flag
    def getData(self):
        try:
            soup = BeautifulSoup(self.driver.page_source,"html.parser")
            left = soup.find("div",{"class":"left"})
            main = soup.find("div",{"class":"main"})
            left_fields = left.select("div[id*=label]")
            main_fields = main.select("div[id*=data]")

            headers_soup = soup.find("div",{"class":"main"}).find("div",{"class":"rf_header"}).select("div[id*=Y]")
            headers = [item.text for item in headers_soup]

            self.headers_dictionary = {}
            for header in headers:
                self.headers_dictionary[header] = []

            log("Left field size : {0}. Main field size : {1}".format(len(left_fields),len(main_fields)))
            log("Headers : {0}".format(headers))

            lines = []
            errors = []

            for item in left_fields:
                ctn = item.find("div",{"class":"lbl"})
                try:
                    lines.append(ctn["title"])
                except Exception as e:
                    lines.append(item.text)

            for line,item in zip(lines,main_fields):
                divs = item.select("div[id*=Y]")
                if "style" not in item.attrs:
                    if len(divs) > 0:
                        for header,ctn in zip(headers,divs):
                            try:
                                rawvalue = ctn["rawvalue"]
                                if rawvalue == "nbsp":
                                    self.headers_dictionary[header].append("")
                                else:
                                    self.headers_dictionary[header].append("$"+str(int(ctn["rawvalue"])))
                            except Exception as e:
                                try:
                                    self.headers_dictionary[header].append(str(float(ctn["rawvalue"])))
                                except Exception as e:
                                    errors.append((e,header,ctn,line))
                                    self.headers_dictionary[header].append("N/A")
                    else:
                        for header in headers:
                            self.headers_dictionary[header].append("")            
                else:
                    for header in headers:
                        self.headers_dictionary[header].append("")

            self.headers_dictionary["USD IN MILLIONS"] = lines
            self.getDfAndPdf()
        except Exception as e:
            log(e)
    def getDfAndPdf(self):
        try:
            for key in self.headers_dictionary.keys():
                log(key)
                log(len(self.headers_dictionary[key]))
            
            df = pd.DataFrame.from_dict(self.headers_dictionary)

            columns = df.columns.tolist()
            columns_list = [""]*len(columns)
            columns_list[0] = columns[-1]
            columns_list[1:] = columns[0:-1]

            df = df[columns_list]
            df = df.replace(np.nan,'--', regex=True)
            df = df.fillna('******')
            log(df.shape)
            
            initials = "".join(item[0] for item in self.key.split())
            csv_name = self.path + initials + "/" + self.stock + " " + initials + ".csv"
            log(csv_name)
            df.to_csv(csv_name,encoding="utf-8")
            df_html = df.to_html(index=False)

            style = """<style>
            table {
                border-collapse: collapse;
                width: 100%;
            }

            th, td {
                text-align: left;
                padding: 8px;
            }

            tr:nth-child(even){background-color: #f2f2f2}
            </style>"""

            header = "<h2>{0}</h2></br>".format(self.key)

            final_df_html = style + header + str(df_html)
            pdf_name = self.path + initials + "/" + self.stock + " " + initials + ".pdf"
            log(pdf_name)
            pdfkit.from_string(str(final_df_html), pdf_name)
        except Exception as e:
            log(e)

