# -*- coding: utf-8 -*-
import argparse
import configparser
import csv
import json
import os
import pandas as pd
import time

#from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import chrome_crawler
import firefox_crawler

"""
python main.py --process html
python main.py --process pdf
python main.py --process download
"""

def __parse_args():
    parser = argparse.ArgumentParser(
        description='Command line to clean up all Teradata metadata on Datacatalog')

    parser.add_argument('--config', help='Application Properties File',
                        default='application.properties')
    parser.add_argument('--module', help='Crawling using systems ex) chrome, firefox, jsoup',
                        default='chrome')
    parser.add_argument('--process', help='Process ex) retrieve, retry, check, test',
                        default='retrieve')

    return parser.parse_args()

if __name__ == "__main__":
    """
    python main.py --process html
    python main.py --process pdf
    """

    args = __parse_args()
    print('--config', args.config, '--csv-file', args.csv_file)
    print('--start', args.start, '--end', args.end)
    print('--module', args.module, '--process', args.process)

    start = int(args.start) if args.start else 0
    end = int(args.end) if args.end else 0
    csv_file_path = args.csv_file if args.csv_file else None
    module = args.module if args.module else 'chrome'
    process = args.process if args.process else 'retrieve'

    #with open(args.config, 'r') as config_file:
    #    config_string = config_file.read()
    #config = configparser.ConfigParser()
    #config.read_string(config_string)

    process = args.process if args.process else 'retrieve'

    if module == 'chrome':
        if process == 'pdf':
            opts = webdriver.ChromeOptions()
            settings = {
                "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}], 
                "selectedDestinationId": "Save as PDF", 
                "version": 2,
                "isHeaderFooterEnabled": False,
                "mediaSize": {
                    "height_microns": 297000,
                    "name": "ISO_A4",
                    "width_microns": 210000,
                    "custom_display_name": "A4"
                },
                "customMargins": {},
                "marginsType": 2,
                "scaling": 100,
                "scalingType": 3,
                "scalingTypePdf": 3,
                "isCssBackgroundEnabled": True
            }
            prefs = {
                'printing.print_preview_sticky_settings.appState': json.dumps(settings),
                'savefile.default_directory': './temp'
            }
            opts.add_experimental_option('prefs', prefs)
            opts.add_argument('--enable-print-browser')
            #opts.add_argument('--headless')
            opts.add_argument('--kiosk-printing')
        else:
            opts = Options()
        opts.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)

        crawler = chrome_crawler.SamsungChromeCrawler(driver)
    elif module == 'firefox':
        #https://stackoverflow.com/questions/64371749/how-can-i-get-selenium-geckodriver-to-work
        #driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        crawler = firefox_crawler.SamsungFirefoxCrawler(driver)
    else:
        exit()

    """
https://samsung-dummy.tpcg.co.kr/sec/smartphones/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s24-ultra-s928/SM-S928NZTNKOO/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s24-ultra-s928-cpo/SM-S928NLBNKOO/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s24-plus-s926/SM-S926NZVEKOO/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s24-plus-s926-cpo/SM-S926NLBEKOO/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s24-s921/SM-S921NZYFKOO/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s24-s921-cpo/SM-S921NLBFKOO/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s24-ultra-sm-s928/SM-S928NZTEKOD/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s24-plus-sm-s926/SM-S926NZVAKOD/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s24-sm-s921/SM-S921NZYEKOD/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s23-fe-5g-sm-s711/SM-S711NZPWKOO/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s23-fe-5g-sm-s711-cpo/SM-S711NZBWKOO/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s23-fe-5g-s711/SM-S711NZPWKOD/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s23-ultra-s918/SM-S918NZGEKOO/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s23-s916/SM-S916NLIAKOO/
https://samsung-dummy.tpcg.co.kr/sec/smartphones/galaxy-s23-s911/SM-S911NZEEKOO/
    """

    models = [
        ("galaxy-s24-ultra-s928", "SM-S928NZTNKOO"),
        ("galaxy-s24-ultra-s928-cpo", "SM-S928NLBNKOO"),
        ("galaxy-s24-plus-s926", "SM-S926NZVEKOO"),
        ("galaxy-s24-plus-s926-cpo", "SM-S926NLBEKOO"),
        ("galaxy-s24-s921", "SM-S921NZYFKOO"),
        ("galaxy-s24-s921-cpo", "SM-S921NLBFKOO"),
        ("galaxy-s24-ultra-sm-s928", "SM-S928NZTEKOD"),
        ("galaxy-s24-plus-sm-s926", "SM-S926NZVAKOD"),
        ("galaxy-s24-sm-s921", "SM-S921NZYEKOD"),
        ("galaxy-s23-fe-5g-sm-s711", "SM-S711NZPWKOO"),
        ("galaxy-s23-fe-5g-sm-s711-cpo", "SM-S711NZBWKOO"),
        ("galaxy-s23-fe-5g-s711", "SM-S711NZPWKOD"),
        ("galaxy-s23-ultra-s918", "SM-S918NZGEKOO"),
        ("galaxy-s23-s916", "SM-S916NLIAKOO"),
        ("galaxy-s23-s911", "SM-S911NZEEKOO")
    ]

    if process == 'retrieve':
        pass
    elif process == 'retry':
        pass
    elif process == 'check':
        pass
    elif process == 'html':
        """
        python main.py --process html
        """

        """
        models = [
            ("galaxy-s24-ultra-s928", "SM-S928NZTNKOO")
        ]
        """

        #model_name = "galaxy-s24-ultra-s928"
        #model_number = "SM-S928NZTNKOO"
        for model in models:
            model_name, model_number = model
            base_url = "https://samsung.com/sec/smartphones"
            url = "{}/{}/{}/".format(base_url, model_name, model_number)

            crawler.innerhtml(url, model_name, model_number)
            time.sleep(5)
    elif process == 'pdf':
        """
        python main.py --process pdf
        """

        """
        models = [
            ("galaxy-s24-ultra-s928", "SM-S928NZTNKOO")
        ]
        """

        #model_name = "galaxy-s24-ultra-s928"
        #model_number = "SM-S928NZTNKOO"
        for model in models:
            model_name, model_number = model
            base_url = "https://samsung.com/sec/smartphones"
            url = "{}/{}/{}/".format(base_url, model_name, model_number)

            crawler.to_pdf(url, model_name, model_number)
            time.sleep(5)
    elif process == 'download':
        """
        python main.py --process download
        """

        """
        models = [
            ("galaxy-s24-ultra-s928", "SM-S928NZTNKOO")
        ]
        """

        #model_name = "galaxy-s24-ultra-s928"
        #model_number = "SM-S928NZTNKOO"
        for model in models:
            model_name, model_number = model
            base_url = "https://samsung.com/sec/smartphones"
            url = "{}/{}/{}/".format(base_url, model_name, model_number)

            crawler.download(url, model_name, model_number)
            time.sleep(5)
    else:
        pass

    time.sleep(10)
    crawler.close()
