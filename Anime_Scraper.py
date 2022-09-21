import boto3
import numpy as np
import os
import pandas as pd
import psycopg2
import time
import urllib.request
import uuid
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine



class Anime_Scraper:
    '''
    Creating a class containing a webscraper to gather Anime data from IMDB.com.
    Information about most popular anime is collected and stored in a pandas dataframe, which is then uploaded to AWS.
    Data collected for each anime;
        title, year ,link, genre, rating, id, uuid, image link.

    '''
    
    def __init__(self,  url : str = "https://www.imdb.com/search/keyword/?keywords=anime&ref_=kw_nxt&mode=detail&page=1&sort=moviemeter,asc"):
        """
        __init__ to initialise all the attributes needed.

        Parameters:
            url: URL for the website that will be used in the class.
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
        self.img_link= []

        self.page = 1

    def __RDS_engine(self):
        """
        Creates a connection to the RDS server an AWS.
        """
        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        self.engine.connect()

    def scrolling(self):
        """
        This function scrolls through the webpage until it reaches the bottom of the page, this is done in order to load all image on the page.
        """

        print('Scrolling to load images')
        for scrolling_iterator in range(16):
            locate = self.driver.find_element(By.XPATH, '//*[@id="styleguide-v2"]')
            locate.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

    def next_page(self):
        """
        This function uses selenium to go to the next page on the browser so get_data can continue to collect more data. 
        Try/except statement is used because the xpath is different on page 1 compared to every other page.
        """

        print(f'Going to page: {int(self.page)+1}')

        try:
            self.nextpage = self.driver.find_element(By.XPATH, '//div[@class="desc"]/a[2]')
        except:
            self.nextpage = self.driver.find_element(By.XPATH, '//div[@class="desc"]/a[1]')

        self.nextpage.click()
        self.page +=1

        time.sleep(5)

    def __local_img_save(self):
        """
        This function iterates through self.img_links links and uses urllib library to downloads and save the images locally.
        opener is made to create an OpenDirectory instance needed to access the websites in the urls.

        Returns:
            Saves all images in the folder raw_data/images as .jpg files.
        """

        print('Saving images to pc')

        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        img_num=0

        for links in self.img_link:

            if pd.isnull(links) == False:
                filename = f"raw_data/images/{self.title[img_num]}.jpg"
                image_url = links
                urllib.request.urlretrieve(image_url, filename)

            else:
                print(f'No image found for {self.title[img_num]}')
                
            img_num+=1 

    def __save_location(self):
        """
        This function decides wether to save images locally or locally and in the cloud.
        """

        location = input('Save Images locally (pc) or local+cloud (both)? Please type “pc” or “both” to make your choice: ').lower()
        
        if location == 'pc':
            print('You chose PC')
            self.__local_img_save()

        else:
            print('You chose both')
            self.__local_img_save()
            self.img_to_aws()

    def __get_data(self, pages):
        """
        This function checks if the data to be scraped already exists in the RDS server. If not, it proceeds to scrape the required information.

        Parameters:
            pages: Integer value gotten from user to determine the number of pages needed to be scraped.
        """    
        print(f'Gathering data on page: {self.page}')

        #reads dataframe stored in RDS
        df = pd.read_sql_table('animescraper', self.engine)
        df=df["title", "year" ,"link", "genre", "rating", "id", "uuid", "img_link"]

        Xpath_list = self.driver.find_elements(By.XPATH, '//div[@class="lister-list"]/div')

        for titles in range(len(Xpath_list)):

            item = self.driver.find_elements(By.XPATH, '//div[@class="lister-list"]/div')[titles+1]
            info = (item.text).split('\n')

            try:    
                temp_link = item.find_element(By.XPATH, f'//div[@class="removable-wrapper"]/a').get_attribute('href')
                temp_id = temp_link[29:36]
            except:
                temp_link = np.NAN
                temp_id = np.NAN

            #checks if data already exists in the RDS server
            if temp_id not in list(df['id']) and temp_id != np.NAN:

                temp_title = info[0].split('(')[0].strip() 
                temp_year = info[0].split('(')[1].replace(')', '') 
                temp_genre = info[1].split('|')[-1].strip() 

                #checks if ranking is listed on the page or not
                temp_check = info[1].split('|')
                if len(temp_check) == 3:
                    temp_rating = temp_check[0]
                else:
                    temp_rating = np.NAN

                try:
                    temp_img= item.find_element(By.XPATH, f'//div[@class="removable-wrapper"]/a/img').get_attribute('src')
                except:
                    temp_img=np.NAN

                self.title.append(temp_title)
                self.year.append(temp_year)
                self.link.append(temp_link)
                self.genre.append(temp_genre)
                self.rating.append(temp_rating)
                self.id.append(temp_id)
                self.uuid.append(str(uuid.uuid4()))
                self.img_link.append(temp_img)

            else:
                continue

        #checks if desired number of pages has been scraped. If yes, loop breaks and create_df function is called.
        if pages != self.page:
            self.next_page()
        else:
            self.driver.quit()
            self.__create_df(df)

    
    def __create_df(self, df):
        """
        This function creates a dataframe by concatenating data from dataframe taken from RDS and the newly gathered data. 

        Parameters:
            df: data frame from the RDS server is given as a parameter from the get_data function.
        """

        print('Creating the dataframe to store all data')

        temp_anime_df = pd.DataFrame({'Title':self.title, 'Year':self.year, 'Link':self.link, 'Genres':self.genre, 'Rating':self.rating, 'ID':self.id, 'UUID':self.uuid, 'Image Links':self.img_link, })
        temp_anime_df.index +=1

        anime_df = pd.concat([df,temp_anime_df],ignore_index=True)

        anime_df.to_json(r'raw_data/data.json')

        self.__data_to_aws(anime_df)

    
    def __data_to_aws(self, anime_df):
        """
        This function uploads the data frame from create_df() to AWS.
        
        Parameters: 
            anime_df: data frame created in the create_df() function.
        """

        print('Uploading dataframe to AWS')

        s3= boto3.client('s3')
        s3.upload_file('raw_data/data.json', 'anime-cloud', 'Raw-Data')
        anime_df.to_sql('animescraper',self.engine, if_exists="replace")

    @staticmethod
    def img_to_aws():
        """
        This function uploads the images to s3 bucket.
        """

        print('Uploading images to AWS')

        path ='raw_data/images'
        os.chdir(path)

        for names in os.listdir():
            s3= boto3.client('s3')
            s3.upload_file(names, 'anime-cloud', 'Images/' + str(names) )

    def run_scraper(self):
        """
        This is the logic of the scraper which runs the scraper as required.
        """

        self.__RDS_engine()

        pages = input('How many pages do you wanna scrape: ')

        for amount in range(int(pages)):
            self.scrolling()
            self.__get_data(pages)    

        self.__save_location()
        
                
if __name__ == '__main__':
    Anime = Anime_Scraper()
    Anime.run_scraper()