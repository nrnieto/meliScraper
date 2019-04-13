""" TODO Docstring """

import os
import string
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, \
    WebDriverException, StaleElementReferenceException, ElementNotVisibleException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from settings import *
import csv
from multiprocessing import Pool, cpu_count
import datetime
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


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


def initialize_web_driver():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options, desired_capabilities=caps)
    chrome_driver.set_window_size(1440, 900)  # load desktop version (macbook air res)---
    return chrome_driver


def delete_comma_cents(price):
    return price.split(',')[0]


def fravega_crawl(url, settings):
    chrome_driver = get_driver()
    chrome_driver.get(url)
    csvfile = open("report.csv", "a")
    chrome_driver.get(url)
    while True:
        products = dict()
        # Find all info wrappers
        products_info_wrapper = chrome_driver.find_elements_by_name(settings["info_wrapper"])
        # Iterate though products and get names an prices
        for product in products_info_wrapper:
            products["name"] = product.find_element_by_name(settings["product_name_attribute"]).text
            products["list_price"] = float(delete_comma_cents(product.find_element_by_name(FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE).text.split("$ ")[1:][0]))
            try:
                products["discount_price"] = float(delete_comma_cents(product.find_element_by_name(FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE).text.split("$ ")[1:][1]))
            except IndexError:
                products["discount_price"] = None
            print(products)
            csvfile.write(str(products["name"]) + "," + str(products["list_price"]) + "," + str(products["discount_price"])+ "\n")
        # Check if next page element existst
        if not check_if_element_exists_by_class_name("ant-pagination-disabled", chrome_driver):
            try:
                # Try clicking it
                chrome_driver.find_element_by_class_name(FRAVEGA_WEBSITE_NEXT_PAGE_CLASS).click()
            except NoSuchElementException:
                csvfile.close()
                break
        else:
            #  chrome_driver.close()
            csvfile.close()
            break


def garbarino_crawl(url, settings):
    # Initialize webdriver
    chrome_driver = get_driver()
    # Expensive
    chrome_driver.get(url)
    csvfile = open("report.csv", "a")
    while True:
        products = dict()
        # Find all info wrappers
        products_info_wrapper = chrome_driver.find_elements_by_class_name(settings["info_wrapper"])
        # Iterate though products and get names an prices
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
        # Try clicking next page element
        try:    # TODO simplify xpath
            chrome_driver.find_elements_by_xpath("/html/body/div[4]/div[3]/div[2]/nav/ul/li[4]/a")[0].click()
        except IndexError:
            csvfile.close()
            break


start_time = time.time()
print("Fravega")
csvfile = open("report.csv", "a")
csvfile.write(FRAVEGA_CRAWLER_SETTINGS["company"] + "," + "list_price" + "," + "discount_price" + "\n")
csvfile.close()
for section in FRAVEGA_WEBSITE_SECTIONS:
    fravega_crawl(FRAVEGA_WEBSITE+section, FRAVEGA_CRAWLER_SETTINGS)


print("Garbarino")
csvfile = open("report.csv", "a")
csvfile.write(GARBARINO_CRAWLER_SETTINGS["company"] + "," + "list_price" + "," + "discount_price" + "\n")
csvfile.close()
for section in GARBARINO_WEBSITE_SECTIONS:
    garbarino_crawl(GARBARINO_WEBSITE+section, GARBARINO_CRAWLER_SETTINGS)

elapsed_time = time.time() - start_time
print(elapsed_time)
