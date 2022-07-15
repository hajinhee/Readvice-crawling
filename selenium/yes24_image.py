from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request
import pandas as pd
import re

import time

import urllib3


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
url = "http://www.yes24.com/24/Category/BestSeller"
driver.get(url)
driver.maximize_window()

'''
경제/경영 3, 만화/라이트노벨 6, 소설/시/희곡 8, 어린이 10, 에세이 11, 여행 12, 
유아 15, 자기계발 18, IT 모바일 24
'''
categoreis = ['3', '6', '8', '10', '11', '12', '15', '18', '24']


# 장르 클릭
for category in categoreis:
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div/div[2]/div[1]/div[1]/ul/li[1]/ul/li[{category}]/a'))).click()
    # 페이지 클릭
    for page in range(1, 12):
        try:
            # driver.find_element(By.XPATH,f'/html/body/div/div[2]/div[2]/div[3]/div[1]/div[1]/p/a[{page}]').click() 
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="bestList"]/div[3]/div[1]/div[1]/p/a[{page}]'))).click()
            # 도서 클릭
            for i in range(1, 40, 2):
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="category_layout"]/tbody/tr[{i}]/td[3]/p[1]/a[1]'))).click()
                # 이미지, 제목 추출
                imgUrl = driver.find_element(By.XPATH, '/html/body/div/div[4]/div[1]/div/span/em/img').get_attribute('src')
                title = driver.find_element(By.XPATH, '/html/body/div/div[4]/div[1]/div/span/em/img').get_attribute('alt')
                # 이미지 저장 및 리스트에 제목 추가
                title2 = re.sub('[\/:*?"<>|]','',title)
                urllib.request.urlretrieve(imgUrl, f'save/image/{title2}.jpg')
                # title_list.append(title)
                time.sleep(2)

                # 뒤로 가기
                driver.back()
        except:
            continue
        
       
# 텍스트 저장
# pd.DataFrame(title_list).to_csv('save/title.csv', index=False)