from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import pandas as pd
from icecream import ic 

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
url = "http://www.yes24.com/24/Category/BestSeller"
driver.get(url)
driver.maximize_window()

'''
건강/취미 2, 경제/경영 3, 소설/시/희곡 8, 에세이 11, 여행 12, IT모바일 24
'''

categoreis = ['2', '3', '8', '11', '12', '18', '24']
list = []

# 장르 클릭
for category in categoreis:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div/div[2]/div[1]/div[1]/ul/li[1]/ul/li[{category}]/a'))).click()
    # 페이지 클릭
    for page in range(1, 6):
        try:
            # driver.find_element(By.XPATH,f'/html/body/div/div[2]/div[2]/div[3]/div[1]/div[1]/p/a[{page}]').click() 
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="bestList"]/div[3]/div[1]/div[1]/p/a[{page}]'))).click()
            # 도서 클릭
            for i in range(1, 40, 2):
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="category_layout"]/tbody/tr[{i}]/td[3]/p[1]/a[1]'))).click()
                # isbn 추출
                isbn = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'#infoset_specific > div.infoSetCont_wrap > div > table > tbody > tr:nth-child(3) > td'))).text
                title = driver.find_element(By.XPATH, '/html/body/div/div[4]/div[1]/div/span/em/img').get_attribute('alt')
                # isbn 저장
                list.append(isbn)
                list.append(title)
                time.sleep(2)
                # 뒤로 가기
                driver.back()
        except:
            continue
        
       
# 텍스트 저장
dict = {list[i]: list[i + 1] for i in range(0, len(list), 2)}
with open('save/isbn.csv', 'w', encoding='UTF-8') as f:
    w = csv.writer(f)
    w.writerow(dict.keys())
    w.writerow(dict.values())

ic(pd.read_csv('save/isbn.csv'))


