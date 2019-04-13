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
from settings import *
import csv

os.environ['HTTPS_PROXY'] = ''
os.environ['HTTP_PROXY'] = ''


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


def delete_comma_cents(price):
    return price.split(',')[0]


def fravega_crawl(url, settings):
    chrome_driver.get(url)
    while True:
        products = dict()
        products_info_wrapper = chrome_driver.find_elements_by_name(settings["info_wrapper"])
        for product in products_info_wrapper:
            products["name"] = product.find_element_by_name(settings["product_name_attribute"]).text
            products["list_price"] = float(delete_comma_cents(product.find_element_by_name(FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE).text.split("$ ")[1:][0]))
            try:
                products["discount_price"] = float(delete_comma_cents(product.find_element_by_name(FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE).text.split("$ ")[1:][1]))
            except IndexError:
                products["discount_price"] = None
            print(products)
            csvfile.write(str(products["name"]) + "," + str(products["list_price"]) + "," + str(products["discount_price"])+ "\n")
        if settings["company"] == "fravega" and not check_if_element_exists_by_class_name("ant-pagination-disabled"):
                chrome_driver.find_element_by_class_name(FRAVEGA_WEBSITE_NEXT_PAGE_CLASS).click()
                time.sleep(2)  # make sure page finishes rendering
        else:
            #  chrome_driver.close()
            csvfile.close()
            break


def garbarino_crawl(url, settings):
    chrome_driver.get(url)
    while True:
        products = dict()
        products_info_wrapper = chrome_driver.find_elements_by_class_name(settings["info_wrapper"])
        for product in products_info_wrapper:
            products["name"] = product.find_element_by_class_name(settings["product_name_attribute"]).text
            try:
                products["list_price"] = float(delete_comma_cents(product.find_element_by_class_name(GARBARINO_WEBSITE_PRODUCT_PRICE_ATTRIBUTE).text.strip("$")).split()[0])
            except IndexError:
                products["list_price"] = float(delete_comma_cents(product.find_element_by_class_name(GARBARINO_WEBSITE_PRODUCT_PRICE_DISCOUNT_ATTRIBUTE).text.strip("$")))
            try:
                products["discount_price"] = float(delete_comma_cents(product.find_element_by_class_name(GARBARINO_WEBSITE_PRODUCT_PRICE_DISCOUNT_ATTRIBUTE).text.strip("$")))
            except IndexError:
                products["discount_price"] = None
            print(products)
            csvfile.write(str(products["name"]) + "," + str(products["list_price"]) + "," + str(products["discount_price"])+ "\n")
        if settings["company"] == "fravega" and not check_if_element_exists_by_class_name("ant-pagination-disabled"):
                chrome_driver.find_element_by_class_name(FRAVEGA_WEBSITE_NEXT_PAGE_CLASS).click()
                time.sleep(2)  # make sure page finishes rendering
        else:
            #  chrome_driver.close()
            break


# Get web page
for section in FRAVEGA_WEBSITE_SECTIONS:
    csvfile = open("report.csv", "a")
    csvfile.write(FRAVEGA_CRAWLER_SETTINGS["company"] + "," + "list_price" + "," + "discount_price" + "\n")
    fravega_crawl(FRAVEGA_WEBSITE+section, FRAVEGA_CRAWLER_SETTINGS)
    csvfile = open("report.csv", "a")
    csvfile.write(GARBARINO_CRAWLER_SETTINGS["company"] + "," + "list_price" + "," + "discount_price" + "\n")
for section in GARBARINO_WEBSITE_SECTIONS:
    garbarino_crawl(GARBARINO_WEBSITE+section, GARBARINO_CRAWLER_SETTINGS)
