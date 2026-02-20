import urllib, json
import requests
from urllib.request import urlopen
import pandas as pd
from datetime import datetime, timedelta
import os
from glob import glob
import time
import numpy as np

def make_train_test_set(path, excluded_years, Year, Month, Day):
    files = glob(path + "/*.csv", recursive = False)

    if not files:
        print("[ERROR] there is no preprocess file. You need to preprocess")
        exit(1)

    df_all = pd.DataFrame()

    for file in files:
        df = pd.read_csv(file)
        if df.empty:
            continue
        else:
            df_all = pd.concat([df_all, df], ignore_index=True)

    # exclude the info which will be used for the application
    df_all['date'] = pd.to_datetime(df_all['date'], format='%Y-%m-%d')
    df_all = df_all[~df_all['date'].dt.year.isin(excluded_years)]

    # exclude the info whose price change is invalid
    df_all = df_all[df_all['pricechange/year'] != -200]

    # shuffle
    df_all = df_all.sample(frac=1)

    # divide
    df_train = df_all.iloc[:round(len(df_all.index)/2), :]
    df_test = df_all.iloc[round(len(df_all.index)/2): , :]

    # get current date
    currentYear = Year
    currentMonth = Month
    currentDay = Day

    # mkdir if there is no dir
    if not os.path.exists("./train"):
        os.mkdir("./train")
        
    if not os.path.exists('./train/' + currentYear + currentMonth + currentDay):
        os.mkdir('./train/' + currentYear + currentMonth + currentDay)

    if not os.path.exists("./test"):
        os.mkdir("./test")
        
    if not os.path.exists('./test/' + currentYear + currentMonth + currentDay):
        os.mkdir('./test/' + currentYear + currentMonth + currentDay)

    df_train.to_csv('./train/' + currentYear + currentMonth + currentDay + f'/train.csv', sep=',', index=False)
    df_test.to_csv('./test/' + currentYear + currentMonth + currentDay + f'/test.csv', sep=',', index=False)


def make_application_set(path, included_years, Year, Month, Day):
    files = glob(path + "/*.csv", recursive = False)

    if not files:
        print("[ERROR] there is no preprocess file. You need to preprocess")
        exit(1)

    df_all = pd.DataFrame()

    for file in files:
        df = pd.read_csv(file)
        if df.empty:
            continue
        else:
            df_all = pd.concat([df_all, df], ignore_index=True)

    for included_year in included_years:
        # include the info which will be used for the application
        df_all['date'] = pd.to_datetime(df_all['date'], format='%Y-%m-%d')
        df_selected = df_all[df_all['date'].dt.year == included_year]

        # get current date
        currentYear = Year
        currentMonth = Month
        currentDay = Day

        # mkdir if there is no dir
        if not os.path.exists("./application"):
            os.mkdir("./application")
        
        if not os.path.exists('./application/' + currentYear + currentMonth + currentDay):
            os.mkdir('./application/' + currentYear + currentMonth + currentDay)

        df_selected.to_csv('./application/' + currentYear + currentMonth + currentDay + '/application_' + str(included_year) + '.csv', sep=',', index=False)


Excluded_years = [2021, 2022, 2023]

currentYear = str(datetime.now().year)
currentMonth = str(datetime.now().month).zfill(2)
currentDay = str(datetime.now().day).zfill(2)

# test/train set: we know answer but not the latest data
preprocess_path = glob("./preprocess/*", recursive = False)[-1]
make_train_test_set(preprocess_path, Excluded_years, currentYear, currentMonth, currentDay)

# application set: we know answer but the latest data
preprocess_path = glob("./preprocess/*", recursive = False)[-1]
make_application_set(preprocess_path, Excluded_years, currentYear, currentMonth, currentDay)
            
