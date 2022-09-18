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

        self.test_scraper = Anime_Scraper.Anime_Scraper()


    def test_url(self):
        
        url = "https://www.imdb.com/search/keyword/?keywords=anime&ref_=kw_nxt&mode=detail&page=1&sort=moviemeter,asc"
        self.driver.get(url)
        time.sleep(2)
        assert "Find an anime inpspection report" in self.driver.title
    
    def test_xpaths(self):

        self.test_scraper.driver.find_element(By.XPATH, '//div[@class="lister-list"]/div').click()
        time.sleep(2)
        self.test_scraper.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/h3/a').click()
        time.sleep(2)
        self.test_scraper.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[1]/div[2]/a/img').click()
        time.sleep(2)
        self.test_scraper.driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/div[2]/a[2]').click()
        time.sleep(2)

    def tearDown(self):
        self.driver.close()

    if __name__ == '__main__':
        unittest.main()