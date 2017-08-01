# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/ubuntu/venv/lib/python2.7/site-packages')
#from seleniumscraper import scraperSelenium
from chromeseleniumscraper import scraperSelenium
import re
from bs4 import BeautifulSoup
import time,random
import datetime
import psutil
import pickle
import pandas as pd

VERBOSE = True
LOGGING = False

def log(message):
    message = str(message)
    if VERBOSE:
        print datetime.datetime.now().strftime('[%d-%m-%y %H:%M:%S] ') + message
    if LOGGING:
        pass

def getData(soup,stock):
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
                            #print item.text
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
                        rows.append(lines)
                except Exception as e:
                    pass
            data = {}
            for x,header in enumerate(headers):
                data[header] = []
                log("Position {0}, Header {1}".format(x,header))
                for row in rows:
                    data[header].append(row[x])
            df = pd.DataFrame()

            for header in data.keys():
                df[header] = data[header]
            dfs.append(df)
        except Exception as e:
            log(e)
    path = r"/home/ubuntu/pickles/"
    with open(path + stock.upper() + ".pickle","w") as f:
        pickle.dump(dfs, f, protocol=pickle.HIGHEST_PROTOCOL)

def closetools(driver,display):
    try:
        log("closing Phantomjs")
        driver.quit()
        driver.close()
    except Exception as e:
        log(e)
    try:
        log("Closing Display")
        display.stop()
    except Exception as e:
        log(e)    

def waithelper(driver,display,url):
    try:
        time.sleep(random.uniform(5.2,12.57))
        driver.get(url)
        time.sleep(5)
    except Exception as e:
        log(e)
        time.sleep(random.uniform(2.2,4.57))
        closetools(driver,display)
        selenium_obj = scraperSelenium(url,False)
        driver,display = selenium_obj.scrap()
    return driver,display

def getStock(stock,driver,display,data={}):
    try:
        error = data["Error Scraper"]
        
        capitalmarket = []
        debtequitity = []
        opercashflow = []
        levercashflow = []
        
        priceearningratio = []
        bookvaluetoprice = []
        priceearninggrowthratio = []
        acquirersmultiple = []
        
        regex = r'\(end\)">(.+?)</td>'
        pattern = re.compile(regex)
        stock = stock.upper()
        url = r"http://financials.morningstar.com/ratios/r.html?t={0}&region=usa&culture=en-US".format(stock)
        memory_usage = float(psutil.virtual_memory().__dict__['percent'])
        if not driver or memory_usage > 70:
            log("Consuming too much memory")
            try:
                closetools(driver,display)
            except Exception as e:
                log(e)
            selenium_obj = scraperSelenium(url,False)
            driver,display = selenium_obj.scrap()
        else:
            driver.get(url)
        loading_page = 0
        while True:
            try:
                time.sleep(1)
                soup = BeautifulSoup(driver.page_source,"html.parser")
                if len(soup.find("div",{"id":"tab-profitability"})(text=re.compile(r'Return on Invested Capital'))) > 0:
                    break
                else:
                    loading_page += 1
                    time.sleep(random.uniform(1.2,2.57))
                    if loading_page > 2:
                        driver,display = waithelper(driver,display,url)
                    if loading_page > 4: 
                        log("Not Working")
                        error += "Not Working. "
                        data["Error Scraper"] = error
                        break
            except Exception as e:
                log(e)
                loading_page += 1
                try:
                    driver.get_screenshot_as_file("tmp/" + str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M")) + ".png")
                except Exception as e:
                    log(e)
                time.sleep(random.uniform(3.2,4.57))
                if loading_page > 2:
                    driver,display = waithelper(driver,display,url)
                if loading_page > 4:
                    log("Not Working")
                    error += "Not Working. "
                    data["Error Scraper"] = error
                    break
        try:
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source,"html.parser")
            roics = []
            for elem in soup.find("div",{"id":"tab-profitability"})(text=re.compile(r'Return on Invested Capital')):
                roics.append(elem.parent.parent)
        
        except Exception as e:
            error += str(e)
        try:
            data["Return on Invested Capital %"] = roics[0].findAll("td")[-2].text#soup_data.select("div[class*=column]")[-1].text
        except Exception as e:
            data["Return on Invested Capital %"] = "N/A"
            error += str(e)

        #try:
        #    time.sleep(2)
        #    soup = BeautifulSoup(driver.page_source,"html.parser")
        #    getData(soup,stock)
        #except Exception as e:
        #    print e

    except Exception as e:
        error += str(e)
        data["Error Scraper"] = error 
    return data,driver,display
