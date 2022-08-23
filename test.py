import selenium
from selenium import webdriver 
import requests 
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
import time

class Anime_Scraper:

    def __init__(self, url : str = "https://www.imdb.com/search/keyword/?keywords=anime&ref_=kw_nxt&mode=detail&page=1&sort=moviemeter,asc"):

        self.driver = webdriver.Chrome()
        self.driver.get(url)

    def get_titles(self):
        time.sleep(2)
        block = self.driver.find_element(By.CLASS_NAME, 'lister-item')
        ftitle = block.find_element(By.CLASS_NAME, 'lister-item-header').text
        forder = block.find_element(By.CLASS_NAME, 'lister-item-index').text
        fyear = ftitle[-6:]
        ftitle = ftitle.replace(forder+' ', '')[:-7 ]
        flink = block.find_element(By.LINK_TEXT, ftitle).get_attribute('href')
        print(ftitle)
        print(fyear)
        print(flink)

    def run_scraper(self):
            self.get_titles()

            

    def quit_scraper(self):
        self.driver.quit()
                
if __name__ == '__main__':
    Anime = Anime_Scraper()
    Anime.run_scraper()
    Anime.quit_scraper()
