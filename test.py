import imp
import selenium
from selenium import webdriver 
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
import time
import uuid
import urllib.request
import os

class Anime_Scraper:

    def __init__(self,  url : str = "https://www.imdb.com/search/keyword/?keywords=anime&ref_=kw_nxt&mode=detail&page=1&sort=moviemeter,asc"):

        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.title= []
        self.year= []
        self.link= []
        self.genre= []
        self.rating= []
        self.id= []
        self.uuid= []
        self.page = 1

    def get_titles(self):
        for i in range(1,5):
            self.uuid.append(str(uuid.uuid4()))
            block = self.driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]')
            try:
                
                try:
                    title_temp = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/h3/a').text
                    self.title.append(title_temp)
                except:
                    title_temp = np.NAN
                    self.title.append(title_temp)

                try:
                    year_temp = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/h3/span[2]').text
                    self.year.append(year_temp)
                except:
                    year_temp = np.NAN
                    self.year.append(year_temp)

                try:    
                    link_temp = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/h3/a').get_attribute('href')
                    self.link.append(link_temp)
                except:
                    link_temp = np.NAN
                    self.link.append(link_temp)

                try:
                    genre_temp = block.find_element(By.CLASS_NAME, 'genre').text
                    self.genre.append(genre_temp)
                except:
                    genre_temp = np.NAN
                    self.genre.append(genre_temp)

                try:
                    rating_temp = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/div/div[1]/strong').text
                    self.rating.append(rating_temp)
                except:
                    rating_temp = np.NAN
                    self.rating.append(rating_temp)
                
                try:
                    id_temp = link_temp[29:36]
                    self.id.append(id_temp)
                except:
                    id_temp = np.NAN
                    self.id.append(id_temp)
                    
            except:
                continue

    def get_img(self):
        img_name= []
        img_link= []
        local_name=[]
        num=1
        for ids in self.id:
            try:
                temp_name= self.driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{num}]/div[1]/a/img').get_attribute('alt')
            except:
                temp_name= np.NAN
            
            try:
                temp_link= self.driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{num}]/div[1]/a/img').get_attribute('src')
            except:
                temp_link= np.NAN

            img_name.append(temp_name)
            img_link.append(temp_link)
            local_name.append(str(num) +'_' +ids)
            num+=1
        ''' Saving images locally
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        x=0
        for links in img_link:
            filename = f"raw_data\images\{local_name[x]}.jpg"
            image_url = links
            urllib.request.urlretrieve(image_url, filename)
            x+=1 '''

    
    def create_df(self):
        anime_df = pd.DataFrame({'Title':self.title, 'Year':self.year, 'Link':self.link, 'Genres':self.genre, 'Rating':self.rating, 'ID':self.id, 'UUID':self.uuid})
        anime_df.index +=1
        print(anime_df)
        #anime_df.to_json(r'raw_data\data.json')
        #anime_df.to_csv('raw_data\data.csv')

    def run_scraper(self):
            self.get_titles()

    def next_page(self):
        
        if self.page == 1:
            self.nextpage = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/a')
            self.nextpage.click()
            self.page +=1

        else:
            self.nextpage = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/a[2]')
            self.nextpage.click()
            self.page +=1
              
    def quit_scraper(self):
        self.driver.quit()
                
if __name__ == '__main__':
    Anime = Anime_Scraper()
    Anime.run_scraper()
    time.sleep(5)
    Anime.get_img()
    Anime.quit_scraper()
