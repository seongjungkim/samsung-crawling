import csv
import json
import math
import random
import time
from urllib.parse import urlparse

from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import samsung_crawler as samsung_crawler


class SamsungChromeCrawler(samsung_crawler.SamsungCrawler):

    def __get_status(self, logs):
        for log in logs:
            if log['message']:
                data = json.loads(log['message'])
                try:
                    content_type = 'text/html' in data['message']['params']['response']['headers']['content-type']
                    response_received = data['message']['method'] == 'Network.responseReceived'
                    if content_type and response_received:
                        return data['message']['params']['response']['status']
                except:
                    pass
        return 0

    def __get_response_status(self):
        # https://www.tutorialspoint.com/how-to-get-http-response-code-using-selenium-webdriver
        # https://stackoverflow.com/questions/5799228/how-to-get-status-code-by-using-selenium-py-python-code
        # establish and open connection with URL
        logs = self.driver.get_log('performance')
        # print('logs', logs)
        status = self.__get_status(logs)
        # print('status', status)
        return status

if __name__ == "__main__":
    opts = Options()
    opts.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)

    model_name, model_number = "galaxy-s24-ultra-s928", "SM-S928NZTNKOO"
    base_url = "https://samsung.com/sec/smartphones"
    url = "{}/{}/{}/".format(base_url, model_name, model_number)

    crawler = SamsungChromeCrawler(driver, csv_file, csv_writer)
    crawler.innerhtml(url, model_name, model_number)

    time.sleep(10)
    crawler.close()
