import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

def login(driver):
    # Switch using iframe indexes
    #driver.switch_to.frame(0)
    driver.switch_to.frame("down")

    # Switch using iframe element
    #main_frame = driver.find_element_by_css_selector('iframe.down')
    #driver.switch_to.frame(main_frame)

    login_button = driver.find_element(By.ID, 'loginout')
    #login_button = driver.find_element_by_id('loginout')
    #driver.find_elements(By.TAG_NAME, 'img')
    login_button.click()
    time.sleep(5)

    # 페이지 이동 후 정보 획득
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[0])
    kakao_login_button = driver.find_element(By.CLASS_NAME, 'link_klogin')
    kakao_login_button.click()
    time.sleep(5)

    # 로그인 페이지
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[0])
    #element = driver.find_element(By.ID, "")
    #element = driver.find_element(By.TAG_NAME, "body")
    #html = element.get_attribute("innerHTML")
    #print(html)

    #kakao_login_id = driver.find_element(By.ID, 'loginId--1')
    kakao_login_id = driver.find_element(By.NAME, 'loginId')
    kakao_login_id.send_keys('sjkim71@gmail.com')
    #kakao_login_pw = driver.find_element(By.ID, 'password--2')
    kakao_login_pw = driver.find_element(By.NAME, 'password')
    kakao_login_pw.send_keys('cjfdls2017!')
    #kakao_login_simple = driver.find_element(By.NAME, 'saveSignedIn')
    #kakao_login_simple = driver.find_element(By.CSS_SELECTOR, 'input.inp_choice')
    kakao_login_simple = driver.find_element(By.CSS_SELECTOR, 'div.item_choice')
    kakao_login_simple.click()
    #kakao_login_simple.send_keys('true')
    #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.inp_choice"))).click()
    """
    selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element <input type="checkbox" id="saveSignedIn--4" class="inp_choice" name="saveSignedIn" value="false"> is not clickable at point (455, 371). Other element would receive the click: <label class="lab_choice" for="saveSignedIn--4" id="label-saveSignedIn">...</label>
    """
    time.sleep(5)

    #kakao_login_button = driver.find_element(By.CLASS_NAME, 'btn_g highlight submit')
    kakao_login_button = driver.find_element(By.CSS_SELECTOR, '.btn_g.highlight.submit')
    #kakao_login_button = driver.find_element(By.CSS_SELECTOR, '.confirm_btn')
    kakao_login_button.click()
    time.sleep(5)

    # 로그인 후 cafe 화면으로 이동
    #driver.save_screenshot('login_results.png')
    #driver.get("https://cafe.daum.net/suwonmarathon")
