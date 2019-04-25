from utils import *
from bs4 import BeautifulSoup as BSoup
from saveToDB import *
from selenium.common.exceptions import WebDriverException


def fravega_crawl(driver, url, settings):
    i=1
    products = list()
    try:
        driver.get(url + "#" + str(i))
    except WebDriverException:
        raise WebDriverException(settings[ERR_MSG["GET_URL"]])
    bs_obj = BSoup(driver.page_source, 'lxml')
    pages = bs_obj.find("div", {"class": "pager bottom"}).find_all("li", {"class": "page-number"})
    for page in pages:
        driver.get(url + "#" + str(i))
        driver.refresh()
        bs_obj = BSoup(driver.page_source, 'lxml')
        products_info_wrapper = bs_obj.find_all("div", {"class": "wrapData"})
        for product in products_info_wrapper:
            product_dict = {"description": product.find("h2").text}
            product_dict["list_price"] = int(delete_comma_cents(product.find("em", {"class": "ListPrice"}).text.split("$ ")[1:][0].replace(".","")))
            try:
                product_dict["discount_price"] = int(delete_comma_cents(product.find("em", {"class": "BestPrice"}).text.split("$ ")[1:][0].replace(".", "")))
            except IndexError:
                product_dict["discount_price"] = product_dict["list_price"]
            product_dict["company"] = "FRAVEGA"
            product_dict["href"] = product.find("a")["href"]
            products.append(product_dict)
        i += 1
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
