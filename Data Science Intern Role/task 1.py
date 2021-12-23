# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 16:52:59 2021

@author: CSpanias
"""

"""
 Part 1

    "You are given three files by a client:\n",
    " - 'Transactions.csv' contains a list of transactions for a bank,\n",
    " - 'EUR Exchange Rates.csv' contains a list of Euro to Pound Sterling exchange rates,\n",
    " - 'USD Exchange Rates.csv' contains a list of US Dollar to Pound Sterling exchange rates.\n",
    " \n",
    "The client has asked for monthly forecasts of their data.\n",
    "\n",
    "Your task is to clean and transform these files before they can be used for analysis.\n",
    "\n",
    "Please produce a single csv file covering the period Jan-2015 to Feb-2019 with column headings:\n",
    " - Calendar Month\n",
    " - Sum of Withdrawals (GBP)\n",
    " - Sum of Deposits (GBP)\n",
    " - Number of Transactions\n",
    " - Account Balance for each account (GBP)\n",
    " \n",
    "You may assume that the Account Balance is zero on 31-Dec-2014."
"""

import pandas as pd
import numpy as np
import datetime
import seaborn as sns

# importing csv files as dataframes
transactions =  pd.read_csv(r"C:\Users\10inm\Desktop\Data Science Interview Tasks\Transactions.csv")
euro_rates = pd.read_csv(r"C:\Users\10inm\Desktop\Data Science Interview Tasks\EUR_Exchange_Rates.csv")
usd_rates = pd.read_csv(r"C:\Users\10inm\Desktop\Data Science Interview Tasks\USD_Exchange_Rates.csv")

# take a look at the dataframes
transactions.head()
transactions.shape

euro_rates.head()
euro_rates.shape

usd_rates.head()
usd_rates.shape

# check the amount of missing values per column
transactions.isnull().sum() # one missing value at "WITHDRAWAL" column
euro_rates.isnull().sum() # none
usd_rates.isnull().sum() # none

# locate the missing value to figure out why it is missing (if possible)
np.where(transactions["WITHDRAWAL AMT"].isnull())[0]
transactions.iloc[34450,:]

# remove row with the missing value
transactions = transactions.dropna()

# checking the dates column types
transactions["DATE"]
euro_rates["Date"]
usd_rates["Date"]

# date columns are "objects", thus we must parse them
transactions["dates_parsed"] = pd.to_datetime(transactions["DATE"], infer_datetime_format = True)
euro_rates["dates_parsed"] = pd.to_datetime(euro_rates["Date"], infer_datetime_format = True)
usd_rates["dates_parsed"] = pd.to_datetime(usd_rates["Date"], infer_datetime_format = True)

# plot the day of the month to check the date parsing (i.e., values in the range of 1-31)
sns.distplot(transactions["dates_parsed"].dt.day, kde = False, bins = 31)
sns.distplot(euro_rates["dates_parsed"].dt.day, kde = False, bins = 31)
sns.distplot(usd_rates["dates_parsed"].dt.day, kde = False, bins = 31)

# select the date range required
start_date = '2015-01-01'
end_date = '2019-02-28'

mask = (transactions['dates_parsed'] > start_date) & (transactions['dates_parsed'] <= end_date)
trans_jan15tofeb19 = transactions.loc[mask]

mask = (euro_rates['dates_parsed'] > start_date) & (euro_rates['dates_parsed'] <= end_date)
euro_rates_jan15tofeb19 = euro_rates.loc[mask]

mask = (usd_rates['dates_parsed'] > start_date) & (usd_rates['dates_parsed'] <= end_date)
usd_rates_jan15tofeb19 = usd_rates.loc[mask]

# combine the rate dataframes while dropping the date column
euro_rates_jan15tofeb19 = euro_rates_jan15tofeb19.drop("Date", 1)
usd_rates_jan15tofeb19 = usd_rates_jan15tofeb19.drop("Date", 1)
trans_jan15tofeb19 = trans_jan15tofeb19.drop("DATE", 1)

rates_merge = pd.merge(euro_rates_jan15tofeb19, usd_rates_jan15tofeb19, how='inner')
df_merge = pd.merge(rates_merge, trans_jan15tofeb19, how="inner")

df_combined = rates_combined.set_index("dates_parsed").join(trans_jan15tofeb19.set_index("dates_parsed"))
df_combined = pd.merge(trans_jan15tofeb19, rates_combined, how='inner', left_on = 'Id', right_on = 'Id')

# converting str columns to numeric
trans_jan15tofeb19['WITHDRAWAL AMT'].apply(type)
trans_jan15tofeb19['WITHDRAWAL AMT'] = trans_jan15tofeb19['WITHDRAWAL AMT'].str.replace('$', '')
pd.to_numeric(trans_jan15tofeb19["WITHDRAWAL AMT"])
pd.to_numeric(trans_jan15tofeb19["DEPOSIT AMT"])

# group by month
test = trans_jan15tofeb19['dates_parsed'].dt.date.value_counts().rename('sum').to_frame()
test = trans_jan15tofeb19['dates_parsed'].dt.date.value_counts().rename('mean').to_frame()
