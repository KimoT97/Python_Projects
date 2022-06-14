# -*- coding: utf-8 -*-
"""
Created on Thu May 19 01:21:34 2022

@author: mrkim
"""

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
#import cookielib
from urllib.request import build_opener, HTTPCookieProcessor, Request, urlopen
import requests
import re
import time
import random

PATH= "D:\python\chromedriver.exe"
driver=webdriver.Chrome(PATH)
driver.get("https://www.amazon.com/")
driver.implicitly_wait(5)
search=driver.find_element(by=By.ID, value="twotabsearchtextbox")
search.send_keys("Gaming Laptops")
search.send_keys(Keys.RETURN)
driver.implicitly_wait(5)
max_price=driver.find_element(by=By.ID, value="high-price")
max_price.send_keys("1500")
Go_button=driver.find_element(by=By.CLASS_NAME, value="a-button-input")
Go_button.send_keys(Keys.RETURN)
html=driver.page_source
Buttons_bottom=list(driver.find_elements(by=By.CLASS_NAME, value="s-pagination-item"))
Next_button=Buttons_bottom[-1]
pages_num=(Buttons_bottom[-2].text)
# driver.implicitly_wait(5)
# items=driver.find_elements(by=By.CLASS_NAME, value="s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col s-widget-spacing-small sg-col-12-of-16s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col s-widget-spacing-small sg-col-12-of-16")
# for i, item in enumerate(items):
#     items[i].click()
#     driver.implicitly_wait(5)
#     driver.back()
#     time.sleep(3)
#     items=driver.find_elements(by=By.CLASS_NAME, value="s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col s-widget-spacing-small sg-col-12-of-16")
#soup=BeautifulSoup(html, 'lxml')
#products1=soup.find_all('div', {'class':'s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'})
products_list=[]
for num in range(int(pages_num)-1):
    html=driver.page_source
    soup=BeautifulSoup(html, 'lxml')
    products_list.append(soup.find_all('div', {'class':'s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'}))
    #time.sleep(3)
    Next_button=list(driver.find_elements(by=By.CLASS_NAME, value="s-pagination-item"))[-1]
    Next_button.send_keys(Keys.RETURN)
    time.sleep(7)

html=driver.page_source
soup=BeautifulSoup(html, 'lxml')
products_list.append(soup.find_all('div', {'class':'s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'}))
products_list_final  = [val for sublist in products_list for val in sublist]

specs=[]
price=[]
reviews=[]
num_of_reviewers=[]
urls=[]
img_urls=[]

for i, product in enumerate(products_list_final):
    try:
        specs.append(products_list_final[i].find_all('span', {'class':'a-size-medium a-color-base a-text-normal'})[0].get_text())
    except:
        specs.append(np.nan)
    try:
        price.append(products_list_final[i].find_all('span', {'class':'a-offscreen'})[0].get_text())
    except:
        price.append(np.nan)
    try:
        reviews.append((products_list_final[i].find_all('span', {'class':'a-icon-alt'})[0].get_text()).replace(' out of 5 stars',''))
    except:
        reviews.append(np.nan)
    try:
        num_of_reviewers.append(products_list_final[i].find_all('span', {'aria-label':True})[1].get_text())
    except:
        num_of_reviewers.append(np.nan)
    try:
        link=(products_list_final[i].find_all('a', {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style'}))
        if len(link)==0:
            link=products_list_final[i].find_all('a', {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        urls.append(("https://www.amazon.com")+(re.findall("href=(.+);", str(link))[0].replace('"','')))
    except:
        urls.append(np.nan)    
    try:
        img_link=(products_list_final[i].find_all('div', {'class':'s-image-fixed-height'}))
        img_urls.append(re.findall("2.5x, (.*)? 3x", str(img_link))[0])
    except:
        img_urls.append(np.nan) 
    
    
specs_table=[]
for i, laptop in enumerate(urls):
    try:
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        #proxies_list = ["128.199.109.241:8080","113.53.230.195:3128","125.141.200.53:80","125.141.200.14:80","128.199.200.112:138","149.56.123.99:3128","128.199.200.112:80","125.141.200.39:80","134.213.29.202:4444"]
        #proxies = {'https': random.choice(proxies_list)}
        time.sleep(0.7 * random.random())
        #r = requests.get(laptop, headers=headers, proxies=proxies)
        #html_page = r.content                       
        opener = build_opener(HTTPCookieProcessor())
        #req = Request(laptop, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81'})
        req = Request(laptop, headers=headers,) 
        response = opener.open(req, timeout=30)
        html_page = response.read()
        #html_page = urlopen(req).read()
        soup2 = BeautifulSoup(html_page, 'html.parser')
        specs_final=(soup2.find_all('div', {'class':['a-section a-spacing-small a-spacing-top-small']})[0].get_text().split('    '),1)
        specs_final=specs_final[0]
        specs_final.pop(0)
        specs_final.pop(-1)
        specs_final2=[z.split('   ', 1) for z in specs_final]
        specs_final3=dict(specs_final2)
        #specs_final2 = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
        
        specs_table.append(specs_final3)
        print((int(i/len(urls)*100)),'%')
    except:
        specs_table.append({'Nan': np.nan})
        print(laptop)
        print((int(i/len(urls)*100)),'%')
#res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    
####################################################################
#Cleaning Data
####################################################################
df_laptops=pd.DataFrame(specs_table)
df_laptops['Title']=specs
df_laptops['Reviews']=reviews
df_laptops['Review Count']=num_of_reviewers
df_laptops['Image']=img_urls
df_laptops['Price']=price
df_laptops['Brand']=df_laptops['Brand'].fillna(df_laptops[' Brand'])
df_laptops[' Operating System']=df_laptops[' Operating System'].fillna(df_laptops['Operating System'])
df_laptops.drop(' Brand', inplace=True, axis=1)
df_laptops.drop('Operating System', inplace=True, axis=1)
df_laptops[' Card Description']=df_laptops[' Card Description'].fillna(df_laptops['  Card Description'])
df_laptops.drop('  Card Description', inplace=True, axis=1)
df_laptops[' Series']=df_laptops[' Series'].fillna(df_laptops['Series'])
df_laptops.drop('Series', inplace=True, axis=1)
df_laptops[' Card Description']=df_laptops[' Card Description'].fillna(df_laptops[' Graphics Card Description'])
df_laptops.drop(' Graphics Card Description', inplace=True, axis=1)
try:
    df_laptops[' Model Name']=df_laptops[' Model Name'].fillna(df_laptops['Model Name'])
    df_laptops.drop('Model Name', inplace=True, axis=1)
except:
    pass
df_laptops.drop(df_laptops.iloc[:, 22:32], inplace = True, axis = 1)
df_laptops.drop(df_laptops.iloc[:, 17:20], inplace = True, axis = 1)
df_laptops.drop(df_laptops.iloc[:, 15:16], inplace = True, axis = 1)
df_laptops.drop(df_laptops.iloc[:, 12:13], inplace = True, axis = 1)
col_old=df_laptops.columns
col_new=[]
for col in col_old:
    col_new.append(col.strip(' '))
df_laptops.columns=col_new
df_laptops.to_csv('Gaming_Laptops_under_1500.csv', index=False)




