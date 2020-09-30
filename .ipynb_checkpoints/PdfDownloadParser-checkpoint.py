import os
import requests
from selenium import webdriver
import pandas as pd
import xlsxwriter
print(pd.__version__)
url = 'https://www.healthfacilityguidelines.com.au/standard-components'

browser = webdriver.Firefox()
browser.get(url)
table = []
drop_down_button = browser.find_element_by_xpath('//*[@id="block-ah-bootstrap-table-all-standard-components"]/div[1]/div[2]/div[1]/span[2]/span/button')
drop_down_button.click()
press_all = browser.find_element_by_xpath('//*[@id="block-ah-bootstrap-table-all-standard-components"]/div[1]/div[2]/div[1]/span[2]/span/ul/li[5]/a')
press_all.click()

for results in range(1,251):
    try:
        header = browser.find_element_by_xpath('//*[@id="all-standard-components"]/tbody/tr['+str(results)+']/td[1]/a')
        subtitle = browser.find_element_by_xpath('//*[@id="all-standard-components"]/tbody/tr['+str(results)+']/td[2]/a')
        excellink = browser.find_element_by_xpath('/html/body/div[3]/div/div/section/div/div[2]/section[3]/div[1]/div[3]/div[2]/table/tbody/tr['+str(results)+']/td[3]/div[2]/div/div/div/div/span/a')
        table.append([header.text,subtitle.text,excellink.get_attribute('href')])
    except:
        pass

browser.quit()

rowcount = 0
database_fn = 'AUSHFG_MGAS_Database.xlsx'

df = pd.DataFrame()

if not os.path.exists(str(os.getcwd()) + '/Downloads/'):
    os.mkdir(str(os.getcwd()) + '/Downloads/')

for index,url in enumerate(table):
    local_filename = str(os.getcwd()) + '/Downloads/' + str(url[0]) + '.xlsx'
    r = requests.get(url[2],local_filename)
    f = open(local_filename,'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:
            f.write(chunk)
    df = df.append(pd.read_excel(local_filename, sheet_name=1, index_col=False, skiprows=6), ignore_index = True)

mgas = df[df['Item Number'].str.contains('MGAS-')]
mege = df[df['Name'].str.contains('oxygen depletion')]
mgfp001 = df[df['Item Number'].str.contains('MGFP-001')]
mgfp007 = df['Item Number'].str.contains('MGFP-007'])
mgfp = mgfp001.append(mgfp007, ignore_index = True)
master_list = mgas.append([mege, mgfp], ignore_index = True)
master_list.sort_values(by = 'AusHFG Room Code', inplace = True)
master_list.to_excel(os.getcwd()+'\\aushfg_mg_items.xlsx', index = False, engine = 'xlsxwriter')
