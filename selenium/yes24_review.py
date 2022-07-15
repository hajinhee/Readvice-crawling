from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request
import pandas as pd
import time
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, TimeoutException, ElementNotInteractableException,NoSuchWindowException, NoSuchFrameException


import urllib3


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
url = "http://www.yes24.com/24/Category/BestSeller"
driver.get(url)
driver.maximize_window()

'''
경제/경영 3, 만화/라이트노벨 6, 소설/시/희곡 8, 어린이 10, 에세이 11, 여행 12, 
유아 15, 자기계발 18, IT모바일 24
'''

# # 장르 클릭
# for category in categoreis:
#     WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div/div[2]/div[1]/div[1]/ul/li[1]/ul/li[{category}]/a'))).click()      
#     time.sleep(2)
#     # 페이지 클릭
#     for i in range(1, 3):
#         try:
#             WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="bestList"]/div[3]/div[1]/div[1]/p/a[{i}]'))).click()
#             # 도서 클릭
#             for i in range(1, 40, 2):               
#                 WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="category_layout"]/tbody/tr[{i}]/td[3]/p[1]/a[1]'))).click()
#                 # 리뷰 페이지 클릭
#                 for i in range(1, 3):
#                     review_page = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="infoset_oneCommentList"]/div[2]/div[1]/div/a[{i}]')))
#                     isExistReview = review_page.is_enabled()
#                     if isExistReview == True:
#                         review_page.click()
#                         # 리뷰 크롤링
#                         for i in range(1, 7):
#                             try:
#                                 title = driver.find_element(By.XPATH, '/html/body/div/div[4]/div[1]/div/span/em/img').get_attribute('alt')
#                                 review = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'#infoset_oneCommentList > div.infoSetCont_wrap.rvCmtRow_cont.clearfix > div:nth-child({i}) > div.cmtInfoBox > div.cmt_cont > span'))).text
#                                 time.sleep(2)
#                                 title_list.append(title)
#                                 review_list.append(review)                           
#                             except:
#                                 break   
#                     else: 
#                         break
#                 # 뒤로 가기
#                 driver.back()
#         except:
#             continue
    # d1 = dict(zip(title_list, review_list))
    # df = pd.DataFrame.from_dict(d1, orient='index')
    # df.to_csv('save/reviews/review.csv', sep=',')




categoreis = ['001001025', '001001008', '001001046', '001001016', '001001047', '001001009', '001001027', '001001026', '001001003']
review_list = []
list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
list7 = []
list8 = []

for category in categoreis:
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="category{category}"]/a'))).click()      
        # 페이지 클릭
        for page in range(1, 10):
            try:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="bestList"]/div[3]/div[1]/div[1]/p/a[{page}]'))).click()                                   
                time.sleep(2)
                # 도서 클릭
                for i in range(1, 40, 2):               
                    try: 
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="category_layout"]/tbody/tr[{i}]/td[3]/p[1]/a[1]'))).click()
                        title = driver.find_element(By.XPATH, '/html/body/div/div[4]/div[1]/div/span/em/img').get_attribute('alt')
                        for page in range(1, 4):  
                            try:
                                driver.find_element(By.XPATH,f'//*[@id="infoset_oneCommentList"]/div[2]/div[1]/div/a[{page}]').click()                                 
                                time.sleep(2)
                                for i in range(1, 7):
                                    try:  
                                        review = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'#infoset_oneCommentList > div.infoSetCont_wrap.rvCmtRow_cont.clearfix > div:nth-child({i}) > div.cmtInfoBox > div.cmt_cont > span'))).text 
                                        review_list.append(review)     
                                    except:
                                        break
                                        driver.back() 
                            except: 
                                break
                                driver.back()  
                        
                        driver.back()
                    except:
                        continue
            except:
                continue    
    except:
        continue                
review_list2 = list(set(review_list))
df = pd.Series(review_list2)
df.to_csv(f'save/reviews/review.csv', sep=',')
    # dt = {i:j for i, j in zip(title_list, review_list)}
    # print(dt)
    # # d1 = dict(zip(title_list, review_list))
    # df = pd.DataFrame.from_dict(dt, orient='index')
    # df.to_csv(f'save/reviews/{category}.csv', sep=',')
