# -*- coding: utf-8 -*-
import pandas as pd
import datetime
import re,json,time
import pickle

def replacer(x):
    try:
        return float(x.replace("$",""))
    except Exception as e:
        print "We have an error:"
        print e
        print
        return x.replace("$","")

def valuationsModels(dfs_list_pickle,is_file,bs_file,cf_file,ratios,price,market_cap,risk_free,corp_bond):

    with open(dfs_list_pickle,"r") as f:
        dfs_list = pickle.load(f)

    df_is = pd.read_csv(is_file)
    df_bs = pd.read_csv(bs_file)
    df_cf = pd.read_csv(cf_file)


    #P/E Ratio + Growth Rate P/E + Revenue 5YR Growth
    try:
        ratios["5"]["P_E_rat_plus_revenue_gro"] = float(ratios["5"]["Price_Earnings"]) + float(ratios["5"]["Revenue_Growth"])
    except Exception as e:
        print e
        ratios["5"]["P_E_rat_plus_revenue_gro"]  = "N/A"
    try:
        ratios["1"]["P_E_rat_plus_revenue_gro"] = float(ratios["1"]["Price_Earnings"]) + float(ratios["1"]["Revenue_Growth"])
    except Exception:
        ratios["1"]["P_E_rat_plus_revenue_gro"] = "N/A"

    try:
        intrisic_val = float(ratios["5"]["Earnings_Per_Share"]) + float(ratios["5"]["P_E_rat_plus_revenue_gro"]) + float(risk_free)
        ratios["5"]["Intrinsic_Value"] = intrisic_val/float(corp_bond)
    except Exception as e:
        print e
        ratios["5"]["Intrinsic_Value"]  = "N/A"

    try:
        ratios["5"]["Current_Margin_of_Safety"] = float(price)/ratios["5"]["Intrinsic_Value"]
    except Exception as e:
        print e
        ratios["5"]["Current_Margin_of_Safety"]  = "N/A"

    return ratios
