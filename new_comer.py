import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

def move_menu(driver, menu):

    menus = {
        "가입인사": "fldlink_Q4Ol_320",
        "개인 훈련일지": "fldlink_POGp_342",
        "정모 및 일요훈련": "fldlink_Q4xl_361",
        "지구별 평일훈련": "fldlink_Q4xj_359",
        "번개훈련": "fldlink_Q4xj_359",
    }

    try:
        menu_id = menus[menu]
        menu_page = driver.find_element(By.ID, menu_id)
        #login_button = driver.find_element_by_id('loginout')
        #driver.find_elements(By.TAG_NAME, 'img')
        menu_page.click()
        time.sleep(5)
    except KeyError as e:
        print(e)
