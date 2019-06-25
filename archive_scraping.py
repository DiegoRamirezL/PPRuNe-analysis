#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 15:52:44 2019

@author: maxence.faldor
"""

# Beginning of scraping 2019-05-29 13:30

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
import dateparser

def my_get(url):
    try:
        return requests.get(url)
    except:
        time.sleep(60)
        return requests.get(url)

# Create empty dataframes
thread = pd.DataFrame(columns = ['name', 'url'])
index_thread = 0

post = pd.DataFrame(columns = ['index_thread', 'user', 'date', 'content'])
index_post = 0

# Define base url
base_url = 'https://www.pprune.org/archive/index.php/'

# Define the specific forum to scrape
forum = 'f-15'

suffix = '.html'

# Request html page
r = my_get(base_url + forum + suffix)

# Read the html
soup = BeautifulSoup(r.text, 'html.parser')

try:
    page_number_max = int(soup.find('div', {'id': 'pagenumbers'}).find_all('a')[-1].get_text())
except:
    page_number_max = 1

page_number_min = 30

for page_number in range(page_number_min, page_number_max + 1):
    print('[+] Scraping page number ' + str(page_number))
    
    # Request html page
    r = my_get(base_url + forum + '-p-' + str(page_number) + '.html')
    
    # Read the html
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Get content
    soup_threads = soup.find('div', {'id': 'content'}).find_all('a')
    
    for soup_thread in soup_threads:
        name = soup_thread.get_text()
        url = soup_thread['href']
        
        # Request html page
        r = my_get(url)
        
        # Read the html
        soup = BeautifulSoup(r.text, 'html.parser')
        
        try:
            page_number_thread_max = int(soup.find('div', {'id': 'pagenumbers'}).find_all('a')[-1].get_text())
        except:
            page_number_thread_max = 1
        
        page_number_thread = 1
        while True:
            time.sleep(1)
            soup_posts = soup.find_all('div', {'class': 'post'})
            
            for soup_post in soup_posts:
                user = soup_post.find("div", {'class': 'username'}).get_text()
                date = dateparser.parse(soup_post.find("div", {'class': 'date'}).get_text())
                content = soup_post.find('div', {'class': 'posttext'}).get_text().encode('ascii', 'ignore').decode('utf-8', errors = 'surrogatepass')
                
                post.loc[index_post] = [index_thread, user, date, content]
                index_post += 1
                
            if page_number_thread == page_number_thread_max:
                break
            else:
                page_number_thread += 1
                r = my_get(url[:-5] + '-p-' + str(page_number_thread) + '.html')
                soup = BeautifulSoup(r.text, 'html.parser')
        
        if index_thread % 25 == 0:
            print('\tthread : ' + name)
            
        thread.loc[index_thread] = [name, url]
        index_thread += 1


writer = pd.ExcelWriter(r'./pprune_scraping_1.xlsx', engine='xlsxwriter')
thread.to_excel(writer, sheet_name='thread', index=False)
post.to_excel(writer, sheet_name='post', index=False)
writer.save()
writer.close()
