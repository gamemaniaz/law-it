from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time, re, pprint, csv, string, math

browser = webdriver.Chrome()
browser.get('https://www.mlaw.gov.sg/eservices/lsra/search-lawyer-or-law-firm/')
WAIT_TIME = 180

alphabets = list(string.ascii_uppercase)
keys = ['name','job_title','key_practice_areas','name_of_law_prac','admission_date','law_prac_type','email','website','tel','address']

page_size_element = WebDriverWait(browser, WAIT_TIME).until(
    EC.visibility_of_element_located((By.ID, 'PageSize'))
)
Select(page_size_element).select_by_visible_text('50')

def loadmask():
    WebDriverWait(browser, WAIT_TIME).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.loadmask'))
    )
    WebDriverWait(browser, WAIT_TIME).until_not(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.loadmask'))
    )

loadmask()

for i in range(1, 27):
    letter = alphabets[i-1]
    print(letter, end=' ')
    xpath = '//*[@id="alphabet"]/div/a[%d]' % i
    alphabet_element = WebDriverWait(browser, WAIT_TIME).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    alphabet_element.click()
    loadmask()
    num_records_text = browser.find_element_by_id('recordAmount').text
    start = num_records_text.index('(') + 1
    end = num_records_text.index(' ', start)
    num_records = int(num_records_text[start:end].replace(',', ''))
    num_pages = math.ceil(num_records / 50)
    for i in range(1, num_pages + 1):
        print(i, end=' ')
        data = []
        page_element = WebDriverWait(browser, WAIT_TIME).until(
            EC.element_to_be_clickable((By.ID, str(i)))
        )
        page_element.click()
        loadmask()
        while True:
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            page_element_html = soup.find(id=str(i))
            if 'active' in page_element_html['class']:
                break
            browser.implicitly_wait(2)
        main_table = soup.find(id='Tbl_Search')
        sub_tables = main_table.findAll("table", {"class": "lsra-search"})
        for t in sub_tables:
            tds = t.findAll('td')
            cell = {
                "name" : tds[1].text.replace(',', ''),
                "job_title" : tds[3].text.replace(',', ''),
                "admission_date": tds[4].text.replace(',', ''),
                "key_practice_areas" : tds[5].text.replace(',', '|'),
                "name_of_law_prac" : tds[7].text.replace(',', ''),
                "law_prac_type" : tds[8].text.replace(',', ''),
                "email" : tds[9].text.replace(',', ''),
                "website" : tds[10].text.replace(',', ''),
                "tel" : tds[11].text.replace('-', '').replace(',', ''),
                "address": re.sub(r'\s+', ' ', tds[13].text).replace(',', '')
            }
            data.append(cell)
        filename = letter + str(i) + '.csv'
        with open(filename, 'w') as f:
            keys_str = ','.join(keys)
            f.write(keys_str + '\n')
            for d in data:
                csv_str = ','.join([d[key] for key in keys])
                f.write(csv_str + '\n')
    print()

