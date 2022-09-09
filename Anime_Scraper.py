from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import boto3
import numpy as np
import os
import pandas as pd
import requests 
import selenium
import time
import urllib.request
import uuid


class Anime_Scraper:
    """
    Creating a class containing a webscraper to gather Anime data from IMDB.com
    """
    def __init__(self,  url : str = "https://www.imdb.com/search/keyword/?keywords=anime&ref_=kw_nxt&mode=detail&page=1&sort=moviemeter,asc"):

        """
        __init__ to initialise all the attributes needed.

        Args:
            driver: sets up the driver to control chrome for selenium.
            title,year,link,genre,rating,id,uuid: creates empty lists to be used later.
            page: sets starting page number(needed for loading new pages in next_page function below)
        """
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)
        self.title= []
        self.year= []
        self.link= []
        self.genre= []
        self.rating= []
        self.id= []
        self.uuid= []
        self.img_name= []
        self.img_link= []
        self.page = 1

    def get_data(self, i=1):

        """
        This function gathers all wanted data by using try/except clauses for each arg.

        Args:
            uuid: global unique ID 
            title: title of the anime
            year: release date of the anime
            link: link to animes page
            genre: genre of the anime
            rating: rating of the anime
            id: ID derived from the link of the anime page

        Returns:
            Try clause appends the wanted data, if available, to the empty lists in the __init__ method. Otherwise the except clause appends a value of NAN from numpy.

        """    
        print(f'Gathering data on page: {self.page}')
        while i < 51:
            self.uuid.append(str(uuid.uuid4()))

            try:
                block = self.driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]')
            except:
                pass

            try:
                title_temp = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/h3/a').text
            except:
                title_temp = np.NAN

            try:
                year_temp = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/h3/span[2]').text
            except:
                year_temp = np.NAN

            try:    
                link_temp = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/h3/a').get_attribute('href')
            except:
                link_temp = np.NAN

            try:
                genre_temp = block.find_element(By.CLASS_NAME, 'genre').text
            except:
                genre_temp = np.NAN

            try:
                rating_temp = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/div/div[1]/strong').text
            except:
                rating_temp = np.NAN
            
            try:
                id_temp = link_temp[29:36]
            except:
                id_temp = np.NAN

            try:
                temp_name= self.driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[1]/div[2]/a/img').get_attribute('alt').replace(':', "").replace('?','').replace('/',' ')
            except:
                try:
                    temp_name= self.driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[1]/a/img').get_attribute('alt').replace(':', "").replace('?','').replace('/',' ')
                except:
                    temp_name=np.NAN
            
            try:
                temp_link= self.driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[1]/div[2]/a/img').get_attribute('src')
            except:
                try:
                    temp_link= self.driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[1]/a/img').get_attribute('src')
                except:
                    temp_link=np.NAN

            self.title.append(title_temp)
            self.year.append(year_temp)
            self.link.append(link_temp)
            self.genre.append(genre_temp)
            self.rating.append(rating_temp)
            self.id.append(id_temp)
            self.img_name.append(temp_name)
            self.img_link.append(temp_link)
            i+=1            

    def scrolling(self):
        print('Scrolling to load images')
        for i in range(16):
            locate = self.driver.find_element(By.XPATH, '//*[@id="styleguide-v2"]')
            locate.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

    def local_img_save(self):
        print('Saving images to pc')
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        x=0
        for links in self.img_link:
            if pd.isnull(links) == False:
                filename = f"raw_data\images\{self.img_name[x]}.jpg"
                image_url = links
                urllib.request.urlretrieve(image_url, filename)
            else:
                print(f'No image found for {self.img_name[x]}')
            x+=1 
    
    def create_df(self):

        """
        This function creates a dataframe, using pandas, and stores the data gathered in the get_titles function as a .json and .csv file.

        Args:
            anime_df:creates the dataframe
            anime_df.index: changes the index to start from 1 instead of 0

        Returns:
            all gathered data is stored in a file on your local machine
        """
        print('Creating the dataframe to store all data')
        anime_df = pd.DataFrame({'Title':self.title, 'Year':self.year, 'Link':self.link, 'Genres':self.genre, 'Rating':self.rating, 'ID':self.id, 'UUID':self.uuid, 'Image Links':self.img_link, 'Image Names':self.img_name})
        anime_df.index +=1
        #print(anime_df)
        anime_df.to_json(r'raw_data\data.json')
        #anime_df.to_csv('raw_data\data.csv')

    def data_to_aws(self):
        print('Uploading dataframe to AWS')
        try:
            s3= boto3.client('s3')
            s3.upload_file('raw_data/data.json', 'anime-cloud', 'Raw-Data')
        except:
            ACCESS_KEY = input('Please type your AWS access key: ')
            SECRET_KEY = input('Please type your AWS secret key: ')
            s3= boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
            s3.upload_file('raw_data/data.json', 'anime-cloud', 'Raw-Data')

    def img_to_aws(self):
        print('Uploading images to AWS')
        path ='raw_data\images'
        for names in os.listdir(path):
            s3= boto3.client('s3')
            s3.upload_file(names, 'anime-cloud', 'Images/' + str(names) )

    def next_page(self):
        
        """
        This function uses selenium to go to the next page on the browser so get_titles can continue to collect more data.

        Args:
            nextpage: uses selenium to locate the 'next' button via XPATH.
            nextpage.click: clicks the previously located button with selenium.

        Returns:
            Next page is displayed on the browser
        """
        print(f'Going to page: {int(self.page)+1}')
        if self.page == 1:
            self.nextpage = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/a')
            self.nextpage.click()
            self.page +=1

        else:
            self.nextpage = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/a[2]')
            self.nextpage.click()
            self.page +=1
        time.sleep(5)

    def save_location(self):
        location = input('Save Images locally (pc) or local+cloud (both)? Please type “pc” or “both” to make your choice: ').lower()
        if location == 'pc':
            print('You chose PC')
            self.local_img_save()
        else:
            print('You chose both')
            self.local_img_save()
            self.img_to_aws()

    def run_scraper(self):
        amount = input('How many pages do you wanna scrape: ')
        for i in range(int(amount)):
            self.scrolling()
            self.get_data()    
            self.next_page()
    
    def quit_scraper(self):
        self.driver.quit()
                
if __name__ == '__main__':
    Anime = Anime_Scraper()
    Anime.run_scraper()
    Anime.quit_scraper()
    Anime.create_df()
    Anime.data_to_aws()
    Anime.save_location()