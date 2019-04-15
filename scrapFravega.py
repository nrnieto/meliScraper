from utils import *
from bs4 import BeautifulSoup as BSoup
from saveToDB import *


def fravega_crawl(driver, url, settings):
    driver.get(url)
    while True:
        driver.get(driver.current_url)
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
            product_to_db(product_dict)
            print(product_dict)
            # Check if next page element exists
        if not check_if_element_exists_by_class_name("ant-pagination-disabled", driver):
            driver.find_element_by_class_name(FRAVEGA_WEBSITE_NEXT_PAGE_CLASS).click()
        else:
            break


fravega_chrome_driver = get_driver()
for section in FRAVEGA_WEBSITE_SECTIONS:
    fravega_crawl(fravega_chrome_driver, FRAVEGA_WEBSITE+section, FRAVEGA_CRAWLER_SETTINGS)


fravega_chrome_driver.close()
