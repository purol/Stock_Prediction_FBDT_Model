import urllib, json
import requests
from urllib.request import urlopen
import pandas as pd
from datetime import datetime, timedelta
import os
from glob import glob
import time
import numpy as np

api_key = ''

# function to drop the common column
def drop_common_columns(df1, df2, key_columns):
    common_columns = df1.columns.intersection(df2.columns).tolist()
    common_columns = [col for col in common_columns if col not in key_columns]
    df2 = df2.drop(columns=common_columns)
    return df2

# Function to get the Data

def get_jsonparsed_data(url):
    while(True):
        try:
            res = urlopen(url)
            data = res.read().decode("utf-8")
            return json.loads(data)
        except Exception as e:
            print("urlopen fail. slep 1 sec...")
            time.sleep(1)

def download_tickers(Year, Month, Day):
    # get current date
    currentYear = Year
    currentMonth = Month
    currentDay = Day

    # mkdir if there is no dir
    if not os.path.exists("./tickers"):
        os.mkdir("./tickers")
        
    if not os.path.exists('./tickers/' + currentYear + currentMonth + currentDay):
        os.mkdir('./tickers/' + currentYear + currentMonth + currentDay)

    # nasdaq
    ticker_json = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/stock-screener?isEtf=false&country=US&exchange=nasdaq&limit=10000&apikey=%s" % api_key)
    ticker_df = pd.DataFrame(ticker_json)
    ticker_df.to_csv('./tickers/' + currentYear + currentMonth + currentDay + '/ticker_nasdaq.csv', sep=',', index=False)

    # nyse
    ticker_json = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/stock-screener?isEtf=false&country=US&exchange=nyse&limit=10000&apikey=%s" % api_key)
    ticker_df = pd.DataFrame(ticker_json)
    ticker_df.to_csv('./tickers/' + currentYear + currentMonth + currentDay + '/ticker_nyse.csv', sep=',', index=False)

def donwload_info(ticker_info, Year, Month, Day):
    ticker = ticker_info["symbol"]
    sector = ticker_info["sector"]
    industry = ticker_info["industry"]
    isActivelyTrading = ticker_info["isActivelyTrading"]
    market_name = ticker_info["exchangeShortName"]

    needed_variable = list(set(["symbol", "date", "marketCap", "price",
                       "revenue", "costOfRevenue", "grossProfit", "researchAndDevelopmentExpenses", "generalAndAdministrativeExpenses",
                       "sellingAndMarketingExpenses", "sellingGeneralAndAdministrativeExpenses", "otherExpenses", "operatingExpenses",
                       "costAndExpenses", "interestIncome", "interestExpense", "depreciationAndAmortization", "ebitda",
                       "operatingIncome", "totalOtherIncomeExpensesNet", "incomeBeforeTax", "incomeTaxExpense", "netIncome", # imcome
                       "cashAndCashEquivalents", "shortTermInvestments", "cashAndShortTermInvestments", "netReceivables",
                       "inventory", "otherCurrentAssets", "totalCurrentAssets", "propertyPlantEquipmentNet", "goodwill",
                       "intangibleAssets", "goodwillAndIntangibleAssets", "longTermInvestments", "taxAssets", "otherNonCurrentAssets",
                       "totalNonCurrentAssets", "otherAssets", "totalAssets", "accountPayables", "shortTermDebt",
                       "taxPayables", "deferredRevenue", "otherCurrentLiabilities", "totalCurrentLiabilities",
                       "longTermDebt", "deferredRevenueNonCurrent", "deferredTaxLiabilitiesNonCurrent",
                       "otherNonCurrentLiabilities", "totalNonCurrentLiabilities", "otherLiabilities",
                       "capitalLeaseObligations", "totalLiabilities", "preferredStock",
                       "commonStock", "retainedEarnings", "accumulatedOtherComprehensiveIncomeLoss", "othertotalStockholdersEquity",
                       "totalStockholdersEquity", "totalEquity", "totalLiabilitiesAndStockholdersEquity", "minorityInterest",
                       "totalLiabilitiesAndTotalEquity", "totalInvestments", "totalDebt", "netDebt", # balance
                       "netIncome", "depreciationAndAmortization", "deferredIncomeTax", "stockBasedCompensation", "changeInWorkingCapital",
                       "accountsReceivables", "inventory", "accountsPayables", "otherWorkingCapital", "otherNonCashItems",
                       "netCashProvidedByOperatingActivities", "investmentsInPropertyPlantAndEquipment", "acquisitionsNet",
                       "purchasesOfInvestments", "salesMaturitiesOfInvestments", "otherInvestingActivites", "netCashUsedForInvestingActivites",
                       "debtRepayment", "commonStockIssued", "commonStockRepurchased", "dividendsPaid", "otherFinancingActivites",
                       "netCashUsedProvidedByFinancingActivities", "effectOfForexChangesOnCash", "netChangeInCash", "cashAtEndOfPeriod",
                       "cashAtBeginningOfPeriod", "operatingCashFlow", "capitalExpenditure", "freeCashFlow"] # cashflow
                       ))
                       
    # get current date
    currentYear = Year
    currentMonth = Month
    currentDay = Day

    # mkdir if there is no dir
    if not os.path.exists("./info"):
        os.mkdir("./info")
        
    if not os.path.exists('./info/' + currentYear + currentMonth + currentDay):
        os.mkdir('./info/' + currentYear + currentMonth + currentDay)

    # check whether there is already info or not
    if len(glob('./info/' + currentYear + currentMonth + currentDay + f'/%s.csv' % ticker)):
        print("there is already info for %s. Just skip" % ticker)
        return # there is already info
    else:
        pass

    # read information
    key_json = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/key-metrics/%s?period=annual&apikey=%s" % (ticker, api_key))
    key_df = pd.DataFrame(key_json)
    income_json = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/income-statement/%s?period=annual&apikey=%s" % (ticker, api_key))
    income_df = pd.DataFrame(income_json)
    balance_json = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/%s?period=annual&apikey=%s" % (ticker, api_key))
    balance_df = pd.DataFrame(balance_json)
    cash_json = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/%s?period=annual&apikey=%s" % (ticker, api_key))
    cash_df = pd.DataFrame(cash_json)

    # if there is no information about company, just skip it
    if (key_df.empty):
        return
    if (income_df.empty):
        return
    if (balance_df.empty):
        return
    if (cash_df.empty):
        return
    
    # Define key columns
    key_columns = ["symbol", "calendarYear", "period"]

    # Start with the base DataFrame
    info_df = key_df

    # List of DataFrames to merge
    dataframes_to_merge = [income_df, balance_df, cash_df]

    # Merge DataFrames while dropping common columns
    for df in dataframes_to_merge:
        df = drop_common_columns(info_df, df, key_columns)
        info_df = pd.merge(info_df, df, on=key_columns, how="inner")
    
    if info_df.empty:
        pass
    else:
        
        # get price
        price_df = pd.DataFrame()
        price_list = []
        price_change_list = []
        problematic_index = []
        for index, row in info_df.iterrows():
           temp_price_df = pd.DataFrame()
           date = row['date']
           retry = 0
           while(temp_price_df.empty):
               print("try to get price at %s" % date)
               price_json = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/historical-price-full/%s?from=%s&to=%s&apikey=%s" % (ticker, date, date, api_key))
               temp_price_df = pd.DataFrame(price_json)
               retry = retry + 1
               date = datetime.strptime(date, "%Y-%m-%d")
               date = date + timedelta(days = 1)
               date = datetime.strftime(date, "%Y-%m-%d")
               if (retry > 7):
                   print("price cannot be found. something wrong. just skip it.")
                   problematic_index.append(index)
                   break;
           if (retry > 7):
               price_list.append(-1000)
           else:
               price_list.append(temp_price_df["historical"][0]["close"])
        info_df["price"] = price_list
        info_df.drop(problematic_index, inplace=True)
        price_list = [x for x in price_list if x != -1000]

        # selecte needed info
        info_df = info_df[needed_variable]

        # append sector/industry
        sector_list = []
        industry_list = []
        isActivelyTrading_list = []
        for i in range(0, len(info_df.index)):
            sector_list.append(sector)
            industry_list.append(industry)
            isActivelyTrading_list.append(isActivelyTrading)
        info_df["sector"] = sector_list
        info_df["industry"] = industry_list
        info_df["isActivelyTrading"] = isActivelyTrading_list

        # append sector/inductry PER
        sector_PER_list = []
        industry_PER_list = []
        problematic_index = []
        for index, row in info_df.iterrows():
            date = row['date']
            sector_PER_df = pd.DataFrame()
            industry_PER_df = pd.DataFrame()
            retry = 0
            while (
                (sector_PER_df.empty or industry_PER_df.empty) or
                (not (('sector' in sector_PER_df.columns) and (sector_list[0] in sector_PER_df['sector'].values))) or
                (not (('industry' in industry_PER_df.columns) and (industry_list[0] in industry_PER_df['industry'].values)))
            ):
                print("try to get sector/industry PER at %s" % date)
                sector_PER_json = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v4/sector_price_earning_ratio?date=%s&exchange=%s&apikey=%s" % (date, market_name, api_key))
                sector_PER_df = pd.DataFrame(sector_PER_json)
                industry_PER_json = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v4/industry_price_earning_ratio?date=%s&exchange=%s&apikey=%s" % (date, market_name, api_key))
                industry_PER_df = pd.DataFrame(industry_PER_json)
                retry = retry + 1
                date = datetime.strptime(date, "%Y-%m-%d")
                date = date + timedelta(days = 1)
                date = datetime.strftime(date, "%Y-%m-%d")
                if (retry > 7):
                    print("sector/industry PER cannot be found. something wrong. just skip it.")
                    problematic_index.append(index)
                    break;
            if (retry > 7):
                sector_PER_list.append(np.nan)
                industry_PER_list.append(np.nan)
            else:
                sector_per = sector_PER_df.loc[sector_PER_df['sector'] == sector_list[0], 'pe'].iloc[0]
                industry_per = industry_PER_df.loc[industry_PER_df['industry'] == industry_list[0], 'pe'].iloc[0]
                sector_PER_list.append(sector_per)
                industry_PER_list.append(industry_per)
        info_df["sector_per"] = sector_PER_list
        info_df["industry_per"] = industry_PER_list

        # append econimical data
        federalFundsrate_json = get_jsonparsed_data("https://financialmodelingprep.com/api/v4/economic?name=federalFunds&apikey=%s" % (api_key))
        CPI_json = get_jsonparsed_data("https://financialmodelingprep.com/api/v4/economic?name=CPI&apikey=%s" % (api_key))
        unemploymentRate_json = get_jsonparsed_data("https://financialmodelingprep.com/api/v4/economic?name=unemploymentRate&apikey=%s" % (api_key))
        industrialProductionTotalIndex_json = get_jsonparsed_data("https://financialmodelingprep.com/api/v4/economic?name=industrialProductionTotalIndex&apikey=%s" % (api_key))
        ThirtyYearFixedRateMortgageAverage_json = get_jsonparsed_data("https://financialmodelingprep.com/api/v4/economic?name=30YearFixedRateMortgageAverage&apikey=%s" % (api_key))

        federalFundsrate_df = pd.DataFrame(federalFundsrate_json)
        CPI_df = pd.DataFrame(CPI_json)
        unemploymentRate_df = pd.DataFrame(unemploymentRate_json)
        industrialProductionTotalIndex_df = pd.DataFrame(industrialProductionTotalIndex_json)
        ThirtyYearFixedRateMortgageAverage_df = pd.DataFrame(ThirtyYearFixedRateMortgageAverage_json)
        
        federalFundsrate_list = []
        CPI_list = []
        unemploymentRate_list = []
        industrialProductionTotalIndex_list = []
        ThirtyYearFixedRateMortgageAverage_list = []
        
        for index, row in info_df.iterrows():
            date = row['date']
            target_date = pd.to_datetime(date)
            
            federalFundsrate_values = federalFundsrate_df[pd.to_datetime(federalFundsrate_df['date']) <= target_date]
            if federalFundsrate_values.empty:
                federalFundsrate_list.append(np.nan)
            else:
                federalFundsrate_value = federalFundsrate_values.iloc[0]["value"]
                federalFundsrate_list.append(federalFundsrate_value)

            CPI_values = CPI_df[pd.to_datetime(CPI_df['date']) <= target_date]
            if CPI_values.empty:
                CPI_list.append(np.nan)
            else:
                CPI_value = CPI_values.iloc[0]["value"]
                CPI_list.append(CPI_value)

            unemploymentRate_values = unemploymentRate_df[pd.to_datetime(unemploymentRate_df['date']) <= target_date]
            if unemploymentRate_values.empty:
                unemploymentRate_list.append(np.nan)
            else:
                unemploymentRate_value = unemploymentRate_values.iloc[0]["value"]
                unemploymentRate_list.append(unemploymentRate_value)

            industrialProductionTotalIndex_values = industrialProductionTotalIndex_df[pd.to_datetime(industrialProductionTotalIndex_df['date']) <= target_date]
            if industrialProductionTotalIndex_values.empty:
                industrialProductionTotalIndex_list.append(np.nan)
            else:
                industrialProductionTotalIndex_value = industrialProductionTotalIndex_values.iloc[0]["value"]
                industrialProductionTotalIndex_list.append(industrialProductionTotalIndex_value)

            ThirtyYearFixedRateMortgageAverage_values = ThirtyYearFixedRateMortgageAverage_df[pd.to_datetime(ThirtyYearFixedRateMortgageAverage_df['date']) <= target_date]
            if ThirtyYearFixedRateMortgageAverage_values.empty:
                ThirtyYearFixedRateMortgageAverage_list.append(np.nan)
            else:
                ThirtyYearFixedRateMortgageAverage_value = ThirtyYearFixedRateMortgageAverage_values.iloc[0]["value"]
                ThirtyYearFixedRateMortgageAverage_list.append(ThirtyYearFixedRateMortgageAverage_value)
                
        info_df["federalFundsrate"] = federalFundsrate_list
        info_df["CPI"] = CPI_list
        info_df["unemploymentRate"] = unemploymentRate_list
        info_df["industrialProductionTotalIndex"] = industrialProductionTotalIndex_list
        info_df["ThirtyYearFixedRateMortgageAverage"] = ThirtyYearFixedRateMortgageAverage_list

            
        #problematic_index = []
            

        # replace infinity to NAN. infinity can be caused by zero market cap.
        #info_df.replace([np.inf, -np.inf], np.nan, inplace=True)

        # remove NAN, which is caused by growth at the oldest data
        #info_df = info_df.dropna()
        
        info_df.to_csv('./info/' + currentYear + currentMonth + currentDay + f'/%s.csv' % ticker, sep=',', index=False)

def download_infos(tickers, Year, Month, Day):
    for index, row in tickers.iterrows():
        print("download info... %s" % row["symbol"])
        donwload_info(row, Year, Month, Day)

def load_tickers(path):
    df_dic = []
    files = glob(path + "/*.csv", recursive = False)

    if not files:
        print("[ERROR] there is no ticker file. You need to download the list of tickers")
        exit(1)
    
    for file in files:
        df = pd.read_csv(file)
        df.drop(df.loc[df['industry']=='Shell Companies'].index, inplace=True) # remove shell company
        df.drop(df.loc[df['isEtf']==True].index, inplace=True) # remove ETF
        df.drop(df.loc[df['isFund']==True].index, inplace=True) # remove fund
        df = df[["symbol", "sector", "industry", "isActivelyTrading", "exchangeShortName"]]
        df = df.dropna()
        df_dic.append(df)
    tickers = pd.concat(df_dic, ignore_index=True)
    return tickers

currentYear = str(datetime.now().year)
currentMonth = str(datetime.now().month).zfill(2)
currentDay = str(datetime.now().day).zfill(2)

do_download_tickers = True
do_download_info = True

# download ticker list from FMP
if (do_download_tickers):
    download_tickers(currentYear, currentMonth, currentDay)

# load ticker list
ticker_path = glob("./tickers/*", recursive = False)[-1]
tickers = load_tickers(ticker_path)

# download stock info
if (do_download_info):
    download_infos(tickers, currentYear, currentMonth, currentDay)

