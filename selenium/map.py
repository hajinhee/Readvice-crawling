from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup 
import re
import time
import pandas as pd
import json 


class Crawling():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)
        self.review_json = {}  # 리뷰 

    # 플레이스 URL 크롤링
    def save_url(self):
        df = pd.read_csv('data/places.csv', encoding = 'cp949')  # 원하는 플레이스 정보가 담긴 파일
        df['naver_map_url'] = '' # 미리 url을 담을 column을 만들어줌 

        for i, keyword in enumerate(df['검색어'].tolist()): 
            
            print("이번에 찾을 키워드 :", i, f"/ {df.shape[0]} 행", keyword) 
            
            try: 
                naver_map_search_url = f'https://map.naver.com/v5/search/{keyword}/place' # 검색 url 만들기 
                self.driver.get(naver_map_search_url) # 검색 url 접속 = 검색하기 
                time.sleep(4) # 중요

                cu = self.driver.current_url # 검색이 성공된 플레이스에 대한 개별 페이지 
                res_code = re.findall(r"place/(\d+)", cu)
                final_url = 'https://pcmap.place.naver.com/restaurant/'+res_code[0]+'/review/visitor#' 
                
                print(final_url)
                df['naver_map_url'][i]=final_url 
                
            except IndexError: 
                df['naver_map_url'][i]= ''
                print('none') 
            
            df.to_csv('data/url_completed.csv', encoding = 'utf-8-sig')


    # 각 플레이스 리뷰 크롤링
    def get_rivews(self):
        df = pd.read_csv('data/url_completed.csv')  # 전처리 완료한 데이터 불러오기
        for i in range(len(df)): 
            print('======================================================') 
            print(str(i)+'번째 식당') 
            
            # 식당 리뷰 개별 url 접속
         
            self.driver.get(df['naver_map_url'][i]) 
            thisurl = df['naver_map_url'][i]
            time.sleep(2) 
            
            # 더보기 버튼 다 누를 것
            while True: 
                try: 
                    time.sleep(1) 
                    self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END) 
                    time.sleep(3) 
                    
                    self.driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div:nth-child(7) > div:nth-child(2) > div.place_section.lcndr > div.lfH3O > a').click() 
                    time.sleep(3) 
                    self.driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END) 
                    time.sleep(1) 
                    
                except: 
                    print('-더보기 버튼 모두 클릭 완료-') 
                    break 
            
            # 파싱
            html = self.driver.page_source 
            soup = BeautifulSoup(html, 'lxml') 
            time.sleep(1) 
            
            # 식당 구분 
            restaurant_name = df['검색어'][i]
            print('식당 이름 : '+restaurant_name) 
            
            self.review_json = {restaurant_name: []}

            # 특정 식당에 대한 리뷰 수집
            try: 
                one_review = soup.find_all('div', attrs = {'class':'ZZ4OK IwhtZ'})
                review_num = len(one_review) # 특정 식당의 리뷰 총 개수 
                print('리뷰 총 개수 : '+str(review_num)) 
                
                # 모든 리뷰에 대해서 정보 수집
                for i in range(len(one_review)): 
                    # review 내용
                    try: 
                        review_content = one_review[i].find('span', attrs = {'class':'zPfVt'}).text
                    except: # 리뷰가 없다면
                        review_content = "" 
                    print('리뷰 내용 : '+ review_content) 
                    dict_temp = {
                        f'{i}번째 review': review_content
                    }

                    self.review_json[restaurant_name].append(dict_temp)


            # 리뷰가 없는 경우        
            except: 
                none_review = "네이버 리뷰 없음" 
                print(none_review)
                review_num = 0           
        print('\n')                

        # 저장
        file_path = "data/review.json" 
        with open(file_path,'w', encoding='utf-8') as f: 
            json.dump(self.review_json, f, ensure_ascii=False) 


if __name__=='__main__':
    # Crawling().save_url()
    Crawling().get_rivews()
