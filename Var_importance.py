#!/usr/bin/env python
import numpy as np
import sys, os
import math

import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

import operator

unsorted_list = [('revenue/marketCap',0.0258522),
('grossProfit/marketCap',0.02162),
('operatingExpenses/marketCap',0.0323737),
('interestIncome/marketCap',0.00398525),
('interestExpense/marketCap',0.00800572),
('depreciationAndAmortization/marketCap',0.0268882),
('ebitda/marketCap',0.0181224),
('operatingIncome/marketCap',0.0123721),
('incomeBeforeTax/marketCap',0.0214638),
('netIncome/marketCap',0.0149753),
('cashAndCashEquivalents/marketCap',0.0219313),
('inventory/marketCap',0.013917),
('totalCurrentAssets/marketCap',0.0165789),
('totalNonCurrentAssets/marketCap',0.0172143),
('totalAssets/marketCap',0.0161724),
('shortTermDebt/marketCap',0.007359),
('totalCurrentLiabilities/marketCap',0.0285901),
('totalNonCurrentLiabilities/marketCap',0.011399),
('totalStockholdersEquity/marketCap',0.0191194),
('netCashProvidedByOperatingActivities/marketCap',0.0238669),
('netCashUsedForInvestingActivites/marketCap',0.0200285),
('debtRepayment/marketCap',0.0105517),
('commonStockIssued/marketCap',0.0118695),
('commonStockRepurchased/marketCap',0.0070691),
('dividendsPaid/marketCap',0.0529508),
('netCashUsedProvidedByFinancingActivities/marketCap',0.0169544),
('netChangeInCash/marketCap',0.0225456),
('freeCashFlow/marketCap',0.0203277),
('Marketcap growth rate',0.0420275),
('grossProfit/marketCap change',0.0131221),
('operatingExpenses/marketCap change',0.0145099),
('interestIncome/marketCap change',0.0165819),
('interestExpense/marketCap change',0.0212875),
('depreciationAndAmortization/marketCap change',0.0107112),
('ebitda/marketCap change',0.00936889),
('operatingIncome/marketCap change',0.0107315),
('incomeBeforeTax/marketCap change',0.00884426),
('netIncome/marketCap change',0.012534),
('cashAndCashEquivalents/marketCap change',0.0139102),
('inventory/marketCap change',0.00687619),
('totalCurrentAssets/marketCap change',0.0148246),
('totalNonCurrentAssets/marketCap change',0.0109129),
('totalAssets/marketCap change',0.00345596),
('shortTermDebt/marketCap change',0.0120053),
('totalCurrentLiabilities/marketCap change',0.0083218),
('totalNonCurrentLiabilities/marketCap change',0.011033),
('totalStockholdersEquity/marketCap change',0.0158731),
('netCashProvidedByOperatingActivities/marketCap change',0.00951752),
('netCashUsedForInvestingActivites/marketCap change',0.014635),
('debtRepayment/marketCap change',0.0208268),
('commonStockIssued/marketCap change',0.0143767),
('commonStockRepurchased/marketCap change',0.00968006),
('dividendsPaid/marketCap change',0.0242374),
('netCashUsedProvidedByFinancingActivities/marketCap change',0.0151674),
('netChangeInCash/marketCap change',0.0118539),
('freeCashFlow/marketCap change',0.015484),
('marketCap/CPI',0.0172897),
('longTermDebt/marketCap/ThirtyYearFixedRateMortgageAverage',0.010322),
('longTermDebt/marketCap/ThirtyYearFixedRateMortgageAverage change',0.0145402),
('revenue/marketCap change / industrialProductionTotalIndex growth',0.041033)]

sorted_list = sorted(unsorted_list, key=operator.itemgetter(1), reverse=True)

features_sorted = []
importance_sorted = []

for i in sorted_list:
    features_sorted += [i[0]]
    importance_sorted += [i[1]]

features_sorted.reverse()
importance_sorted.reverse()

plt.rcParams['figure.figsize'] = [15, 12]

fig, ax = plt.subplots()
bars = ax.barh(features_sorted,importance_sorted)
ax.bar_label(bars, fmt = '%.1e')

#plt.barh(y, Nevt)
#plt.yticks(y, decay)

plt.xlabel("Variable Importance")
plt.ylabel("Variable")
plt.grid(True, axis = "x", linestyle="--")

plt.savefig("Var_importance.png", bbox_inches='tight')
