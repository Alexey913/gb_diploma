from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


import time
import re

import webbrowser

import platform

from winreg import *
 
# def get_win_browser():
    
#     with OpenKey(HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice") as key:
#         return QueryValueEx(key, 'Progid')[0]
        
# def get_other_browser():
#     browser = webbrowser.get()
#     return browser.name

# def get_default_browser():
#     if platform.system() == "Windows":
#         return get_win_browser()
#     else:
#         return get_other_browser()
    
 
# default_browser = get_default_browser()
# print(default_browser)

# if 'Edge' in default_browser:
#     driver=webdriver.Edge()
# elif 'Chrome' or 'Yandex' or 'Opera' in default_browser:
#     driver=webdriver.Chrome()
# elif 'Firefox' in default_browser:
#     driver=webdriver.Firefox
# elif 'Ie' in default_browser:
#     driver=webdriver.Ie
# elif 'Proxy' in default_browser:
#     driver=webdriver.Proxy
# elif 'Safari' in default_browser:
#     driver=webdriver.Safari
# else:
#     raise RuntimeError('Для работы необходим браузер Chrome, Edge, Internet Explorer, Safari или Proxi')

# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# firefox_binary = FirefoxBinary("D:\\Firefox Portable\\FirefoxPortable\\firefox.exe")
# driver = webdriver.Firefox(firefox_binary=firefox_binary)


options = Options()
options.headless = True

driver = webdriver.Chrome(options=options)
# driver.maximize_window()
driver.get('https://lk.gosuslugi.ru/profile?')


username = '79290027022'
pwd = 'T637kn24091990!'
WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.NAME, 'Телефон  /  Email  /  СНИЛС')))

login = driver.find_element(By.NAME, 'Телефон  /  Email  /  СНИЛС')
WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.NAME, 'Пароль')))
password = driver.find_element(By.NAME, 'Пароль')
WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, '//button[normalize-space()="Войти"]')))
but = driver.find_element(By.XPATH, '//button[normalize-space()="Войти"]')
login.send_keys(username)
password.send_keys(pwd)
but.send_keys(Keys.RETURN)
WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'esia-code-input')))

phone_code_in_page = driver.find_elements(By.TAG_NAME, 'input')
for i in phone_code_in_page:
    print(i.tag_name)
# field = driver.find_element(By.XPATH, '/html/body/esia-root/div/esia-login/div/div/esia-enter-mfa/esia-otp/div/form/div/esia-code-input/div/code-input/span[1]/input')
# print(field.tag_name)
phone_code = input('Введите код из смс:\n')
# field.send_keys(int(phone_code[0]))
# time.sleep(10)
for elem, field in zip(phone_code, phone_code_in_page):
    field.send_keys(int(elem))

WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, '//p[normalize-space()="Документы и данные"]')))
doc = driver.find_element(By.XPATH, '//p[normalize-space()="Документы и данные"]')
doc.click()

# WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.TAG_NAME, 'html')))
# with open("page_2.html", "w", encoding="utf-8") as file:
#     file.write(driver.page_source)
# driver.quit()
# print('---------------')
# for i in phone_code_in_page:
#     print(i.text)
#     print(i)    
# print('---------------')
# for elem
# time.sleep(10)
# if driver.title == "Портал государственных услуг Российской Федерации":
#     time.sleep(2)
#     driver.close()
# else:
#     time.sleep(10)
# time.sleep(5)
# driver.find_element_by_value('Документы').click()
# page_source = driver.page_source


# url = webbrowser.open_new_tab('https://esia.gosuslugi.ru/login/')
# webbrowser.get(url)