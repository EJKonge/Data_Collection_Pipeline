import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import Anime_Scraper
import time
import os


class GoogleTestCase(unittest.TestCase):

    def setUp(self):
        self.test_scraper = Anime_Scraper.Anime_Scraper()

    def test_scrolling(self):
        self.test_scraper.scrolling()


    def tearDown(self):
        self.test_scraper.driver.quit()


if __name__ == '__main__':
    unittest.main()