import os
import requests
from selenium import webdriver

url = 'https://www.healthfacilityguidelines.com.au/standard-components'
chromedriver = os.getcwd() + '\chromedriver'
browser = webdriver.Chrome(chromedriver)
browser.get(url)
table = []
drop_down_button = browser.find_element_by_xpath('//*[@id="block-ah-bootstrap-table-all-standard-components"]/div[1]/div[2]/div[1]/span[2]/span/button')
drop_down_button.click()
press_all = browser.find_element_by_xpath('//*[@id="block-ah-bootstrap-table-all-standard-components"]/div[1]/div[2]/div[1]/span[2]/span/ul/li[5]/a')
press_all.click()

for results in range(1,4):
    try:
        header = browser.find_element_by_xpath('//*[@id="all-standard-components"]/tbody/tr['+str(results)+']/td[1]/a')
        print(header.text + str(results))
        subtitle = browser.find_element_by_xpath('//*[@id="all-standard-components"]/tbody/tr['+str(results)+']/td[2]/a')
        pdf = browser.find_element_by_xpath('/html/body/div[3]/div/div/section/div/div[2]/section[3]/div[1]/div[3]/div[2]/table/tbody/tr['+str(results)+']/td[3]/div[1]/div/div/div/div/span/a')
        table.append([header.text,subtitle.text,pdf.get_attribute('href')])
    except:
        pass

browser.quit()

for index,url in enumerate(table):
    local_filename = str(os.getcwd()) + '/Downloads/' + str(url[0]) + '.pdf'
    r = requests.get(url[2],local_filename)
    f = open(local_filename,'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:
            f.write(chunk)

from tabula import read_pdf
import csv

with open('database.csv', 'a') as dcsv:
    csv_output = csv.writer(dcsv, delimiter=',', quotechar='"')
    for index,url in enumerate(table):
        local_filename = str(os.getcwd()) + '/Downloads/' + str(url[0]) + '.pdf'
        df = read_pdf(local_filename)
        csv_output.writerow(str(url[0]))
        csv_output.writerow('AusHFG Code,Description,Group,Qty,Comment')
        csv_output.writerow(df[df['AusHFG'].str.contains('MGAS')])
