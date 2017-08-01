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

def performanceData(dfs_list_pickle,is_file,bs_file,cf_file,ratios):

    with open(dfs_list_pickle,"r") as f:
        dfs_list = pickle.load(f)

    df_is = pd.read_csv(is_file)
    df_bs = pd.read_csv(bs_file)
    df_cf = pd.read_csv(cf_file)

    print df_is.shape, df_bs.shape, df_cf.shape
    for df in dfs_list:
        try:
            try:
                if df[df['Financials'].str.contains("10-Year Average")].any:
                    dates = []
                    EPS_growth = df[df['Financials'].str.contains("10-Year Average")]

                    for column in EPS_growth[3:4]:
                        try:
                            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
                        except Exception:
                            pass
                    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
                    eps_vals = []
                    for date in dates:
                        eps_vals.append(EPS_growth[date[1]].tolist()[0])
                    if len(eps_vals) == 5:
                        try:
                            ratios["5"]["eps 10"] = sum(float(val) for val in eps_vals)/5.0
                        except Exception:
                            ratios["5"]["eps 10"] = "N/A"
                    try:
                        ratios["1"]["eps 10"] = float(eps_vals[0])
                    except Exception:
                        ratios["1"]["eps 10"] = "N/A"
            except Exception:
                pass
            try:
                net_income = df[(df['Financials'].str.contains("net income",case=False)) &
                                (df['Financials'].str.contains("mil",case=False))]
                if net_income.any:
                    dates = []

                    for column in net_income:
                        try:
                            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
                        except Exception:
                            pass       
                    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
                    net_incomes = []
                    for date in dates:
                        net_income_val = net_income[date[1]].tolist()[0].replace(",",".")
                        net_incomes.append(net_income_val)
                        print net_income_val
                    if len(net_incomes) == 5:
                        try:
                            ratios["5"]["net_income"] = sum(float(val) for val in net_incomes)/5.0
                        except Exception:
                            print e
                            ratios["5"]["net_income"] = "N/A"
                    try:
                        ratios["1"]["net_income"] = float(net_incomes[0])
                    except Exception:
                        ratios["1"]["net_income"] = "N/A"
            except Exception:
                pass
            try:
                revenue = df[(df['Financials'].str.contains("Revenue",case=False)) &
                                 (df['Financials'].str.contains("mil",case=False))] 
                if revenue.any:
                    dates = []

                    for column in revenue:
                        try:
                            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
                        except Exception:
                            pass   
                    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
                    revenues = []
                    for date in dates:
                        revenue_val = revenue[date[1]].tolist()[0].replace(",",".")
                        revenues.append(revenue_val)
                    if len(revenues) == 5:
                        try:
                            ratios["5"]["revenue"] = sum(float(val) for val in revenues)/5.0
                        except Exception:
                            ratios["5"]["revenue"] = "N/A"
                    try:
                        ratios["1"]["revenue"] = float(revenues[0])
                    except Exception:
                        ratios["1"]["revenue"] = "N/A"
            except Exception:
                pass
            try:
                #df[(df['Financials'].str.contains("Dividends",case=False))&(df['Financials'].str.contains("USD",case=False))]
                dividends_per_share = df[(df['Financials'].str.contains("Dividends",case=False)) & 
                                         (df['Financials'].str.contains("USD",case=False))]
                if dividends_per_share.any:
                    dates = []

                    for column in dividends_per_share:
                        try:
                            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
                        except Exception:
                            pass   
                    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
                    dividends_per_shares = []
                    for date in dates:
                        dividends_per_share_val = dividends_per_share[date[1]].tolist()[0].replace(",",".")
                        dividends_per_shares.append(dividends_per_share_val)
                    if len(dividends_per_shares) == 5:
                        try:
                            ratios["5"]["dividends_per_share"] = sum(float(val) for val in dividends_per_shares)/5.0
                        except Exception:
                            ratios["5"]["dividends_per_share"] = "N/A"
                    try:
                        ratios["1"]["dividends_per_share"] = float(dividends_per_shares[0])
                    except Exception:
                        ratios["1"]["dividends_per_share"] = "N/A"
            except Exception:
                pass
            try:
                #df[df['Profitability'].str.contains("Return on Invested Capital")]
                roic = df[df['Profitability'].str.contains("Return on Invested Capital")]
                if roic.any:
                    dates = []

                    for column in roic:
                        try:
                            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
                        except Exception:
                            pass   
                    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
                    roics = []
                    for date in dates:
                        roic_val = roic[date[1]].tolist()[0].replace(",",".")
                        roics.append(roic_val)
                    if len(roics) == 5:
                        try:
                            ratios["5"]["roic"] = sum(float(val) for val in roics)/5.0
                        except Exception:
                            ratios["5"]["roic"] = "N/A"
                    try:
                        ratios["1"]["roic"] = float(roics[0])
                    except Exception:
                        ratios["1"]["roic"] = "N/A"
            except Exception:
                pass
            try:
                #df[df['Financials'].str.contains("Operating Margin")]
                operating_margin = df[df['Financials'].str.contains("Operating Margin")]
                if operating_margin.any:
                    dates = []

                    for column in operating_margin:
                        try:
                            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
                        except Exception:
                            pass   
                    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
                    operating_margins = []
                    for date in dates:
                        operating_margin_val = operating_margin[date[1]].tolist()[0].replace(",",".")
                        operating_margins.append(operating_margin_val)
                    if len(operating_margins) == 5:
                        try:
                            ratios["5"]["operating_margin"] = sum(float(val) for val in operating_margins)/5.0
                        except Exception:
                            ratios["5"]["operating_margin"] = "N/A"
                    try:
                        ratios["1"]["operating_margin"] = float(operating_margins[0])
                    except Exception:
                        ratios["1"]["operating_margin"] = "N/A"
            except Exception:
                pass
            try:
                #df[df['Profitability'].str.contains("Interest Coverage")]
                interest_coverage = df[df['Profitability'].str.contains("Interest Coverage")]
                if interest_coverage.any:
                    dates = []

                    for column in interest_coverage:
                        try:
                            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
                        except Exception:
                            pass   
                    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
                    interest_coverages = []
                    for date in dates:
                        interest_coverage_val = interest_coverage[date[1]].tolist()[0].replace(",",".")
                        interest_coverages.append(interest_coverage_val)
                    if len(interest_coverages) == 5:
                        try:
                            ratios["5"]["interest_coverages"] = sum(float(val) for val in interest_coverages)/5.0
                        except Exception:
                            ratios["5"]["interest_coverages"] = "N/A"
                    try:
                        ratios["1"]["interest_coverages"] = float(interest_coverages[0])
                    except Exception:
                        ratios["1"]["interest_coverages"] = "N/A"
            except Exception:
                pass
            try:
                #df[(df['Financials'].str.contains("Working Capital",case=False))&(df['Financials'].str.contains("USD",case=False))]
                working_capital = df[(df['Financials'].str.contains("Working Capital",case=False)) &
                                     (df['Financials'].str.contains("USD",case=False))]
                if working_capital.any:
                    dates = []

                    for column in working_capital:
                        try:
                            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
                        except Exception:
                            pass   
                    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
                    working_capitals = []
                    for date in dates:
                        working_capital_val = working_capital[date[1]].tolist()[0].replace(",",".")
                        working_capitals.append(working_capital_val)
                    if len(working_capitals) == 5:
                        try:
                            ratios["5"]["working_capital"] = sum(float(val) for val in working_capitals)/5.0
                        except Exception:
                            ratios["5"]["working_capital"] = "N/A"
                    try:
                        ratios["1"]["working_capital"] = float(working_capitals[0])
                    except Exception:
                        ratios["1"]["working_capital"] = "N/A"
            except Exception:
                pass
            try:
                #df[(df['Financials'].str.contains("Free Cash Flow",case=False))&(df['Financials'].str.contains("USD Mil",case=False))]
                free_cash_flow = df[(df['Financials'].str.contains("Free Cash Flow",case=False)) &
                                    (df['Financials'].str.contains("USD Mil",case=False))]
                if free_cash_flow.any:
                    dates = []

                    for column in free_cash_flow:
                        try:
                            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
                        except Exception:
                            pass   
                    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
                    free_cash_flows = []
                    for date in dates:
                        free_cash_flow_val = free_cash_flow[date[1]].tolist()[0].replace(",",".")
                        free_cash_flows.append(free_cash_flow_val)
                    if len(free_cash_flows) == 5:
                        try:
                            ratios["5"]["free cash flow"] = sum(float(val) for val in free_cash_flows)/5.0
                        except Exception:
                            ratios["5"]["free cash flow"] = "N/A"
                    try:
                        ratios["1"]["free cash flow"] = float(free_cash_flows[0])
                    except Exception:
                        ratios["1"]["free cash flow"] = "N/A"
            except Exception:
                pass
            try:
                #df[(df['Financials'].str.contains("Free Cash Flow",case=False))&(df['Financials'].str.contains("USD Mil",case=False))]
                EarningsPerShare = df[(df['Financials'].str.contains("Earnings Per Share",case=False)) &
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
                            ratios["5"]["Earnings Per Share"] = sum(float(val) for val in earnings_per_shares)/5.0
                        except Exception:
                            ratios["5"]["Earnings Per Share"] = "N/A"
                    else:
                        ratios["5"]["Earnings Per Share"] = "N/A"
                    try:
                        ratios["1"]["Earnings Per Share"] = float(earnings_per_shares[0])
                    except Exception:
                        ratios["1"]["Earnings Per Share"] = "N/A"
                    ratios["5"]["Earnings_Per_Share"] = ratios["5"]["Earnings Per Share"]
                    ratios["1"]["Earnings_Per_Share"] = ratios["1"]["Earnings Per Share"]
            except Exception:
                pass
            try:
                FreeCashFlow = df[(df['Financials'].str.contains("Free Cash Flow",case=False)) &
                                  (df['Financials'].str.contains("USD Mil",case=False))]
                if FreeCashFlow.any:
                    dates = []

                    for column in FreeCashFlow:
                        try:
                            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
                        except Exception:
                            pass   
                    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
                    free_cash_flows = []
                    for date in dates:
                        free_cash_flow_val = FreeCashFlow[date[1]].tolist()[0].replace(",",".")
                        free_cash_flows.append(free_cash_flow_val)
                    if len(free_cash_flows) == 5:
                        try:
                            ratios["5"]["Free_Cash_Flow_to_Security_Holders"] = sum(float(val) for val in free_cash_flows)/5.0
                        except Exception:
                            ratios["5"]["Free_Cash_Flow_to_Security_Holders"] = "N/A"
                    try:
                        ratios["1"]["Free_Cash_Flow_to_Security_Holders"] = float(free_cash_flows[0])
                    except Exception:
                        ratios["1"]["Free_Cash_Flow_to_Security_Holders"] = "N/A"
            except Exception:
                pass

            try:
                
                index = df.loc[df["Financials"]=="Revenue %"].index.tolist()[0]
                revenue_data = df.loc[range(index,index+5)]
                dates = []
                revenue_5_df = revenue_data[revenue_data['Financials'].str.contains("5-Year Average")]
                if revenue_5_df.any:
                    for column in revenue_5_df:
                        try:
                            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
                        except Exception:
                            pass   

                    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
                    revenues_growth = []
                    for date in dates:
                        revenue_5_val = revenue_5_df[date[1]].tolist()[0].replace(",",".").replace("$","")
                        revenues_growth.append(revenue_5_val)
                    if len(revenues_growth) == 5:
                        try:
                            ratios["5"]["Revenue_Growth"] = sum(float(val) for val in revenues_growth)/5.0
                        except Exception:
                            ratios["5"]["Revenue_Growth"] = "N/A"
                        
                    try:
                        ratios["1"]["Revenue_Growth"] = float(revenues_growth[0])
                    except Exception:
                        ratios["1"]["Revenue_Growth"] = "N/A"
            except Exception as e:
                print e

        except Exception:
            pass
    dates = []
    EPS_basic_df = df_is[df_is['USD IN MILLIONS'].str.contains("Basic")][0:1]

    for column in EPS_basic_df:
        try:
            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
        except Exception:
            pass   

    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
    eps_basics = []
    for date in dates:
        eps_basic_val = EPS_basic_df[date[1]].tolist()[0].replace(",",".")
        eps_basics.append(eps_basic_val)
    if len(eps_basics) == 5:
        try:
            ratios["5"]["eps_basic"] = sum(float(val) for val in eps_basics)/5.0
        except Exception:
            ratios["5"]["eps_basic"] = "N/A"
    try:
        ratios["1"]["eps_basic"] = float(eps_basics[0])
    except Exception:
        ratios["1"]["eps_basic"] = "N/A"

    #eps diluted
    dates = []
    EPS_diluted_df = df_is[df_is['USD IN MILLIONS'].str.contains("Diluted")][0:1]

    for column in EPS_diluted_df:
        try:
            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
        except Exception:
            pass   

    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
    eps_diluteds = []
    for date in dates:
        eps_diluted_val = EPS_diluted_df[date[1]].tolist()[0].replace(",",".").replace("$","")
        eps_diluteds.append(eps_diluted_val)
    if len(eps_basics) == 5:
        try:
            ratios["5"]["eps_diluted"] = sum(float(val) for val in eps_diluteds)/5.0
        except Exception as e:
            print e
            ratios["5"]["eps_diluted"] = "N/A"
    try:
        ratios["1"]["eps_diluted"] = float(eps_basics[0])
    except Exception:
        ratios["1"]["eps_diluted"] = "N/A"

    #ROE ROA
    cf_net_income_df = df_cf[df_cf['USD IN MILLIONS'].str.contains("Net income")]
    print cf_net_income_df.shape
    dates = []
    for column in cf_net_income_df:
        try:
            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
        except Exception:
            pass   
    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
    columns = [date[1] for date in dates]
    print columns
    cf_net_income_df = cf_net_income_df[columns].applymap(replacer)

    print cf_net_income_df.shape

    if cf_net_income_df.shape[1] == 5:
        try:
            ratios["5"]["net income CF"] = sum(float(val) for val in cf_net_income_df.ix[cf_net_income_df.index[0]].tolist())/5.0
        except Exception as e:
            print e
            ratios["5"]["net income CF"] = "N/A"
    try:
        ratios["1"]["net income CF"] = float(cf_net_income_df.ix[cf_net_income_df.index[0]].tolist()[0])
    except Exception:
        ratios["1"]["net income CF"] = "N/A"


    stockholders_equitity_df = df_bs[df_bs['USD IN MILLIONS'].str.contains("Total stockholders' equity")]
    dates = []
    for column in stockholders_equitity_df:
        try:
            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
        except Exception:
            pass   
    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
    columns = [date[1] for date in dates]

    stockholders_equitity_df = stockholders_equitity_df[columns].applymap(replacer)

    if stockholders_equitity_df.shape[1] == 5:
        try:
            ratios["5"]["stockholders equitity CF"] = sum(float(val) for val in stockholders_equitity_df.ix[stockholders_equitity_df.index[0]].tolist())/5.0
        except Exception as e:
            print e
            ratios["5"]["stockholders equitity CF"] = "N/A"
    try:
        ratios["1"]["stockholders equitity CF"] = float(stockholders_equitity_df.ix[stockholders_equitity_df.index[0]].tolist()[0])
    except Exception:
        ratios["1"]["stockholders equitity CF"] = "N/A"


    total_assets_df = df_bs[df_bs['USD IN MILLIONS'].str.contains("Total assets")]
    dates = []
    for column in total_assets_df:
        try:
            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
        except Exception:
            pass   
    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
    columns = [date[1] for date in dates]
    total_assets_df = total_assets_df[columns].applymap(replacer)

    if total_assets_df.shape[1] == 5:
        try:
            ratios["5"]["total assets CF"] = sum(float(val) for val in total_assets_df.ix[total_assets_df.index[0]].tolist())/5.0
        except Exception as e:
            print e
            ratios["5"]["total assets CF"] = "N/A"
    try:
        ratios["1"]["total assets CF"] = float(total_assets_df.ix[total_assets_df.index[0]].tolist()[0])
    except Exception:
        ratios["1"]["total assets CF"] = "N/A"

    try:
        ratios["5"]["ROE"] = 100.0*ratios["5"]["net income CF"]/ratios["5"]["stockholders equitity CF"]
    except Exception as e:
        print e
        ratios["5"]["ROE"] = "N/A"
    try:
        ratios["1"]["ROE"] = 100.0*ratios["1"]["net income CF"]/ratios["1"]["stockholders equitity CF"]
    except Exception:
        ratios["1"]["ROE"] = "N/A"

    try:
        ratios["5"]["ROA"] = 100.0*ratios["5"]["net income CF"]/ratios["5"]["total assets CF"]
    except Exception as e:
        print e
        ratios["5"]["ROA"] = "N/A"
    try:
        ratios["1"]["ROA"] = 100.0*ratios["1"]["net income CF"]/ratios["1"]["total assets CF"]
    except Exception:
        ratios["1"]["ROA"] = "N/A"

    #gross profit
    dates = []
    gross_profit_df = df_is[df_is['USD IN MILLIONS'].str.contains("Gross profit")]

    for column in gross_profit_df:
        try:
            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
        except Exception:
            pass   

    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
    gross_profits = []
    for date in dates:
        gross_profit_val = gross_profit_df[date[1]].tolist()[0].replace(",",".").replace("$","")
        gross_profits.append(gross_profit_val)
    if len(gross_profits) == 5:
        try:
            ratios["5"]["gross_profit"] = sum(float(val) for val in gross_profits)/5.0
        except Exception:
            print e
            ratios["5"]["gross_profit"] = "N/A"
    try:
        ratios["1"]["gross_profit"] = float(gross_profits[0])
    except Exception:
        ratios["1"]["gross_profit"] = "N/A"

    #Liqudiation Value (CA - All L) – Current Assets (from the BS) MINUS Total Liabilities (from the BS)
    TotalCash_df = df_bs[df_bs['USD IN MILLIONS'].str.contains("Total cash")]
    dates = []
    for column in TotalCash_df:
        try:
            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
        except Exception:
            pass   
    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
    columns = [date[1] for date in dates]

    TotalCash_df = TotalCash_df[columns].applymap(replacer)

    if TotalCash_df.shape[1] == 5:
        try:
            ratios["5"]["total cash CF"] = sum(float(val) for val in TotalCash_df.ix[TotalCash_df.index[0]].tolist())/5.0
        except Exception as e:
            print e
            ratios["5"]["total cash CF"] = "N/A"
    try:
        ratios["1"]["total cash CF"] = float(TotalCash_df.ix[TotalCash_df.index[0]].tolist()[0])
    except Exception:
        ratios["1"]["total cash CF"] = "N/A"


    TotalLiabilities = df_bs[df_bs['USD IN MILLIONS'].str.contains("Total liabilities")][0:1]
    dates = []
    for column in TotalLiabilities:
        try:
            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
        except Exception:
            pass   
    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
    columns = [date[1] for date in dates]

    TotalLiabilities = TotalLiabilities[columns].applymap(replacer)

    if TotalLiabilities.shape[1] == 5:
        try:
            ratios["5"]["total liabilities CF"] = sum(float(val) for val in TotalLiabilities.ix[TotalLiabilities.index[0]].tolist())/5.0
        except Exception as e:
            print e
            ratios["5"]["total liabilities CF"] = "N/A"
    try:
        ratios["1"]["total liabilities CF"] = float(TotalLiabilities.ix[TotalLiabilities.index[0]].tolist()[0])
    except Exception:
        ratios["1"]["total liabilities CF"] = "N/A"

    try:
        ratios["5"]["Liquidation_Val"] = ratios["5"]["total cash CF"] - ratios["5"]["total liabilities CF"]
    except Exception as e:
        print e
        ratios["5"]["Liquidation_Val"] = "N/A"
    try:
        ratios["1"]["Liquidation_Val"] = ratios["1"]["total cash CF"] - ratios["1"]["total liabilities CF"]
    except Exception:
        ratios["1"]["Liquidation_Val"] = "N/A"

    #Debt-Equity Debt - Equity Ratio = Total Liabilities / Shareholders' Equity , “Total Liabilities” at Balance Sheet, 
    #“SHAREHOLDER'S EQUITY” at BALANCE SHEET

    try:
        ratios["5"]["Debt_Equity_Debt"] = ratios["5"]["total liabilities CF"]/ratios["5"]["stockholders equitity CF"]
    except Exception as e:
        print e
        ratios["5"]["Debt_Equity_Debt"] = "N/A"
    try:
        ratios["1"]["Debt_Equity_Debt"] = ratios["1"]["total liabilities CF"]/ratios["1"]["stockholders equitity CF"]
    except Exception:
        ratios["1"]["Debt_Equity_Debt"] = "N/A"

    #Total Debt , Short-term debt (BS) + Long-term debt (BS)

    #Short-term debt
    dates = []
    short_term_debt_df = df_bs[df_bs['USD IN MILLIONS'].str.contains("Short-term debt")]

    for column in short_term_debt_df:
        try:
            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
        except Exception:
            pass   

    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
    short_term_debts = []
    for date in dates:
        short_term_debt_val = short_term_debt_df[date[1]].tolist()[0].replace(",",".").replace("$","")
        short_term_debts.append(short_term_debt_val)
    if len(short_term_debts) == 5:
        try:
            ratios["5"]["short term debt"] = sum(float(val) for val in short_term_debts)/5.0
        except Exception:
            print e
            ratios["5"]["short term debt"] = "N/A"
        try:
            ratios["1"]["short term debt"] = float(short_term_debts[0])
        except Exception:
            ratios["1"]["short term debt"] = "N/A"

    #Long-term debt
    dates = []
    long_term_debt_df = df_bs[df_bs['USD IN MILLIONS'].str.contains("Long-term debt")]

    for column in long_term_debt_df:
        try:
            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
        except Exception:
            pass   

    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
    long_term_debts = []
    for date in dates:
        long_term_debt_val = long_term_debt_df[date[1]].tolist()[0].replace(",",".").replace("$","")
        long_term_debts.append(long_term_debt_val)
    if len(short_term_debts) == 5:
        try:
            ratios["5"]["long term debt"] = sum(float(val) for val in long_term_debts)/5.0
        except Exception:
            print e
            ratios["5"]["long term debt"] = "N/A"
    try:
        ratios["1"]["long term debt"] = float(long_term_debts[0])
    except Exception:
        ratios["1"]["long term debt"] = "N/A"

    try:
        ratios["5"]["Total_Debt"] = ratios["5"]["long term debt"] + ratios["5"]["short term debt"]
    except Exception as e:
        print e
        ratios["5"]["Total_Debt"] = "N/A"
    try:
        ratios["1"]["Total_Debt"] = ratios["1"]["long term debt"] + ratios["1"]["short term debt"]
    except Exception:
        ratios["1"]["Total_Debt"] = "N/A"

    #Working Capital (less invetories) working capital (from Key ratios) MINUS inventory (from Balance Sheet)

    #inventories

    dates = []
    inventories_df = df_bs[df_bs['USD IN MILLIONS'].str.contains("Inventories")]

    for column in inventories_df:
        try:
            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
        except Exception:
            pass   

    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
    inventories = []
    for date in dates:
        inventories_val = inventories_df[date[1]].tolist()[0].replace(",",".").replace("$","")
        inventories.append(inventories_val)
    if len(inventories) == 5:
        try:
            ratios["5"]["inventories"] = sum(float(val) for val in inventories)/5.0
        except Exception:
            print e
            ratios["5"]["inventories"] = "N/A"
    try:
        ratios["1"]["inventories"] = float(inventories[0])
    except Exception:
        ratios["1"]["inventories"] = "N/A"

    #Free Cash Flow to Security Holders (Owner Earnings) Free Cash Flow (from Key Ratios)



    #still missing the ratios from Key Ratios

    #Free Cash Flow to Shareholders (Net Owner Earnings) Free Cash Flow (from key ratios - as above) 
    #MINUS total debt (from Balance Sheet).

    #still missing the ratios from Key Ratios

    #Total Current Assets “Total Current Assets” at BS

    dates = []
    total_current_assets_df = df_bs[df_bs['USD IN MILLIONS'].str.contains("Total current assets")]

    for column in total_current_assets_df:
        try:
            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
        except Exception:
            pass   

    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
    total_current_assets = []
    for date in dates:
        total_current_assets_val = total_current_assets_df[date[1]].tolist()[0].replace(",",".").replace("$","")
        total_current_assets.append(total_current_assets_val)
    if len(total_current_assets) == 5:
        try:
            ratios["5"]["total_current_assets"] = sum(float(val) for val in total_current_assets)/5.0
        except Exception:
            print e
            ratios["5"]["total_current_assets"] = "N/A"
    try:
        ratios["1"]["total_current_assets"] = float(total_current_assets[0])
    except Exception:
        ratios["1"]["total_current_assets"] = "N/A"

    #Cash at end of period “Cash at end of period” at CF

    dates = []
    cash_at_end_of_period_df = df_cf[df_cf['USD IN MILLIONS'].str.contains("Cash at end of period")]

    for column in cash_at_end_of_period_df:
        try:
            dates.append((datetime.datetime.strptime(column,"%Y-%m"),column))
        except Exception:
            pass   

    dates = sorted(dates, key=lambda x: x[0],reverse=True)[:5]
    cash_at_end_of_periods = []
    for date in dates:
        cash_at_end_of_period_val = cash_at_end_of_period_df[date[1]].tolist()[0].replace(",",".").replace("$","")
        cash_at_end_of_periods.append(cash_at_end_of_period_val)
    if len(cash_at_end_of_periods) == 5:
        try:
            ratios["5"]["Cash_at_end_of_period"] = sum(float(val) for val in cash_at_end_of_periods)/5.0
        except Exception:
            print e
            ratios["5"]["Cash_at_end_of_period"] = "N/A"
    try:
        ratios["1"]["Cash_at_end_of_period"] = float(cash_at_end_of_periods[0])
    except Exception:
        ratios["1"]["Cash_at_end_of_period"] = "N/A"

    #Book Value Total Assets (BS) - Total Liabilities (BS)

    try:
        ratios["5"]["Book_Value"] = ratios["5"]["total_current_assets"] - ratios["5"]["total liabilities CF"]
    except Exception as e:
        print e
        ratios["5"]["Book_Value"] = "N/A"
    try:
        ratios["1"]["Book_Value"] = ratios["1"]["total_current_assets"] - ratios["1"]["total liabilities CF"]
    except Exception:
        ratios["1"]["Book_Value"] = "N/A"

    #Free Cash Flow to Shareholders (Net Owner Earnings) Free Cash Flow (from key ratios - as above) MINUS total debt (from Balance Sheet).

    try:
        ratios["5"]["Free_Cash_Flow_to_Shareholders"] = ratios["5"]["Free_Cash_Flow_to_Security_Holders"] - ratios["5"]["Total_Debt"]
    except Exception as e:
        print e
        ratios["5"]["Free_Cash_Flow_to_Shareholders"] = "N/A"
    try:
        ratios["1"]["Free_Cash_Flow_to_Shareholders"] = ratios["1"]["Free_Cash_Flow_to_Security_Holders"] - ratios["1"]["Total_Debt"]
    except Exception:
        ratios["1"]["Free_Cash_Flow_to_Shareholders"] = "N/A"

    #Working Capital (less invetories) working capital (from Key ratios) MINUS inventory (from Balance Sheet)

    try:
        ratios["5"]["Working_Capital_less_invetories"] = ratios["5"]["working_capital"] - ratios["5"]["inventories"]
    except Exception as e:
        print e
        ratios["5"]["Working_Capital_less_invetories"] = "N/A"
    try:
        ratios["1"]["Working_Capital_less_invetories"] = ratios["1"]["working_capital"] - ratios["1"]["inventories"]
    except Exception:
        ratios["1"]["Working_Capital_less_invetories"] = "N/A"
    return ratios
