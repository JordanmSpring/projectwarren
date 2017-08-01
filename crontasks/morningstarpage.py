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

VERBOSE = True
LOGGING = False

def log(message):
    message = str(message)
    if VERBOSE:
        print datetime.datetime.now().strftime('[%d-%m-%y %H:%M:%S] ') + message
    if LOGGING:
        pass

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

def freeCashFlow(value):
    return float(value.replace(",",""))*1000000

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
        url = r"http://financials.morningstar.com/cash-flow/cf.html?t={0}&region=usa&culture=en-US".format(stock)
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
                if "This page is temporarily unavailable" in soup.text:
                    data["working"] = False
                    break
                else:
                    soup_data = soup.findAll("div",{"class":"rf_crow"})[-1]
                    if len(soup_data.select("div[class*=column]")) > 0:
                        break
                    else:
                        loading_page += 1
                        time.sleep(random.uniform(1.2,2.57))
                        if loading_page > 2:
                            driver,display = waithelper(driver,display,url)
                        if loading_page > 4: 
                            log("Page Not Working")
                            error += "Not Working. "
                            data["Error Scraper"] = error
                            data["working"] = False
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
                    log("Page Not Working")
                    error += "Not Working. "
                    data["Error Scraper"] = error
                    data["working"] = False
                    break
        if data["working"]:
            try:
                time.sleep(1)
                soup = BeautifulSoup(driver.page_source,"html.parser")
                first_column = soup.find("div",{"class":"left"}).select("div[class*=rf_]")
                second_column = soup.find("div",{"class":"scrollWrapper"}).select("div[class*=rf_]")
                numbers = []
                free_cash_flows_list = []
                for x,elem in enumerate(first_column):
                    new_data = elem(text=re.compile(r'Free cash flow'))
                    if len(new_data) > 0:
                        try:
                            numbers.append(x)
                        except Exception as e:
                            pass

                for number in numbers:
                    soup_cash_flow = second_column[number]
                    free_cash_flows_list.append(soup_cash_flow.select("div[class*=column]")[-2].text)

            except Exception as e:
                error += str(e)
                data["working"] = False
            try:
                data["Free Cash Flow"] = freeCashFlow(re.sub(r"[^\d]+","",free_cash_flows_list[-1]))
                log(data["Free Cash Flow"])
            except Exception as e:
                data["Free Cash Flow"] = "N/A"
                error += str(e)
            try:
                percentualFlow = 100*float(data["Free Cash Flow"])/float(data["Market Capitalization"])
                percentualFlow = str(round(percentualFlow,2)) + "%"
                log(percentualFlow)
                data["Free Cash Flow %"] = percentualFlow
            except Exception as e:
                data["Free Cash Flow %"] = "N/A"
                error += str(e)

            data["Error Scraper"] = error
    except Exception as e:
        error += str(e)
        data["Error Scraper"] = error 
        data["working"] = False
    return data,driver,display
