import Anime_Scraper
import time
import unittest
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Scraper_test(unittest.TestCase):

    def setUp(self):

        options = Options()

        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.imdb.com/search/keyword/?keywords=anime&ref_=kw_nxt&mode=detail&page=1&sort=moviemeter,asc")

        self.test_scraper = Anime_Scraper.Anime_Scraper()


    def test_scrolling(self):
        self.test_scraper.scrolling()
        time.sleep(2)

    def test_page_swap(self):
        self.test_scraper.next_page()
    
    def tearDown(self):
        self.driver.close()

    if __name__ == '__main__':
        unittest.main(verbosity=2)