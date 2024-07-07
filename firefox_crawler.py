import csv
import json
import math
import random
import time
from urllib.parse import urlparse

from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.firefox import GeckoDriverManager

import samsung_crawler as samsung_crawler

class SamsungFirefoxCrawler(samsung_crawler.SamsungCrawler):

    def __get_response_status(self):
        status = 0
        # Access requests via the 'requests' attribute
        for request in dirver.requests:
            if request.response:
                print(
                    request.url,
                    request.response.status_code,
                    request.response.headers['Content-Type']
                )
                status = request.response.status_code

        return status

if __name__ == "__main__":
    # https://stackoverflow.com/questions/64371749/how-can-i-get-selenium-geckodriver-to-work
    #driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    model_name, model_number = "galaxy-s24-ultra-s928", "SM-S928NZTNKOO"
    base_url = "https://samsung.com/sec/smartphones"
    url = "{}/{}/{}/".format(base_url, model_name, model_number)

    crawler = SamsungFirefoxCrawler(driver, csv_file, csv_writer)
    crawler.innerhtml(url, model_name, model_number)

    time.sleep(10)
    crawler.close()
