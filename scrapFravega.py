from utils import *
from bs4 import BeautifulSoup as BSoup
from saveToDB import *
from selenium.common.exceptions import WebDriverException


def fravega_crawl(driver, url, settings):
    """
    Crawls and returns list of products
    :param driver: driver object
    :param url: base url + section
    :param settings: crawler settings
    :return: list of products
    :return:
    """
    products = list()
    try:
        driver.get(url)
    except WebDriverException:
        raise WebDriverException(settings[ERR_MSG["GET_URL"]])
    while True:
        bs_obj = BSoup(driver.page_source, 'lxml')
        products_info_wrapper = bs_obj.find_all("div", {"name": settings["info_wrapper"]})
        for product in products_info_wrapper:
            product_dict = {"description": product.find("h2", {"name": settings["product_name_attribute"]}).text}
            product_dict["list_price"] = int(delete_comma_cents(product.find("p", {"class": FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE}).text.split("$ ")[1:][0].replace(".","")))
            try:
                product_dict["discount_price"] = int(delete_comma_cents(product.find("p", {"class": FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE}).text.split("$ ")[1:][1].replace(".","")))
            except IndexError:
                product_dict["discount_price"] = product_dict["list_price"]
            product_dict["company"] = "FRAVEGA"
            product_dict["href"] = FRAVEGA_CRAWLER_SETTINGS["url"] + product.parent["href"]
            products.append(product_dict)
        if not check_if_element_exists_by_class_name("ant-pagination-disabled", driver):
            driver.find_element_by_class_name(FRAVEGA_WEBSITE_NEXT_PAGE_CLASS).click()
        else:
            return products


fravega_chrome_driver = get_driver()
for section in FRAVEGA_WEBSITE_SECTIONS:
    try:
        products = fravega_crawl(fravega_chrome_driver, FRAVEGA_WEBSITE+section, FRAVEGA_CRAWLER_SETTINGS)
        for product in products:
            process_and_save_to_db(product)
    except WebDriverException:
        raise WebDriverException(ERR_MSG["GET_URL"])

fravega_chrome_driver.close()
