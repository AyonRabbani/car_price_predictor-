#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 08:53:09 2019

@author: ayonrab
"""

from bs4 import BeautifulSoup
import csv 
import requests 

def get_page(url): 
    response = requests.get(url)
    
    if not response.ok: 
        print('Server responded:', response.status_code)
    else: 
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

def get_data(soup): 
    #Car year, brand, model
    try: 
        car_info = soup.find('h1', class_ = "cui-heading-2--secondary vehicle-info__title").text.strip().split()
        year = car_info[0]
        brand = car_info[1]
        model = car_info[2]
    except: 
        year = ''
        brand = ''
        model = '' 
    
    #mileage
    try: 
        mileage = soup.find('div', class_= "vdp-cap-price__mileage--mobile vehicle-info__mileage").text.strip().split()
        mileage = mileage[0]
    except: 
        mileage = ''
    
    #price
    
    try: 
        price = soup.find('span', class_ = "vehicle-info__price-display").text
    except: 
        price = '' 
    
    #engine
    try: 
        table_info = [item.text.strip().split() for item in soup.find_all('li', class_ = 'vdp-details-basics__item')]
        engine = ' '.join(table_info[8])
    except: 
        engine = ''
        
    
    #features 
    try: 
        #features = [info.text.strip() for info in soup.find('ul', class_ = 'vdp-details-basics__features-list')]
        features = [s.text.strip() for s in soup.find_all('ul', class_='vdp-details-basics__features-list')]
        features = [row.replace('\n', ',') for row in features]
        
    except:
        features = ''
        
    data = {
            'Year' : year, 
            'Brand' : brand, 
            'Model' : model, 
            'Mileage' : mileage, 
            'Engine' : engine,
            'Price' : price,
            'Features' : features, 
            }
    
    return data

def get_url_index(soup): 
    #get all car links on page 
    links = soup.find_all('a', class_ = 'shop-srp-listings__listing')
    
    href_list = [link.get('href') for link in links]
    
    car_links = ["https://www.cars.com" + href for href in href_list]
    
    return car_links

def csv_writer(data): 
    with open('car_inventory_lot.csv', 'a') as csvfile: 
        writer = csv.writer(csvfile)

        row = [data['Year'], data['Brand'], data['Model'], data['Mileage'], data['Engine'],data['Price'],  data['Features']]
        
        writer.writerow(row)
        
def main():
    #url = 'https://www.cars.com/for-sale/searchresults.action/?dealerType=localOnly&mdId=20606&mkId=20017&page=1&perPage=50&rd=50&sort=relevance&zc=20148'
    
    prime_url = 'https://www.cars.com/for-sale/searchresults.action/?dealerType=all&mdId=20606&mkId=20017&perPage=30&page='
    url_list = [ prime_url + str(number) for number in range (1, 20)]
    
    
    for page in url_list: 
        car_inventory = get_url_index(get_page(page))
        for car in car_inventory:
            data = get_data(get_page(car))
            csv_writer(data)
    
    
    

if __name__ == '__main__': 
    main()
