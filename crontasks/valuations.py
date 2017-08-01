from bs4 import BeautifulSoup
import pdfkit
import numpy as np
import datetime,time,random,re
from dbfeeder import updatedb
from seleniumscraper import scraperSelenium,closetools
import signal

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

def getDividend(stock):
    url = r"http://financials.morningstar.com/valuation/price-ratio.html?t={0}&region=usa&culture=en-US".format(stock.upper())
    selenium_obj = scraperSelenium(url,False)
    driver,display = selenium_obj.scrap()
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
                                time.sleep(0.5)
                                print "looping.."
                                print len(lines)
                                lines.append("--")
                        rows.append(lines)
                except Exception as e:
                    pass
            data = {}
            for x,header in enumerate(headers):
                data[header] = []
                print x,header
                for row in rows:
                    data[header].append(row[x])
            df = pd.DataFrame()

            for header in data.keys():
                df[header] = data[header]
            dfs.append(df)
        except Exception as e:
            print e
    for df in dfs:
        try:
            coke_df = df[df['Financials'].str.contains("Dividend Yield")]
        except Exception:
            pass
    five_years_avg_column = stock.upper() + " 5Y Avg*"
    five_years_avg = coke_df[five_years_avg_column].tolist()
    one_year = coke_df[stock.upper()].tolist()
    print five_years_avg[0],one_year[0]
    return five_years_avg[0],one_year[0]
