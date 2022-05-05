# -*- coding: utf-8 -*-
"""
Created on Tue May  3 20:49:41 2022

@author: akile
"""

from py5paisa import FivePaisaClient
from smartapi import SmartConnect
from datetime import date
from datetime import timedelta

import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read("data/config.ini")

cred = {
    "APP_NAME": config["5Paisa_Keys"]["app_name"],
    "APP_SOURCE": config["5Paisa_Keys"]["app_source"],
    "USER_ID": config["5Paisa_Keys"]["user_id"],
    "PASSWORD": config["5Paisa_Keys"]["password"],
    "USER_KEY": config["5Paisa_Keys"]["user_key"],
    "ENCRYPTION_KEY": config["5Paisa_Keys"]["encryption_key"],
}

client = FivePaisaClient(
    email=config["5Paisa_Keys"]["account_email"],
    passwd=config["5Paisa_Keys"]["account_password"],
    dob=config["5Paisa_Keys"]["account_dob"],
    cred=cred,
)
client.login()

# obj = SmartConnect(api_key=config["AngelOne_Keys"]["api_key"])
# data = obj.generateSession(
#     config["AngelOne_Keys"]["client_id"], config["AngelOne_Keys"]["passwd"]
# )

# data = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"

script_table = pd.read_csv("data/scripmaster-csv-format.csv")
script_table = script_table[(script_table.Exch == "N") & (script_table.Series == "EQ")]

nifty_scrips = pd.read_csv("data/from_nse/ind_nifty50list.csv")
bnf_scrips = pd.read_csv("data/from_nse/ind_niftybanklist.csv")

nifty_scrips = pd.merge(
    nifty_scrips,
    script_table[["Name", "Scripcode"]],
    how="left",
    left_on="Symbol",
    right_on="Name",
)

# historical_data(<Exchange>,<Exchange Type>,<Scrip Code>,<Time Frame>,<From Data>,<To Date>)

df = client.historical_data(
    "N",
    "C",
    1660,
    "1d",
    date.today().strftime("%Y-%m-%d"),
    date.today().strftime("%Y-%m-%d"),
)
print(df)

# Note : TimeFrame Should be from this list ['1m','5m','10m','15m','30m','60m','1d']
