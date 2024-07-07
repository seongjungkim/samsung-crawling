import csv
import json
import math
import random
import os
import time
from urllib.parse import urlparse

from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException, NoAlertPresentException, ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SamsungCrawler:
    csv_file = None
    csv_writer = None
    MIN_WAITING_TIME = 5
    MAX_404_ERROR_COUNT = 5

    def __init__(self, driver, csv_file=None, csv_writer=None):
        self.driver = driver
        self.provider = 'cisco'
        self.csv_file = csv_file
        self.csv_writer = csv_writer

    def set_csv_writer(self, csv_file=None, csv_writer=None):
        self.csv_file = csv_file
        self.csv_writer = csv_writer

    def close(self):
        if self.driver:
            self.driver.quit()

    def get_error(self):
        try:
            elem_error = self.driver.find_element(By.CSS_SELECTOR, "div.error-page-area.sec-spacer")
            error_text = elem_error.text
            print(error_text)
            if "This exam page is currently offline" in error_text:
                return 1
            elif "This discussion was moved" in error_text:
                return 2
        except NoSuchElementException as e:
            #print(e)
            print("NoSuchElementException", "div.error-page-area.sec-spacer")

        try:
            elem_error = self.driver.find_element(By.CSS_SELECTOR, "div.error-page-message div.error-page")
            error_text = elem_error.text
            print(error_text)
            if "General Server Error" in error_text and \
                    ("Error Code: 1006" in error_text or \
                     "Error Code: 1002" in error_text):
                return 9
        except NoSuchElementException as e:
            #print(e)
            print("NoSuchElementException", "div.error-page-message div.error-page")

        elems = self.driver.find_elements(By.TAG_NAME, "img")
        for elem in elems:
            src_url = elem.get_attribute("src")
            print(src_url)
            # 페이지가 존재하지 않는 경우
            if "/assets/images/et/404robot.jpg" in src_url:
                return -1

        return 0

    def __get_response_status(self):
        return 200

    def _download_assets(
            self,
            requests,
            asset_dir="temp",
            default_fname="unnamed",
            skip_domains=["facebook", "google", "yahoo", "agkn", "2mdn"],
            exts=[".js", ".css", ".png", ".jpeg", ".jpg", ".svg", ".gif", ".pdf", ".bmp", ".webp", ".ico", ".webm", ".mp4"],
            append_ext=False):
    
        from mimetypes import guess_extension
        import datetime
        import os

        asset_list = {}
        for req_idx, request in enumerate(requests):
            if "https://images.samsung.com" in request.url:
                print(request)
            # request.headers
            # request.response.body is the raw response body in bytes
            if request is None or request.response is None or request.response.headers is None or 'Content-Type' not in request.response.headers:
                continue
            
            ext = guess_extension(request.response.headers['Content-Type'].split(';')[0].strip())
            if ext is None or ext == "" or ext not in exts:
                #Don't know the file extention, or not in the whitelist
                continue
            parsed_url = urlparse(request.url)
        
            skip = False
            for d in skip_domains:
                if d in parsed_url.netloc:
                    skip = True
                    break
            if skip:
                continue
        
            frelpath = parsed_url.path.strip()
            if frelpath == "":
                timestamp = str(datetime.datetime.now().replace(microsecond=0).isoformat())
                frelpath = f"{default_fname}_{req_idx}_{timestamp}{ext}"
            elif frelpath.endswith("\\") or frelpath.endswith("/"):
                timestamp = str(datetime.datetime.now().replace(microsecond=0).isoformat())
                frelpath = frelpath + f"{default_fname}_{req_idx}_{timestamp}{ext}"
            elif append_ext and not frelpath.endswith(ext):
                frelpath = frelpath + f"_{default_fname}{ext}" #Missing file extension but may not be a problem
            if frelpath.startswith("\\") or frelpath.startswith("/"):
                frelpath = frelpath[1:]
        
            fpath = os.path.join(asset_dir, parsed_url.netloc, frelpath)
            if os.path.isfile(fpath):
                continue
            os.makedirs(os.path.dirname(fpath), exist_ok=True)
            print(f"Downloading {request.url} to {fpath}")
            asset_list[fpath] = request.url

            if os.path.exists(fpath):
                continue

            try:
                with open(fpath, "wb") as file:
                    file.write(request.response.body)
            except:
                print(f"Cannot download {request.url} to {fpath}")
        return asset_list

    """
        section .content
        section .component-bar .aniAct
        section .itm-component
         - div .component-body
        # 구매혜택
         - - article .component-content .component02
        # 특장점
         - - article .component-content .component01 .close
         - - article .component-con
         - - article .compRelationGoods
        # 스펙
         - - article .component-con .spec-all .drop-component .component03
        # 설치가이드
         - - article .component-con .install-guide .drop-component .component04
        # 매뉴얼
         - - article .component-con .customer-center .drop-component .component05
        # 기타서비스
         - - article .component-con .drop-component .component11
        # 상품평 고도화
         - - article .component-con .component07
        # 카드 혜택
         - - article .component-con .drop-component .component12
        # 연관제품
         - - article .component-con .component08
        # 구매시 유의사항
         - - article .component-con .component09
         footer .footer_b2c
    """

    def innerhtml(self, url, model_name, model_number):
        status = -1
        count = 1

        print('Html', url, status, count)
        self.driver.get(url)

        time.sleep(1)
        try:
            if EC.alert_is_present():
                self.driver.switch_to.alert.accept()
        except NoAlertPresentException as e:
            #print(e)
            print("NoAlertPresentException")

        elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.dropButton')
        for element in elements:
            #print(element)
            #print(element.get_attribute('outerHTML'))
            #element.get_attribute('innerHTML')
            try:
                element.click()
            except ElementNotInteractableException:
                pass
            except ElementClickInterceptedException as e:
                pass
            time.sleep(5)

        # 현재 화면만 저장
        #self.driver.save_screenshot(model_name + ".png")

        body_element = self.driver.find_element(By.TAG_NAME, "body")

        articles = [
            ("itm-information", "## 제품 정보영역 ##", "div.itm-information.advance"),
            ("component02", "## 구매혜택 ##", "article.component-content.component02"),
            ("component01", "## 특장점 ##", "article.component-content.component01"),
            ("component03", "## 스펙 ##", "article.component-con.spec-all.drop-component.component03"),
            ("component04", "## 설치가이드 ##", "article.component-con.install-guide.drop-component.component04"),
            ("component05", "## 매뉴얼 ##", "article.component-con.customer-center.drop-component.component05"),
            ("component11", "## 기타서비스 ##", "article.component-con.drop-component.component11"),
            ("component07", "## 상품평 고도화 ##", "article.component-con.component07"),
            ("component12", "## 카드 혜택 ##", "article.component-con.drop-component.component12"),
            ("component08", "## 연관제품 ##", "article.component-con.component08")
        ]
        #articles = [ ]

        #content_element = body_element.find_element(By.CSS_SELECTOR, "section.content")
        #print(content_element.get_attribute('innerHTML'))
        #print(content_element.text)

        # https://stackoverflow.com/questions/71881074/how-to-get-all-elements-with-multiple-classes-in-selenium

        contents = { }
        for article in articles:
            component, subtitle, css_selector = article

            print('\n', subtitle, '\n')
            try:
                if '.drop-component' in css_selector:
                    elements = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))
                    for element in elements:
                        #print(element.text)
                        contents[component] = element.text
                else:
                    element = body_element.find_element(By.CSS_SELECTOR, css_selector)
                    #print(element.get_attribute('innerHTML'))
                    #print(element.text)
                    contents[component] = element.text
            except NoSuchElementException as e:
                pass
        
        #    ("component09", "## 구매시 유의사항 ##", "article.component-con.component09")

        #print(element.text)

        time.sleep(10)

        asset_dir = "temp"
        
        #model_path = os.path.join(asset_dir, model_name)
        model_path = os.path.join(asset_dir, "all")
        if not os.path.exists(model_path):
            os.makedirs(model_path)

        """
        file = open(os.path.join(asset_dir, f"{model_name}.txt"), 'w')

        #title_element = self.driver.find_element(By.TAG_NAME, "title")
        file.write(f"\n\n## 제품명 ##\n\n")
        file.write(self.driver.title)

        for article in articles:
            component, subtitle, _ = article
            text = contents[component]
            file.write(f"\n\n{subtitle}\n\n")
            file.write(text)
        """
        
        """ """
        file = open(os.path.join(asset_dir, f"{model_name}.html"), 'w')

        # Text, innerHTML, outerHTML
        #texts = self.driver.find_element(By.XPATH, "/html").text + "\n"
        #texts = self.driver.find_element(By.XPATH, "/html").get_attribute('innerHTML') + "\n"
        #texts = self.driver.find_element(By.XPATH, "/html").get_attribute('outerHTML') + "\n"

        #html = self.driver.find_element(By.XPATH, "/html/head").get_attribute('outerHTML') + "\n\n" + \
        #self.driver.find_element(By.XPATH, "/html/body").get_attribute('outerHTML') + "\n"

        # HTML 추출
        html = self.driver.find_element(By.XPATH, "/html").get_attribute('outerHTML')

        # HTML에서 script, iframe 제거
        #https://stackoverflow.com/questions/1936466/how-to-scrape-only-visible-webpage-text-with-beautifulsoup
        #https://stackoverflow.com/questions/25729589/how-to-get-html-from-a-beautiful-soup-object
        #https://www.crummy.com/software/BeautifulSoup/bs4/doc/#pretty-printing

        import json
        from bs4 import BeautifulSoup
        from bs4.element import Comment

        def tag_visible(element):
            if element.parent.name in ['script']:
                return False
            if isinstance(element, Comment):
                return False
            return True
        
        # html text 로딩
        soup = BeautifulSoup(html, 'html.parser')
        #texts = soup.findAll(text=True)
        #visible_texts = filter(tag_visible, texts)
        #texts = u" ".join(t.strip() for t in visible_texts)

        # 특정 태그 제거
        [s.extract() for s in soup(['script', 'iframe'])]
        
        #texts = soup.getText()

        # HTML tag를 간략화
        texts = soup.prettify( formatter="html" )
        print(texts)
        file.write(texts)
        """ """

        """
        print("## 구매시 유의사항 ##\n")
        file.write(f"\n\n## 구매시 유의사항 ##\n\n")
        css_selector = "article.component-con.component09"
        component09_element = body_element.find_element(By.CSS_SELECTOR, css_selector)

        css_selector = "div > li.slick-slide.slick-active > a.on"
        elements = component09_element.find_elements(By.CSS_SELECTOR, css_selector)
        for element in elements:
            try:
                element.click()
                print(element.text)
                file.write("\n" + element.text + "\n")
                time.sleep(5)

                xpath = "//div[@class='product-purchase-caus_contents tab-content' and(contains(@style, 'display: block'))]"
                purchase_cause_element = component09_element.find_element(By.XPATH, xpath)
                print(purchase_cause_element.text)
                file.write("\n" + purchase_cause_element.text + "\n")
            except ElementNotInteractableException as e:
                pass
            except ElementClickInterceptedException as e:
                pass
        """

        file.close()

        #selenium-wire
        #print('driver', type(self.driver))
        #self._download_assets(self.driver.requests, asset_dir=model_path)
        
    def download(self, url, model_name, model_number):
        status = -1
        count = 1

        print('Html', url, status, count)
        self.driver.get(url)

        time.sleep(1)
        try:
            if EC.alert_is_present():
                self.driver.switch_to.alert.accept()
        except NoAlertPresentException as e:
            #print(e)
            print("NoAlertPresentException")

        elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.dropButton')
        for element in elements:
            #print(element)
            #print(element.get_attribute('outerHTML'))
            #element.get_attribute('innerHTML')
            try:
                element.click()
            except ElementNotInteractableException:
                pass
            except ElementClickInterceptedException as e:
                pass
            time.sleep(5)

        from selenium.webdriver.common.action_chains import ActionChains

        #xpath = "//li[text()= 'A']"
        #xpath = "//div[@class='highlights-overview__carousel-slide swiper-slide swiper-slide-prev']"
        #element = self.driver.find_element(By.XPATH, xpath)
        css_selector = "div.highlights-overview__contents"
        element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
        action = ActionChains(self.driver)
        action.move_to_element(element).click().perform()
        time.sleep(5)

        #css_selector = "div.highlights-overview__navigation-button-wrap > button.highlights-overview__navigation-button"
        css_selector = "button.highlights-overview__navigation-button"
        elements = self.driver.find_elements(By.CSS_SELECTOR, css_selector)
        for element in elements:
            #print(element)
            #print(element.get_attribute('outerHTML'))
            #element.get_attribute('innerHTML')
            try:
                element.click()
            except ElementNotInteractableException:
                pass
            except ElementClickInterceptedException as e:
                pass
            time.sleep(5)

        # 현재 화면만 저장
        #self.driver.save_screenshot(model_name + ".png")

        asset_dir = "temp"
        
        #model_path = os.path.join(asset_dir, model_name)
        model_path = os.path.join(asset_dir, "all")
        if not os.path.exists(model_path):
            os.makedirs(model_path)

        #selenium-wire
        #print('driver', type(self.driver))
        self._download_assets(self.driver.requests, asset_dir=model_path)
        #time.sleep(300)

    def to_pdf(self, url, model_name, model_number):
        status = -1
        count = 1

        print('Html', url, status, count)
        self.driver.get(url)

        time.sleep(1)
        try:
            if EC.alert_is_present():
                self.driver.switch_to.alert.accept()
        except NoAlertPresentException as e:
            #print(e)
            print("NoAlertPresentException")

        elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.dropButton')
        for element in elements:
            try:
                element.click()
            except ElementNotInteractableException:
                pass
            except ElementClickInterceptedException as e:
                pass
            time.sleep(5)

        asset_dir = "temp"
        
        #model_path = os.path.join(asset_dir, model_name)
        model_path = os.path.join(asset_dir, "all")
        if not os.path.exists(model_path):
            os.makedirs(model_path)

        #https://stackoverflow.com/questions/56897041/how-to-save-opened-page-as-pdf-in-selenium-python
        #https://stackoverflow.com/questions/45576958/scrolling-to-top-of-the-page-in-python-using-selenium
        
        """
        from selenium.webdriver.common.keys import Keys
        import base64

        self.driver.find_element(By.XPATH, "/html/body").send_keys(Keys.CONTROL + Keys.HOME)
        pdf = self.driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})
        pdf_data = base64.b64decode(pdf["data"])
        file = open(os.path.join(asset_dir, f"{model_name}.pdf"), 'wb')
        file.write(pdf_data)

        file.close()
        """

        self.driver.execute_script('window.print();')

        #selenium-wire
        #print('driver', type(self.driver))
        #self._download_assets(self.driver.requests, asset_dir=model_path)
