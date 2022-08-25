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
        i=50
        page = 1
        block = self.driver.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]')
        title = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/h3/a').text
        year = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/h3/span[2]').text
        link = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/h3/a').get_attribute('href')
        genre = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/p[1]/span[5]').text
        rating = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/div/div[1]/strong').text
        certificate = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/p[1]/span[1]').text
        runtime = block.find_element(By.XPATH, f'//*[@id="main"]/div/div[2]/div[3]/div[{i}]/div[2]/p[1]/span[3]').text
        print(title)
        print(year)
        print(link + "\n" + genre + "\n" + rating + "\n" + certificate + "\n" + runtime)
        time.sleep(2)
        if page == 1:
            self.first_page()
            page +=1
        else: 
            self.next_page
            page +=1

    def run_scraper(self):
            self.get_titles()
    
    def first_page(self):
        self.nextpage = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/a')
        self.nextpage.click()

    def next_page(self):
        self.nextpage = self.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/a[2]')
        self.nextpage.click()

              
    def quit_scraper(self):
        self.driver.quit()
                
if __name__ == '__main__':
    Anime = Anime_Scraper()
    time.sleep(5)
    Anime.first_page()
    time.sleep(5)
    Anime.next_page()
    time.sleep(5)
    Anime.next_page()
    time.sleep(5)
    Anime.quit_scraper()
    
