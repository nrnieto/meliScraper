from utils import *
from bs4 import BeautifulSoup as BSoup
from saveToDB import *
from selenium.common.exceptions import WebDriverException
import requests

sections = list()

FRAVEGA_TV_SITEMAP = "https://www.fravega.com/sitemap-category-1000004-tv.xml"
FRAVEGA_AC_SITEMAP = "https://www.fravega.com/sitemap-category-1000129-aire-acondicionado.xml"

tv_bs_obj = BSoup(requests.get(FRAVEGA_TV_SITEMAP).content, 'lxml')
sections.append(tv_bs_obj.find("loc").text)
ac_bs_obj = BSoup(requests.get(FRAVEGA_AC_SITEMAP).content, 'lxml')
sections.append(ac_bs_obj.find("loc").text)

def fravega_crawl(driver, url):
    i = 1
    products = list()
    try:
        driver.get(url + "#" + str(i))
    except WebDriverException as err:
        raise WebDriverException(str(err))
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
for section in sections:
    try:
        products = fravega_crawl(fravega_chrome_driver, section)
        for product in products:
            process_and_save_to_db(product)
    except WebDriverException:
        raise WebDriverException(ERR_MSG["GET_URL"])

fravega_chrome_driver.close()
