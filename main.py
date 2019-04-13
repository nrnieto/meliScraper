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
FRAVEGA_WEBSITE_NEXT_PAGE_CLASS = 'ant-pagination-next'
FRAVEGA_WEBSITE_PRODUCT_NAME_ATTRIBUTE = "itemTitle"
FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE = "itemPrice"
FRAVEGA_WEBSITE_PRODUCT_INFO_WRAPPER = "infoWrapper"
FRAVEGA_WEBSITE_SECTIONS = ["/tv-y-video/tv/", "/heladeras-freezers-y-cavas/", "/lavado/", "/climatizacion/"]

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
#chrome_options.add_argument("--headless")
chrome_driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)
chrome_driver.set_window_size(1440, 900)  # load desktop version (macbook air res)


def delete_comma_cents(price):
    return price.split(',')[0]


def crawl(url):
    n = 1
    i = 1
    chrome_driver.get(url)
    while True:
        print("Page number", i)
        products = dict()
        products_info_wrapper = chrome_driver.find_elements_by_name(FRAVEGA_WEBSITE_PRODUCT_INFO_WRAPPER)
        for product in products_info_wrapper:
            products["name"] = product.find_element_by_name(FRAVEGA_WEBSITE_PRODUCT_NAME_ATTRIBUTE).text
            products["list_price"] = float(delete_comma_cents(product.find_element_by_name(FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE).text.split("$ ")[1:][0]))
            try:
                products["discount_price"] = float(delete_comma_cents(product.find_element_by_name(FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE).text.split("$ ")[1:][1]))
            except IndexError:
                products["discount_price"] = None
            print(products, n)
            n+=1
        if not check_if_element_exists_by_class_name("ant-pagination-disabled"):
            chrome_driver.find_element_by_class_name(FRAVEGA_WEBSITE_NEXT_PAGE_CLASS).click()
            time.sleep(2)  # make sure page finishes rendering
            i += 1
        else:
            #  chrome_driver.close()
            break


if __name__ == "__main__":
    # Get web page
    for section in FRAVEGA_WEBSITE_SECTIONS:
        crawl(FRAVEGA_WEBSITE+section)
