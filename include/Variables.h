#ifndef VARIABLES_H
#define VARIABLES_H

#include <vector>
#include <string>

std::vector<std::string> input_variables_names = {
    // income
    "revenue/marketCap", "netIncome/marketCap",

    // balance
    "totalCurrentAssets/marketCap", "ebitda/marketCap", "totalStockholdersEquity/marketCap", "shortTermDebt/marketCap", "longTermDebt/marketCap",
    "totalCurrentLiabilities/marketCap",

    // cash flow
    "operatingCashFlow/marketCap", "freeCashFlow/marketCap", "dividendsPaid/marketCap",

    // growth of market cap
    "Marketcap growth rate",

    // change of stock
    "changestock",

    // income growth 
    "revenue/marketCap change", "netIncome/marketCap change",

    // balance growth
    "totalCurrentAssets/marketCap change", "ebitda/marketCap change", "totalStockholdersEquity/marketCap change", "shortTermDebt/marketCap change", "longTermDebt/marketCap change",
    "totalCurrentLiabilities/marketCap change",

    // cash flow growth
    "operatingCashFlow/marketCap change", "freeCashFlow/marketCap change", "dividendsPaid/marketCap change"

    /*
    // income
    "revenue/marketCap", "grossProfit/marketCap", "operatingExpenses/marketCap", "interestIncome/marketCap", "interestExpense/marketCap",
    "depreciationAndAmortization/marketCap", "ebitda/marketCap", "operatingIncome/marketCap", "incomeBeforeTax/marketCap", "netIncome/marketCap",

    // balance
    "cashAndCashEquivalents/marketCap", "inventory/marketCap", 
    "totalCurrentAssets/marketCap", "totalNonCurrentAssets/marketCap", "totalAssets/marketCap","shortTermDebt/marketCap", 
    "totalCurrentLiabilities/marketCap", "longTermDebt/marketCap", "totalNonCurrentLiabilities/marketCap", "totalStockholdersEquity/marketCap",

    // cash flow
    "netCashProvidedByOperatingActivities/marketCap", "netCashUsedForInvestingActivites/marketCap", "debtRepayment/marketCap",
    "commonStockIssued/marketCap", "commonStockRepurchased/marketCap", "dividendsPaid/marketCap", "netCashUsedProvidedByFinancingActivities/marketCap",
    "netChangeInCash/marketCap", 
    //"operatingCashFlow/marketCap", 
    "freeCashFlow/marketCap",

    // growth of market cap
    "Marketcap growth rate", 

    // growth of income
    "revenue/marketCap change", "grossProfit/marketCap change", "operatingExpenses/marketCap change", "interestIncome/marketCap change",
    "interestExpense/marketCap change", "depreciationAndAmortization/marketCap change", "ebitda/marketCap change","operatingIncome/marketCap change", 
    "incomeBeforeTax/marketCap change", "netIncome/marketCap change",

    // growth of balance
    "cashAndCashEquivalents/marketCap change", "inventory/marketCap change", "totalCurrentAssets/marketCap change", "totalNonCurrentAssets/marketCap change", 
    "totalAssets/marketCap change", "shortTermDebt/marketCap change", "totalCurrentLiabilities/marketCap change","longTermDebt/marketCap change", 
    "totalNonCurrentLiabilities/marketCap change", "totalStockholdersEquity/marketCap change",

    // growth of cash flow
    "netCashProvidedByOperatingActivities/marketCap change", "netCashUsedForInvestingActivites/marketCap change","debtRepayment/marketCap change", 
    "commonStockIssued/marketCap change", "commonStockRepurchased/marketCap change","dividendsPaid/marketCap change", 
    "netCashUsedProvidedByFinancingActivities/marketCap change", "netChangeInCash/marketCap change", 
    //"operatingCashFlow/marketCap change",
    "freeCashFlow/marketCap change"
    */
};

#endif 