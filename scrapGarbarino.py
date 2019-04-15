from utils import *
from bs4 import BeautifulSoup as BSoup
import string
from saveToDB import *


def garbarino_crawl(driver, url, settings):
    driver.get(url)
    while True:
        driver.get(driver.current_url)
        bs_obj = BSoup(driver.page_source, 'lxml')
        products_info_wrapper = bs_obj.find_all("div", {"class": settings["info_wrapper"]})
        for product in products_info_wrapper:
            product_dict = {"description": product.find("h3", {"class": settings["product_name_attribute"]}).text}
            try:
                product_dict["list_price"] = int(delete_comma_cents(product.find("span", {"class": GARBARINO_WEBSITE_PRODUCT_PRICE_ATTRIBUTE}).text.split()[0].strip("$").replace(".","")))
            except IndexError:
                product_dict["list_price"] = int(delete_comma_cents(product.find("span", {"class": GARBARINO_WEBSITE_PRODUCT_PRICE_DISCOUNT_ATTRIBUTE}).text.split()[0].strip("$").replace(".","")))
                product_dict["discount_price"] = product_dict["list_price"]
            product_dict["company"] = "GARBARINO"
            product_dict["href"] = GARBARINO_CRAWLER_SETTINGS["url"] + product.find_all("a", href=True)[0]["href"]
            product_to_db(product_dict)
            print(product_dict)
        # Try clicking next page element
        try:    # TODO simplify xpath
            driver.find_elements_by_xpath("/html/body/div[4]/div[3]/div[2]/nav/ul/li[4]/a")[0].click()
        except IndexError:
            break


garbarino_chrome_driver = get_driver()
for section in GARBARINO_WEBSITE_SECTIONS:
    garbarino_crawl(garbarino_chrome_driver, GARBARINO_WEBSITE+section, GARBARINO_CRAWLER_SETTINGS)

garbarino_chrome_driver.close()
