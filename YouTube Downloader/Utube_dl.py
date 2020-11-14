# This is a youtube-downloader that uses qdownloader
# Made by Hossein Zamani Nasab

import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

utube_url = input('Insert link: ')

# Phase 1
# Selenium
website_url = 'https://qdownloader.io/'
driver = webdriver.Chrome()  # Download and install chrome webdriver from official site(https://chromedriver.chromium.org/downloads)
driver.set_window_position(-106000, 0)  # Hide windows from our sight
driver.get(website_url)
url = driver.find_element_by_class_name('url-input')  # Find the box to insert utube_url
url.send_keys(utube_url)
driver.find_element_by_id('downloadBtn').click()  # Click on the download button
time.sleep(5)  # We need time to our download page loaded, change that time considering speed of your connection
get_url = driver.current_url  # When we click on download button, we got new url, for scraping we need the new one

# Phase 2
# Request
req = requests.get(get_url)
soup = BeautifulSoup(req.text, 'html.parser')
tables = soup.find_all('div', {'class': 'col-md-8'})

# Phase 3
# Panda
tabs_dic = {}
for table in tables:
    tab_data = [[cell.text for cell in row.find_all(["th", "td"])] for row in table.find_all("tr")]
    df = pd.DataFrame(tab_data)
    tabs_dic = df
print(f'---------------------------------------------------------------------------------------------\n|The first row'
      f' of QFSD(Quality Format Size Downloads) is for \'Download Video with Sound\', middle one is for \'Download'
      f' Audio Only\' and the last one is for \'Download Video without Sound\'|\n----------------------------------'
      f'-----------------------------------------------------------\n{tabs_dic}')

# Phase 4
# Get title and download links
print('-------------------------------------------------')
num = 1
for links in soup.select('td > a'):  # Grab only target link
    title_link = []
    title = links.get_attribute_list('download')
    get_link = links.get_attribute_list('href')
    title_link.append(title)
    title_link.append(get_link)
    print(f'({num})\n-----------\n|The title|\n-----------\n{title_link[0]}\n\n***************\n|Download link|\n****'
          f'***********\n{title_link[1]}')
    num += 1
    print('----------------------------------------------------------------------------------------------------------'
          '--------------------------------------------')
driver.close()
