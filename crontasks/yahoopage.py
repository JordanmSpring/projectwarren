# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/ubuntu/flask/flaskapp/lib/python2.7/site-packages')
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
        time.sleep(random.uniform(2.2,12.57))
        driver.get(url)
        time.sleep(5)
    except Exception as e:
        log(e)
        time.sleep(random.uniform(1.2,3.57))
        closetools(driver,display)
        selenium_obj = scraperSelenium(url,False)
        driver,display = selenium_obj.scrap()
    return driver,display

def marketCap(value):
    if "B" in value or "b" in value:
        value = float(value.replace("B","").replace("b",""))*1000000000
    elif "M" in value or "m" in value:
        value = float(value.replace("M","").replace("m",""))*1000000
    elif "K" in value or "k" in value:
        value = float(value.replace("K","").replace("k",""))*1000
    else:
        value = float(value)
    return value
        
def getStock(stock,driver,display,data={}):
    try:
        error = ""
        data["working"] = True
        capitalmarket = []
        debtequitity = []
        opercashflow = []
        levercashflow = []
        
        priceearningratio = []
        bookvaluetoprice = []
        priceearninggrowthratio = []
        acquirersmultiple = []
        
        #regex = r'\(end\)">(.+?)</td>'
        regex = r'\(end\)" data-reactid="\d+">(.+?)</td>'
        pattern = re.compile(regex)
        stock = stock.lower()
        url = r"https://finance.yahoo.com/quote/{0}/key-statistics?ltr=1".format(stock)
        memory_usage = float(psutil.virtual_memory().__dict__['percent'])
        if not driver or memory_usage > 60:
            if memory_usage > 60:
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
                if "No results for" in soup.find("div",{"id":"Main"}).text:
                    data["working"] = False
                    break
                soup_data = soup.find("div",{"data-test":"qsp-statistics"})
                if len(soup_data(text=re.compile(r'Levered Free Cash Flow'))) > 0:
                    break
                else:
                    loading_page += 1
                    time.sleep(random.uniform(1.2,2.57))
                    if loading_page > 2:
                        driver,display = waithelper(driver,display,url)

                    if loading_page > 3: 
                        log("Page Not Working")
                        error += "Not Working. "
                        data["working"] = False
                        data["Error Scraper"] = error
                        break
            except Exception as e:
                log(e)
                loading_page += 1
                try:
                    driver.get_screenshot_as_file("tmp/" + str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M")) + ".png")
                except Exception as e:
                    log(e)
                time.sleep(random.uniform(1.2,2.57))
                if loading_page > 2:
                    driver,display = waithelper(driver,display,url)
                if loading_page > 3:
                    log("Page Not Working")
                    error += "Not Working. "
                    data["working"] = False
                    data["Error Scraper"] = error
                    break
        if data["working"]:
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source,"html.parser")
            soup_data = soup.find("div",{"data-test":"qsp-statistics"})
            for elem in soup_data(text=re.compile(r'Market Cap')):
                capitalmarket.append(elem.parent.parent.parent)
            for elem in soup_data(text=re.compile(r'Total Debt/Equity')):
                debtequitity.append(elem.parent.parent.parent)
            for elem in soup_data(text=re.compile(r'Operating Cash Flow')):
                opercashflow.append(elem.parent.parent.parent)
            for elem in soup_data(text=re.compile(r'Levered Free Cash Flow')):
                levercashflow.append(elem.parent.parent.parent)

            for elem in soup_data(text=re.compile(r'Trailing P/E')):
                priceearningratio.append(elem.parent.parent.parent)
            for elem in soup_data(text=re.compile(r'Price/Book')):
                bookvaluetoprice.append(elem.parent.parent.parent)
            for elem in soup_data(text=re.compile(r'PEG Ratio')):
                priceearninggrowthratio.append(elem.parent.parent.parent)
            for elem in soup_data(text=re.compile(r'EBITDA')):
                if "Enterprise Value/EBITDA" not in str(elem.parent.parent.parent):
                    acquirersmultiple.append(elem.parent.parent.parent)
            try:
                data["Market Capitalization"] = marketCap(re.findall(pattern,str(capitalmarket[0]))[0]) 
            except Exception as e:
                data["Market Capitalization"] = "N/A"
                error += str(e)
            try:
                DebtEquitityRatio = re.findall(pattern,str(debtequitity[0]))[0]
                if "N/A" in DebtEquitityRatio:
                    data["Debt Equitity Ratio"] = "N/A"
                else:
                    data["Debt Equitity Ratio"] = DebtEquitityRatio 
            except Exception as e:
                data["Debt Equitity Ratio"] = "N/A"
                error += str(e)
            try:
                OperativeCashFlow = re.findall(pattern,str(opercashflow[0]))[0]
                if "N/A" in OperativeCashFlow:
                    data["Operating Cash Flow"] = "N/A"
                else:
                    data["Operating Cash Flow"] = OperativeCashFlow 
            except Exception as e:
                data["Operating Cash Flow"] = "N/A"
                error += str(e)     
            try:
                LeveredFreeCashFlow = re.findall(pattern,str(levercashflow[0]))[0]
                if "N/A" in LeveredFreeCashFlow:
                    data["Levered Free Cash Flow"] = "N/A"
                else:
                    data["Levered Free Cash Flow"] = LeveredFreeCashFlow 
            except Exception as e:
                data["Levered Free Cash Flow"] = "N/A"
                error += str(e)     

            if not data["Price Earnings Ratio"]:
                try:
                    PriceEarningsRatio = re.findall(pattern,str(priceearningratio[0]))[0]
                    if "N/A" in PriceEarningsRatio:
                        data["Price Earnings Ratio"] = "N/A"
                    else:
                        data["Price Earnings Ratio"] = PriceEarningsRatio
                except Exception as e:
                    data["Price Earnings Ratio"] = "N/A"
                    error += str(e)  
            if not data["Book Value to Price"]:
                try:
                    BookValuePrice = re.findall(pattern,str(bookvaluetoprice[0]))[0]
                    if "N/A" in BookValuePrice:
                        data["Book Value to Price"] = "N/A"
                    else:
                        data["Book Value to Price"] = BookValuePrice 
                except Exception as e:
                    data["Book Value to Price"] = "N/A"
                    error += str(e) 
            if not data["Price Earnings Growth Ratio"]:
                try:
                    PriceEarningsGrowthRatio = re.findall(pattern,str(priceearninggrowthratio[0]))[0]
                    if "N/A" in PriceEarningsGrowthRatio:
                        data["Price Earnings Growth Ratio"] = "N/A"
                    else:
                        data["Price Earnings Growth Ratio"] =  PriceEarningsGrowthRatio
                except Exception as e:
                    data["Price Earnings Growth Ratio"] = "N/A"
                    error += str(e) 
            if not data["Acquirers Multiple"]:
                try:
                    data["Acquirers Multiple"] = re.findall(pattern,str(acquirersmultiple[0]))[0] 
                except Exception as e:
                    data["Acquirers Multiple"] = "N/A"
                    error += str(e) 
            if not data["Name"]:
                soup_name = soup.find("div",{"id":"quote-header-info"})
                try:
                    name_ptn = r"\((\w+)\)"
                    name = soup_name.find("h1",{"class":"D(ib)"}).text
                    stock_ctn = re.findall(name_ptn,name)
                    if len(stock_ctn) > 0:
                        stock_ctn = "("+str(stock_ctn[0])+")"
                        name = name.replace(stock_ctn,"").strip()
                    data["Name"] = name
                except Exception as e:
                    data["Name"] = "N/A"
            if not data["Exchange"]:
                soup_exchange = soup.find("div",{"id":"quote-header-info"})
                try:
                    exchange = soup_exchange.find("span",{"class":"C($finDarkGray)"}).text.split("-")[0]
                    data["Exchange"] = exchange.replace("Currency in USD","").replace(" . ","")
                except Exception as e:
                    data["Exchange"] = "N/A"
            data["Error Scraper"] = error

    except Exception as e:
        error += str(e)
        data["working"] = False
        data["Error Scraper"] = error 
        #closetools(driver,display)
    return data,driver,display
