# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/ubuntu/venv/lib/python2.7/site-packages')
from dbfeeder import updatedb
import datetime

obj_db = updatedb()

def remove(stock):
    try:
        print "Removing the stock {0}".format(stock)
        table = "data_stocks_names"
        obj_db.deleteRecord(table,"stock",stock)
    except Exception as e:
        print e

def banned(stock):
    try:
        print "Banning the stock {0}".format(stock)
        table = "data_bannedstocks"
        date = datetime.datetime.now()
        columns = "(stock, date)"
        obj_db.update(columns,table,stock,date)
    except Exception as e:
        print e

def main():
    table = "data_unworkingstocks"
    data = obj_db.getAllValues(table)
   
    stocks = [item[1] for item in data]

    unique_stocks = list(set(stocks))

    for stock in unique_stocks:
        try:
            stocks_data = obj_db.getAllValuesUsingField(table,"stock",stock)
            if len(stocks_data) > 4:
                stocks_data = stocks_data[-5:]
                dates = [item["date"] for item in stocks_data]
                dif = dates[0] - dates[4]
                if abs(dif.days) < 16:
                    print
                    banned(stock)
                    remove(stock)
        except Exception as e:
            print e
main()
