""" TODO Docstring """

import os
import string
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, \
    WebDriverException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

os.environ['HTTPS_PROXY'] = ''
os.environ['HTTP_PROXY'] = ''
FRAVEGA_WEBSITE = "https://shopping.fravega.com"  # fravega.com redirects to shopping subdomain
FRAVEGA_WEBSITE_TV_SECTION_PATH = "/tv-y-video/tv/"
FRAVEGA_WEBSITE_NEXT_PAGE_CLASS = 'ant-pagination-next'
FRAVEGA_WEBSITE_PRODUCT_NAME_ATTRIBUTE = "itemTitle"
FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE = "itemPrice"
FRAVEGA_WEBSITE_PRODUCT_INFO_WRAPPER = "infoWrapper"

CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"


def check_if_element_exists_by_class_name(class_name):
    try:
        element = chrome_driver.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    if element.get_attribute("title") == "Next Page":
        return True
    return False


# Initialize webdriver
print("Initializing driver")
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)
chrome_driver.set_window_size(1440, 900)  # load desktop version (macbook air res)

if __name__ == "__main__":
    # Get web page
    chrome_driver.get(FRAVEGA_WEBSITE+FRAVEGA_WEBSITE_TV_SECTION_PATH)
    i = 1
    while True:
        print("Page number", i)
        products = dict()
        products_info_wrapper = chrome_driver.find_elements_by_name(FRAVEGA_WEBSITE_PRODUCT_INFO_WRAPPER)
        for product in products_info_wrapper:
            products["name"] = product.find_element_by_name(FRAVEGA_WEBSITE_PRODUCT_NAME_ATTRIBUTE).text
            products["price"] = product.find_element_by_name(FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE).text
            print(products)
        if not check_if_element_exists_by_class_name("ant-pagination-disabled"):
            time.sleep(1)  # random error, make sure page loads
            chrome_driver.find_element_by_class_name(FRAVEGA_WEBSITE_NEXT_PAGE_CLASS).click()
            i+=1
        else:
            print("Done", i)
            chrome_driver.close()
            break
