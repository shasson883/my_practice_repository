# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 08:55:33 2020

@author: shass
"""

"Github Directory: https://github.com/shasson883/shasson883/blob/master/internetusers.py"

import pandas as pd
import requests
from bs4 import BeautifulSoup

def internet_users():

    headers = {
        'authority': 'www.nationmaster.com',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-dest': 'document',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cookie': '__utma=141835693.8164019.1586158875.1586158875.1586158875.1; __utmc=141835693; __utmz=141835693.1586158875.1.1.utmcsr=(direct)^|utmccn=(direct)^|utmcmd=(none); __utmb=141835693.1.10.1586158875; _hjid=661a334a-5ef3-4dd1-98f9-350a0cf9625b; trc_cookie_storage=taboola^%^2520global^%^253Auser-id^%^3D0b373ca4-c398-465c-a9fe-a2cef8f12a40-tuct4eacd1d; _hjIncludedInSample=1; __vliadb=1',
    }
    
    response = requests.get('https://www.nationmaster.com/country-info/stats/Media/Internet-users', headers=headers)
    
    soup = BeautifulSoup(response.content, features="html.parser")
    
    table = soup.find_all('table')[0] 
    df = pd.read_html(str(table))[0]
    countries = df["COUNTRY"].tolist()
    amount = df["AMOUNT"].tolist()
    date = df["DATE"].tolist()
    dict = {'COUNTRY':countries, 'AMOUNT':amount, 'DATE':date}
    df = pd.DataFrame(dict)
    df.to_csv('C:/Users/shass/Documents/Python/internetusers.csv', index = False)

if __name__ == "__main__":
    internet_users()
    print("Run Successfully")
    
