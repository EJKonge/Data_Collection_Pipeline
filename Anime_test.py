import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import Anime_Scraper
import requests
import time
import os


class Anime_test(unittest.TestCase):

    def setUp(self):
        self.test_scraper = Anime_Scraper.Anime_Scraper()

    def test_scrolling(self):
        self.test_scraper.scrolling()

    def test_page_swap(self):
        self.test_scraper.next_page()

    def test_xpaths_click(self):
        self.driver = webdriver.Chrome()
        for i in ['//div[@class="desc"]/a[1]', 
            '//*[@id="styleguide-v2"]',     
            '//div[@class="lister-list"]/div', 
            '//div[@class="removable-wrapper"]/a', 
            '//div[@class="removable-wrapper"]/a/img']:
            self.driver.find_element(By.XPATH, i).click()
            time.sleep(2)
            new_url=self.driver.current_url
            
            with requests.Session() as s:
                   response = s.get(new_url)
            assert response.status_code == 200

    def tearDown(self):
        self.test_scraper.driver.quit()


if __name__ == '__main__':
    unittest.main()