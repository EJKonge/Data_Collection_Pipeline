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
#Creating a class containing a webscraper to gather Anime data from IMDB.com
    
    def __init__(self,  url : str = "https://www.imdb.com/search/keyword/?keywords=anime&ref_=kw_nxt&mode=detail&page=1&sort=moviemeter,asc"):
        """
        __init__ to initialise all the attributes needed.

        Parameters:
            engine: creates a connection to the RDS server.
            driver: sets up the driver to control chrome for selenium.
            title,year,link,genre,rating,id,uuid: creates empty lists to be used later.
            page: sets starting page number(needed for loading new pages in next_page function below)
        """

        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        self.engine.connect()

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

    def scrolling(self):
        """
        This function scrolls through the webpage until it reaches the bottom of the page, this is done in order to load all image on the page
        
        Parameters:
            i: i is used as an iterator to scroll 16 times, that is the number needed to reach the bottom of the page.
        """

        print('Scrolling to load images')
        for i in range(16):
            locate = self.driver.find_element(By.XPATH, '//*[@id="styleguide-v2"]')
            locate.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

    def next_page(self):
        """
        This function uses selenium to go to the next page on the browser so get_titles can continue to collect more data.

        Parameters:
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

    def local_img_save(self):
        """
        This function downloads the images from self.img_link and saves them locally
        
        Parameters:
            opener: accesses urllib in order to prepare for downloading.
            img_num: counter to keep self.title at the same iteration as self.img_links.
            links: iterates through self.img_links.

        Returns:
            Saves all images in the list to raw_data/images as .jpg files.
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
    

    def get_data(self, pages):
        """
        This function gathers all wanted data by using try/except clauses for each arg.

        Args:
            df: gets a data frame from RDS server.
            amount: sets up the webdriver and locates the requried xpath.
            titles: iterator for going through the amount list.
            id: checks if uuid exists for current data in the dataframe.


        Returns:
            Appends all data gatherd to the lists created in the __init__ method.

        """    
        print(f'Gathering data on page: {self.page}')

        
        df = pd.read_sql_table('animescraper', self.engine)
        df=df["title", "link", "genre", "rating", "id", "uuid", "img_link"]

        amount = self.driver.find_elements(By.XPATH, '//div[@class="lister-list"]/div')

        for titles in range(len(amount)):

            self.uuid.append(str(uuid.uuid4()))
            if id in list(df['uuid']):
                continue

            item = self.driver.find_elements(By.XPATH, '//div[@class="lister-list"]/div')[titles]
            info = (item.text).split('\n')
            temp_title = info[0].split('(')[0].strip() 
            temp_year = info[0].split('(')[1].replace(')', '') 
            temp_genre = info[1].split('|')[-1].strip() 

            temp_check = info[1].split('|')
            if len(temp_check) == 3:
                temp_rating = temp_check[0]
            else:
                temp_rating = np.NAN

            try:    
                temp_link = item.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{titles+1}]/div[2]/h3/a').get_attribute('href')
                temp_id = temp_link[29:36]
            except:
                temp_link = np.NAN
                temp_id = np.NAN

            try:
                temp_img= item.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{titles+1}]/div[1]/div[2]/a/img').get_attribute('src')
            except:
                try:
                    temp_img= item.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{titles+1}]/div[1]/a/img').get_attribute('src')
                except:
                    temp_img=np.NAN

            self.title.append(temp_title)
            self.year.append(temp_year)
            self.link.append(temp_link)
            self.genre.append(temp_genre)
            self.rating.append(temp_rating)
            self.id.append(temp_id)
            self.img_link.append(temp_img)

        if pages != self.page:
            self.next_page()
        else:
            self.driver.quit()
            self.create_df(df)

    #continue here
    def create_df(self, df):
        """
        This function creates a dataframe, using pandas, and stores the data gathered in the get_data function as a .json and .csv file.

        Args:
            anime_df:creates the dataframe
            anime_df.index: changes the index to start from 1 instead of 0

        Returns:
            all gathered data is stored in a file on your local machine
        """

        print('Creating the dataframe to store all data')
        temp_anime_df = pd.DataFrame({'Title':self.title, 'Year':self.year, 'Link':self.link, 'Genres':self.genre, 'Rating':self.rating, 'ID':self.id, 'UUID':self.uuid, 'Image Links':self.img_link, })
        temp_anime_df.index +=1
        anime_df = pd.concat([df,temp_anime_df],ignore_index=True)
        anime_df.to_json(r'raw_data/data.json')

        self.data_to_aws(anime_df)

    
    def data_to_aws(self, anime_df):
        print('Uploading dataframe to AWS')
        s3= boto3.client('s3')
        s3.upload_file('raw_data/data.json', 'anime-cloud', 'Raw-Data')
        anime_df.to_sql('animescraper',self.engine, if_exists="replace")

    def img_to_aws():
        print('Uploading images to AWS')
        path ='raw_data/images'
        os.chdir(path)
        for names in os.listdir():
            s3= boto3.client('s3')
            s3.upload_file(names, 'anime-cloud', 'Images/' + str(names) )


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
        pages = input('How many pages do you wanna scrape: ')
        for i in range(int(pages)):
            self.scrolling()
            self.get_data(pages)    
        self.save_location()
        
                
if __name__ == '__main__':
    Anime = Anime_Scraper()
    Anime.run_scraper()