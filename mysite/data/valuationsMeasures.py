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

def valuationsData(dfs_list_pickle,is_file,bs_file,cf_file,ratios,price,market_cap):

    with open(dfs_list_pickle,"r") as f:
        dfs_list = pickle.load(f)

    df_is = pd.read_csv(is_file)
    df_bs = pd.read_csv(bs_file)
    df_cf = pd.read_csv(cf_file)

    print df_is.shape, df_bs.shape, df_cf.shape
    for df in dfs_list:
        try:
            try:
                #df[(df['Financials'].str.contains("Free Cash Flow",case=False))&(df['Financials'].str.contains("USD Mil",case=False))]
                EarningsPerShare = df[(df['Financials'].str.contains("Book Value Per Share",case=False)) &
                                      (df['Financials'].str.contains("USD",case=False))]
                if EarningsPerShare.any:
                    dates = []

                    for column in EarningsPerShare:
                        try:
                            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
                        except Exception:
                            pass   
                    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
                    earnings_per_shares = []
                    for date in dates:
                        earnings_per_share_val = EarningsPerShare[date[1]].tolist()[0].replace(",",".")
                        earnings_per_shares.append(earnings_per_share_val)
                    if len(earnings_per_shares) == 5:
                        try:
                            ratios["5"]["Price_Book"] = sum(float(val) for val in earnings_per_shares)/5.0
                        except Exception:
                            ratios["5"]["Price_Book"] = "N/A"
                    try:
                        ratios["1"]["Price_Book"] = float(earnings_per_shares[0])
                    except Exception:
                        ratios["1"]["Price_Book"] = "N/A"
            except Exception:
                pass
        except Exception:
            pass

    try:
        ratios["1"]["Price"] = float(price)
    except Exception as e:
        print e
        ratios["1"]["Price"] = "N/A"
    try:
        ratios["1"]["Market Cap"] = float(market_cap)
    except Exception:
        ratios["1"]["Market Cap"] = "N/A"

    try:
        ratios["5"]["Price_Working"] = ratios["1"]["Market Cap"] / ratios["5"]["working_capital"]
    except Exception as e:
        print e
        ratios["5"]["Price_Working"]  = "N/A"
    try:
        ratios["1"]["Price_Working"] = ratios["1"]["Market Cap"] / ratios["1"]["working_capital"]
    except Exception:
        ratios["1"]["Price_Working"] = "N/A"

    try:
        ratios["5"]["Price_Liquidation"] = ratios["1"]["Price"] / ratios["5"]["Liquidation_Val"]
    except Exception as e:
        print e
        ratios["5"]["Price_Liquidation"]  = "N/A"
    try:
        ratios["1"]["Price_Liquidation"] = ratios["1"]["Price"] / ratios["1"]["Liquidation_Val"]
    except Exception:
        ratios["1"]["Price_Liquidation"] = "N/A"

    try:
        ratios["5"]["Price_Current_Assets"] = ratios["1"]["Price"] / ratios["5"]["total_current_assets"]
    except Exception as e:
        print e
        ratios["5"]["Price_Current_Assets"]  = "N/A"
    try:
        ratios["1"]["Price_Current_Assets"] = ratios["1"]["Price"] / ratios["1"]["total_current_assets"]
    except Exception:
        ratios["1"]["Price_Current_Assets"] = "N/A"

    #Total Cash in CF or BS?
    try:
        ratios["5"]["Price_Cash_Assets"] = ratios["1"]["Price"] / ratios["5"]["total cash CF"]
    except Exception as e:
        print e
        ratios["5"]["Price_Cash_Assets"]  = "N/A"
    try:
        ratios["1"]["Price_Cash_Assets"] = ratios["1"]["Price"] / ratios["1"]["total cash CF"]
    except Exception:
        ratios["1"]["Price_Cash_Assets"] = "N/A"

    try:
        ratios["5"]["Price_Earnings"] = ratios["1"]["Price"] / ratios["5"]["Earnings Per Share"]
    except Exception as e:
        print e
        ratios["5"]["Price_Earnings"]  = "N/A"
    try:
        ratios["1"]["Price_Earnings"] = ratios["1"]["Price"] / ratios["1"]["Earnings Per Share"]
    except Exception:
        ratios["1"]["Price_Earnings"] = "N/A"

    try:
        ratios["5"]["Price_Sales"] = ratios["1"]["Price"] / ratios["5"]["revenue"]
    except Exception as e:
        print e
        ratios["5"]["Price_Sales"]  = "N/A"
    try:
        ratios["1"]["Price_Sales"] = ratios["1"]["Price"] / ratios["1"]["revenue"]
    except Exception:
        ratios["1"]["Price_Sales"] = "N/A"

    try:
        ratios["5"]["Price_Debt"] = ratios["1"]["Market Cap"] / ratios["5"]["Total_Debt"]
    except Exception as e:
        print e
        ratios["5"]["Price_Debt"]  = "N/A"
    try:
        ratios["1"]["Price_Debt"] = ratios["1"]["Market Cap"] / ratios["1"]["Total_Debt"]
    except Exception:
        ratios["1"]["Price_Debt"] = "N/A"

    #Free Cash Flow at CF
    dates = []
    free_cash_flow_df = df_cf[df_cf['USD IN MILLIONS'].str.contains("Free cash flow")]

    for column in free_cash_flow_df:
        try:
            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
        except Exception:
            pass   

    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
    free_cash_flows = []
    for date in dates:
        free_cash_flow_val = free_cash_flow_df[date[1]].tolist()[0].replace(",",".").replace("$","")
        free_cash_flows.append(free_cash_flow_val)
    if len(free_cash_flows) == 5:
        try:
            ratios["5"]["Free Cash Flow"] = sum(float(val) for val in free_cash_flows)/5.0
        except Exception:
            print e
            ratios["5"]["Free Cash Flow"] = "N/A"
    try:
        ratios["1"]["Free Cash Flow"] = float(free_cash_flows[0])
    except Exception:
        ratios["1"]["Free Cash Flow"] = "N/A"
    
    #FCF Coupon - Free Cash Flow to Security Holders (Key Ratios) = Free Cash Flow (CF)
    try:
        percentualFlowFive = 100*float(ratios["5"]["Free_Cash_Flow_to_Security_Holders"] / ratios["1"]["Market Cap"])
        ratios["5"]["Free_Cash_Flow_percent"] = round(percentualFlowFive,2)
    except Exception as e:
        print e
        ratios["5"]["Free_Cash_Flow_percent"]  = "N/A"
    try:
        percentualFlowOne = 100*float(ratios["1"]["Free_Cash_Flow_to_Security_Holders"] / ratios["1"]["Market Cap"])
        ratios["1"]["Free_Cash_Flow_percent"] = round(percentualFlowOne,2)
    except Exception:
        ratios["1"]["Free_Cash_Flow_percent"] = "N/A"

    #FCF (to Equity) Coupon Free Cash flow to shareholders (net owner earnings)/Market Cap
    try:
        ratios["5"]["FCF_to_Equity_Coupon"] = ratios["5"]["Free_Cash_Flow_to_Shareholders"] / ratios["1"]["Market Cap"]
    except Exception as e:
        print e
        ratios["5"]["FCF_to_Equity_Coupon"]  = "N/A"
    try:
        ratios["1"]["FCF_to_Equity_Coupon"] = ratios["1"]["Free_Cash_Flow_to_Shareholders"] / ratios["1"]["Market Cap"]
    except Exception:
        ratios["1"]["FCF_to_Equity_Coupon"] = "N/A"

    return ratios
