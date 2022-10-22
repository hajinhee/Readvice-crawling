from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import re
import time
import pandas as pd


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
url = "http://www.yes24.com/24/Category/BestSeller"
driver.get(url)
driver.maximize_window()

'''
경제/경영 3, 소설/시/희곡 8, 에세이 11, 여행 12, IT 모바일 24
'''
categoreis = ['2', '3', '24']
title_list = []


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
                # 이미지, 제목 추출
                imgUrl = driver.find_element(By.XPATH, '/html/body/div/div[4]/div[1]/div/span/em/img').get_attribute('src')
                title = driver.find_element(By.XPATH, '/html/body/div/div[4]/div[1]/div/span/em/img').get_attribute('alt')
                # 이미지 저장 및 리스트에 제목 추가
                for j in range(100):
                    urllib.request.urlretrieve(imgUrl, f'save/images/{i}-{j}.jpg')
                    title2 = f'{i}-{j}.jpg' 
                    title_list.append(title)
                # 뒤로 가기
                driver.back()
        except:
            continue
        
       
# 텍스트 저장
pd.DataFrame(title_list).to_csv('save/titles.csv', index=True)