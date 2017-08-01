# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/ubuntu/venv/lib/python2.7/site-packages')
from requestsscraper import scraper
from bs4 import BeautifulSoup
import pdfkit
import numpy as np
import datetime,time,random,re
from dbfeeder import updatedb
from seleniumscraper import scraperSelenium,closetools
import signal

VERBOSE = True
LOGGING = False

def log(message):
    if VERBOSE:
        print datetime.datetime.now().strftime('[%d-%m-%y %H:%M:%S] ') + message
    if LOGGING:
        pass

def bonds():
    url = r"http://finance.yahoo.com/bonds/composite_bond_rates?bypass=true"

    page_obj = scraper(url,False)
    page = page_obj.scrap()
    try:
        soup = BeautifulSoup(page)
        corpBonds = soup.findAll('caption', text = re.compile(r'\bCorporate Bonds\b'))[0]
        data = corpBonds.parent.findAll('td', text = re.compile(r'\b20yr AAA\b'))[0].parent
        americanbond = data.findAll("td")[1].text
        log(americanbond)
    except Exception as e:
        log(e)
        americanbond = None
    url = r"http://www.asx.com.au/asx/markets/interestRateSecurityPrices.do"

    page_obj = scraper(url,False)
    page = page_obj.scrap()

    try:
        soup = BeautifulSoup(page)
        data = soup.find("a",{"id":"GSBE47"}).parent.parent
        australianbond = data.findAll("td")[0].text.strip().replace("%","")
        log(australianbond)
    except Exception as e:
        log(e)
        australianbond = None
    return americanbond,australianbond

def main():
    table_obj = updatedb()
    table = "data_bonds"
    columns = """(date, australian_bond, american_bond, scraper_working)"""

    americanbond,australianbond = bonds()
    if americanbond and australianbond:
        working_scraper = "yes"
    else:
        working_scraper = "no"
    if not americanbond:
        americanbond = db_obj.getLastValue("american_bond",table)
    if not australianbond:
        australianbond = db_obj.getLastValue("australian_bond",table)

    log("American bond : {0}, Australian bond : {1}, Working scraper: {2}".format(americanbond,australianbond,working_scraper))
    today = datetime.datetime.now()
    table_obj.update(columns,table,today,australianbond,americanbond,working_scraper)

main()
