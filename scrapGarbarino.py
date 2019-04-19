from utils import *
from bs4 import BeautifulSoup as BSoup
from saveToDB import *
from settings import ERR_MSG


def get_garbarino_product_price_by_classname(product, classname):
    try:
        element = product.find("span", {"class": classname}).text.strip()
    except AttributeError:
        return None
    if element:
        return int(delete_comma_cents(element.split()[0].strip("$").replace(".","")))
    return None  # no list price


def garbarino_crawl(driver, url, settings):
    """
    Crawls and returns list of products
    :param driver: driver object
    :param url: base url + section
    :param settings: crawler settings
    :return: list of products
    """
    products = list()
    try:
        driver.get(url)
    except WebDriverException or TimeoutException:
        driver.close()
        raise WebDriverException()
    while True:
        bs_obj = BSoup(driver.page_source, 'lxml')
        products_info_wrapper = bs_obj.find_all("div", {"class": settings["info_wrapper"]})
        for product in products_info_wrapper:
            try:
                product_data = {"description": product.find("h3", {"class": settings["product_name_attribute"]}).text,
                                "company": "GARBARINO"}
            except AttributeError:
                raise AttributeError(settings[ERR_MSG["FIND_ELEMENT"]])
            try:
                product_data["list_price"] = get_garbarino_product_price_by_classname(product, GARBARINO_WEBSITE_PRODUCT_PRICE_ATTRIBUTE)
                product_data["discount_price"] = get_garbarino_product_price_by_classname(product, GARBARINO_WEBSITE_PRODUCT_PRICE_DISCOUNT_ATTRIBUTE)
            except AttributeError:
                raise AttributeError(settings[ERR_MSG["FIND_ELEMENT"]])
            product_data["href"] = GARBARINO_CRAWLER_SETTINGS["url"] + product.find_all("a", href=True)[0]["href"]
            products.append(product_data)
        try:
            next_page_arrow = bs_obj.find_all("li", {"class": "pagination__page"})[-1].span
        except Exception:
            return products
        if next_page_arrow:
            driver.find_elements_by_class_name("pagination__page")[-1].click()
        else:
            return products


garbarino_chrome_driver = get_driver()
for section in GARBARINO_WEBSITE_SECTIONS:
    try:
        products = garbarino_crawl(garbarino_chrome_driver, GARBARINO_WEBSITE+section, GARBARINO_CRAWLER_SETTINGS)
        for product in products:
            process_and_save_to_db(product)
    except WebDriverException:
        raise WebDriverException(ERR_MSG["GET_URL"])


garbarino_chrome_driver.close()
