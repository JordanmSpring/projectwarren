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

table = "data_stocks"

stocks = ['msft']

table_obj = updatedb()

for x,stock in enumerate(stocks):
    init_time = time.time()
    time.sleep(random.uniform(0.5,5.2))
    if x % 10 == 0 and x != 0:
        time.sleep(random.uniform(3.3,6.27))
        yahoopage.closetools(driver,display)
        driver = None
        display = None
    print stock
    data = {}
    dicts_list = table_obj.getLastValueUsingField(table,"stock",stock)
    print dicts_list
    print dicts_list["freecashflow"]
    print dicts_list["freecashflowpercent"]
    print dicts_list["roic"]

