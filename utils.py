from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from settings import *
import os

os.environ['HTTPS_PROXY'] = ''
os.environ['HTTP_PROXY'] = ''


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)
    chrome_driver.set_window_size(1440, 900)  # load desktop version (macbook air res)---
    return chrome_driver


def check_if_element_exists_by_class_name(class_name, chrome_driver):
    try:
        element = chrome_driver.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    if element.get_attribute("title") == "Next Page":
        return True
    return False


def delete_comma_cents(price):
    return price.split(',')[0]
