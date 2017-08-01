# -*- coding: utf-8 -*-
import sys
import os
sys.path.append('/home/ubuntu/venv/lib/python2.7/site-packages')
from yahoo_finance import Share

def getStock(stock,exchanges_dictionary,data={}):
    try:
        stock = stock.upper()
        stock_obj = Share(stock)
        data["Stock"] = stock
        data["Price"] = stock_obj.get_price()        
        if not data["Price"]:
            data["Price"] = "N/A"
        data["Price Earnings Ratio"] = stock_obj.get_price_earnings_ratio()
        data["Book Value to Price"] = stock_obj.get_price_book()
        data["Price Earnings Growth Ratio"] = stock_obj.get_price_earnings_growth_ratio()
        data["Acquirers Multiple"] = stock_obj.get_ebitda()
        data["Name"] = stock_obj.get_name()
        try:
            code = stock_obj.get_stock_exchange()
            data["Exchange"] = exchanges_dictionary[code]
        except Exception as e:
            data["Exchange"] = None
        data["Error API"] = ""
    except Exception as e:
        data["Error API"] = str(e)
    return data
