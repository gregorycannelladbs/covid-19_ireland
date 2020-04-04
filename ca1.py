# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 21:07:24 2020

@author: Greg
"""

import requests
import csv
from bs4 import BeautifulSoup      

def missing_values(lst):
    indexes = sorted(list(range(3,50,5)) + list(range(4,50,5))) 
    for i in indexes:
        lst.insert(i, 0)
    return lst

def to_matrix(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

def save_csv(matrix, path = "output.csv"):
    with open(path, "w", newline="",  encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(matrix)
        f.close()

def get_soup():
    headers = {
        'authority': 'en.wikipedia.org',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'sec-fetch-dest': 'document',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,fr;q=0.7',
        'cookie': 'WMF-Last-Access=24-Mar-2020; WMF-Last-Access-Global=24-Mar-2020; GeoIP=IE:L:Dublin:53.33:-6.25:v4; enwikimwuser-sessionId=e6872356b36439c013de',
    }
    
    response = requests.get('https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_Republic_of_Ireland', headers=headers)
    soup = BeautifulSoup(response.content, features="html.parser")
    return soup

def get_data(soup):
    tables = soup.find_all("table")
    table = tables[2] 
    
    header = ["Date", "num_cases", "growth_cases", "num_deaths", "growth_death"]
    data = []
    for tr in table.find_all("tr"):
        for td in tr.find_all("td"):
            # get the values of the header + the first column values
            td_clean = str(td.string).strip().replace("\n", "")
            # get rid of the header and only keep first column values
            if td_clean not in ("None", "Date", "# of cases", "# of deaths"):
                # replace the funny value "⋮" by "-" and append values to list
                data.append(td_clean.replace("⋮", "-"))          
            
            # get the last 4 column values
            for span in td.find_all("span"):
                span = str(span.string).strip().replace("\n", "")
                # remove unnecessary "None" values
                if span != "None":
                    # replace non numerical values by their numerical equivalent which is 0
                    if span in ("(n.a.)", "(=)"): 
                       data.append(0)
                    # convert non numerical percentages to numerical equivalent
                    elif span[0] == "(": 
                        data.append(float(span[2:len(span)-2]) / 100)
                    # remove the thousands separator
                    else: 
                        span = span.replace(",", "")
                        data.append(eval(span))

    data = missing_values(data) # insert 0 in missing value indexes
    data = header + data  # add custom header at the beginning of the list
    return data

def main():
    soup = get_soup()
    data = get_data(soup)
    matrix = to_matrix(data, 5) # convert list to matrix composed of 5 columns
    save_csv(matrix)

main()