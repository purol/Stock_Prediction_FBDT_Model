import urllib, json
import requests
from urllib.request import urlopen
import pandas as pd
from datetime import datetime, timedelta
import os
from glob import glob
import time
import numpy as np

def DropAnomaly(df):
    
    # replace infinity to NAN. infinity can be caused by zero market cap.
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # remove NAN, which is caused by growth at the oldest data
    df = df.dropna()

    # drop large value
    df = df.copy()
    numeric_columns = df.select_dtypes(include=[np.number])
    df = df[(numeric_columns.abs() <= 100).all(axis=1)]
    df.reset_index(drop=True, inplace=True)

    return df

def FilterCompany(df):
    # If we use all dataset, there can be bias. If the company is liquidated, there is no more data. There are two way to deal with it.
    # 1. add data with pricechange = -100%
    # 2. do not use the data point which will be liquidated one year after.
    # the option 1 is better. However, it is technically difficult (I cannot distinguish between liquidated one and MnA one...)
    # therefore, I require that the total stockholders equity should be positive.
    # generally, the company will not be liquidated if total stockholders equity is positive.
    df = df[df['totalStockholdersEquity/marketCap'] >= 0]
    return df
    

def Do_preprocess(path, Year, Month, Day):
    files = glob(path + "/*.csv", recursive = False)

    if not files:
        print("[ERROR] there is no info file. You need to download info")
        exit(1)

    for file in files:
        info_df = pd.read_csv(file)
        # df to save processed dataset
        process_df = pd.DataFrame()
        if info_df.empty:
            continue
        else:
            price_change_list = []
            
            # basic information
            process_df['symbol'] = info_df['symbol']
            process_df['date'] = info_df['date']
            
            # income
            process_df['revenue/marketCap'] = info_df['revenue'] / info_df['marketCap']
            process_df['grossProfit/marketCap'] = info_df['grossProfit'] / info_df['marketCap']
            process_df['operatingExpenses/marketCap'] = info_df['operatingExpenses'] / info_df['marketCap']
            process_df['interestIncome/marketCap'] = info_df['interestIncome'] / info_df['marketCap']
            process_df['interestExpense/marketCap'] = info_df['interestExpense'] / info_df['marketCap']
            process_df['depreciationAndAmortization/marketCap'] = info_df['depreciationAndAmortization'] / info_df['marketCap']
            process_df['ebitda/marketCap'] = info_df['ebitda'] / info_df['marketCap']
            process_df['operatingIncome/marketCap'] = info_df['operatingIncome'] / info_df['marketCap']
            process_df['incomeBeforeTax/marketCap'] = info_df['incomeBeforeTax'] / info_df['marketCap']
            process_df['netIncome/marketCap'] = info_df['netIncome'] / info_df['marketCap']
            # balance
            process_df['cashAndCashEquivalents/marketCap'] = info_df['cashAndCashEquivalents'] / info_df['marketCap']
            process_df['inventory/marketCap'] = info_df['inventory'] / info_df['marketCap']
            process_df['totalCurrentAssets/marketCap'] = info_df['totalCurrentAssets'] / info_df['marketCap']
            process_df['totalNonCurrentAssets/marketCap'] = info_df['totalNonCurrentAssets'] / info_df['marketCap']
            process_df['totalAssets/marketCap'] = info_df['totalAssets'] / info_df['marketCap']
            process_df['shortTermDebt/marketCap'] = info_df['shortTermDebt'] / info_df['marketCap']
            process_df['totalCurrentLiabilities/marketCap'] = info_df['totalCurrentLiabilities'] / info_df['marketCap']
            process_df['longTermDebt/marketCap'] = info_df['longTermDebt'] / info_df['marketCap']
            process_df['totalNonCurrentLiabilities/marketCap'] = info_df['totalNonCurrentLiabilities'] / info_df['marketCap']
            process_df['totalStockholdersEquity/marketCap'] = info_df['totalStockholdersEquity'] / info_df['marketCap']
            # cash flow
            process_df['netCashProvidedByOperatingActivities/marketCap'] = info_df['netCashProvidedByOperatingActivities'] / info_df['marketCap']
            process_df['netCashUsedForInvestingActivites/marketCap'] = info_df['netCashUsedForInvestingActivites'] / info_df['marketCap']
            process_df['debtRepayment/marketCap'] = info_df['debtRepayment'] / info_df['marketCap']
            process_df['commonStockIssued/marketCap'] = info_df['commonStockIssued'] / info_df['marketCap']
            process_df['commonStockRepurchased/marketCap'] = info_df['commonStockRepurchased'] / info_df['marketCap']
            process_df['dividendsPaid/marketCap'] = info_df['dividendsPaid'] / info_df['marketCap']
            process_df['netCashUsedProvidedByFinancingActivities/marketCap'] = info_df['netCashUsedProvidedByFinancingActivities'] / info_df['marketCap']
            process_df['netChangeInCash/marketCap'] = info_df['netChangeInCash'] / info_df['marketCap']
            process_df['operatingCashFlow/marketCap'] = info_df['operatingCashFlow'] / info_df['marketCap']
            process_df['freeCashFlow/marketCap'] = info_df['freeCashFlow'] / info_df['marketCap']
            # additional info
            process_df['changestock'] = (info_df['marketCap'] / info_df['price']).pct_change(periods=-1)
            # growth info
            process_df['Marketcap growth rate'] = info_df['marketCap'].pct_change(periods=-1)
            
            process_df['revenue/marketCap change'] = process_df['revenue/marketCap'].diff(periods=-1)
            process_df['grossProfit/marketCap change'] = process_df['grossProfit/marketCap'].diff(periods=-1)
            process_df['operatingExpenses/marketCap change'] = process_df['operatingExpenses/marketCap'].diff(periods=-1)
            process_df['interestIncome/marketCap change'] = process_df['interestIncome/marketCap'].diff(periods=-1)
            process_df['interestExpense/marketCap change'] = process_df['interestExpense/marketCap'].diff(periods=-1)
            process_df['depreciationAndAmortization/marketCap change'] = process_df['depreciationAndAmortization/marketCap'].diff(periods=-1)
            process_df['ebitda/marketCap change'] = process_df['ebitda/marketCap'].diff(periods=-1)
            process_df['operatingIncome/marketCap change'] = process_df['operatingIncome/marketCap'].diff(periods=-1)
            process_df['incomeBeforeTax/marketCap change'] = process_df['incomeBeforeTax/marketCap'].diff(periods=-1)
            process_df['netIncome/marketCap change'] = process_df['netIncome/marketCap'].diff(periods=-1)

            process_df['cashAndCashEquivalents/marketCap change'] = process_df['cashAndCashEquivalents/marketCap'].diff(periods=-1)
            process_df['inventory/marketCap change'] = process_df['inventory/marketCap'].diff(periods=-1)
            process_df['totalCurrentAssets/marketCap change'] = process_df['totalCurrentAssets/marketCap'].diff(periods=-1)
            process_df['totalNonCurrentAssets/marketCap change'] = process_df['totalNonCurrentAssets/marketCap'].diff(periods=-1)
            process_df['totalAssets/marketCap change'] = process_df['totalAssets/marketCap'].diff(periods=-1)
            process_df['shortTermDebt/marketCap change'] = process_df['shortTermDebt/marketCap'].diff(periods=-1)
            process_df['totalCurrentLiabilities/marketCap change'] = process_df['totalCurrentLiabilities/marketCap'].diff(periods=-1)
            process_df['longTermDebt/marketCap change'] = process_df['longTermDebt/marketCap'].diff(periods=-1)
            process_df['totalNonCurrentLiabilities/marketCap change'] = process_df['totalNonCurrentLiabilities/marketCap'].diff(periods=-1)
            process_df['totalStockholdersEquity/marketCap change'] = process_df['totalStockholdersEquity/marketCap'].diff(periods=-1)

            process_df['netCashProvidedByOperatingActivities/marketCap change'] = process_df['netCashProvidedByOperatingActivities/marketCap'].diff(periods=-1)
            process_df['netCashUsedForInvestingActivites/marketCap change'] = process_df['netCashUsedForInvestingActivites/marketCap'].diff(periods=-1)
            process_df['debtRepayment/marketCap change'] = process_df['debtRepayment/marketCap'].diff(periods=-1)
            process_df['commonStockIssued/marketCap change'] = process_df['commonStockIssued/marketCap'].diff(periods=-1)
            process_df['commonStockRepurchased/marketCap change'] = process_df['commonStockRepurchased/marketCap'].diff(periods=-1)
            process_df['dividendsPaid/marketCap change'] = process_df['dividendsPaid/marketCap'].diff(periods=-1)
            process_df['netCashUsedProvidedByFinancingActivities/marketCap change'] = process_df['netCashUsedProvidedByFinancingActivities/marketCap'].diff(periods=-1)
            process_df['netChangeInCash/marketCap change'] = process_df['netChangeInCash/marketCap'].diff(periods=-1)
            process_df['operatingCashFlow/marketCap change'] = process_df['operatingCashFlow/marketCap'].diff(periods=-1)
            process_df['freeCashFlow/marketCap change'] = process_df['freeCashFlow/marketCap'].diff(periods=-1)
            # economical indicator
            #process_df['federalFundsrate'] = info_df['federalFundsrate']
            #process_df['CPI growth'] = info_df['CPI'].pct_change(periods=-1)
            #process_df['unemploymentRate'] = info_df['unemploymentRate']
            #process_df['industrialProductionTotalIndex growth'] = info_df['industrialProductionTotalIndex'].pct_change(periods=-1)
            #process_df['ThirtyYearFixedRateMortgageAverage'] = info_df['ThirtyYearFixedRateMortgageAverage']
            
            # market cap
            #process_df['marketCap/CPI'] = info_df['marketCap'] / info_df['CPI']
            #process_df['longTermDebt/marketCap/ThirtyYearFixedRateMortgageAverage'] = process_df['longTermDebt/marketCap'] / info_df['ThirtyYearFixedRateMortgageAverage']
            #process_df['longTermDebt/marketCap/ThirtyYearFixedRateMortgageAverage change'] = process_df['longTermDebt/marketCap/ThirtyYearFixedRateMortgageAverage'].diff(periods=-1)
            #process_df['revenue/marketCap change / industrialProductionTotalIndex growth'] = process_df['revenue/marketCap change'] / (process_df['industrialProductionTotalIndex growth'].pct_change(periods=-1))


            # calculate price change per year (answer)
            price_list = info_df['price'].tolist()
            date_list = info_df["date"].tolist()
            for i in range(0, len(info_df.index)):
                if(i == 0):
                    price_change_list.append(-200)# price change per year is null
                else:
                    price_current = price_list[i]
                    price_future = price_list[i - 1]
                    date_current = datetime.strptime(date_list[i], "%Y-%m-%d")
                    date_future = datetime.strptime(date_list[i - 1], "%Y-%m-%d")

                    delta_date = (date_future - date_current).days
                    price_change = price_future / price_current
                    
                    if(delta_date != 0):
                        price_change_per_year = pow(price_change, 365.0/delta_date)
                    else: # ENBA shows two report in the same period... why? just remove one of it
                        price_change_per_year = 1000000.0 
                    
                    price_change_list.append(price_change_per_year)
            process_df["pricechange/year"] = price_change_list

            # drop anomaly
            process_df = DropAnomaly(process_df)

            # filter company
            #process_df = FilterCompany(process_df)

        # debug
        # process_df['price'] = info_df['price']
        # process_df['stock'] = info_df['marketCap'] / info_df['price']

        # get current date
        currentYear = Year
        currentMonth = Month
        currentDay = Day

        # mkdir if there is no dir
        if not os.path.exists("./preprocess"):
            os.mkdir("./preprocess")
        
        if not os.path.exists('./preprocess/' + currentYear + currentMonth + currentDay):
            os.mkdir('./preprocess/' + currentYear + currentMonth + currentDay)

        process_df.to_csv('./preprocess/' + currentYear + currentMonth + currentDay + "/" + os.path.basename(file), sep=',', index=False)


currentYear = str(datetime.now().year)
currentMonth = str(datetime.now().month).zfill(2)
currentDay = str(datetime.now().day).zfill(2)

# do preprocess
info_path = glob("./info/*", recursive = False)[-1]
Do_preprocess(info_path, currentYear, currentMonth, currentDay)

            
