from utils import *
import time
from bs4 import BeautifulSoup as BSoup
import string


def garbarino_crawl(garbarino_chrome_driver, url, settings, csvfile):
    garbarino_chrome_driver.get(url)
    while True:
        products = dict()
        garbarino_chrome_driver.get(garbarino_chrome_driver.current_url)
        bs_obj = BSoup(garbarino_chrome_driver.page_source, 'lxml')
        products_info_wrapper = bs_obj.find_all("div", {"class": settings["info_wrapper"]})
        for product in products_info_wrapper:
            products["name"] = product.find("h3", {"class": settings["product_name_attribute"]}).text
            try:
                products["list_price"] = int(delete_comma_cents(product.find("span", {"class": GARBARINO_WEBSITE_PRODUCT_PRICE_ATTRIBUTE}).text.strip("$"+string.punctuation+string.whitespace).split()[0].replace(".","")))
            except IndexError:
                products["list_price"] = int(delete_comma_cents(product.find("span", {"class": GARBARINO_WEBSITE_PRODUCT_PRICE_DISCOUNT_ATTRIBUTE}).text.strip("$"+string.punctuation+string.whitespace).split()[0].replace(".","")))
                products["discount_price"] = products["list_price"]
            try:
                products["discount_price"] = float(delete_comma_cents(product.find("span", {"class": GARBARINO_WEBSITE_PRODUCT_PRICE_DISCOUNT_ATTRIBUTE}).text.strip("$"+string.punctuation+string.whitespace).split()[0].replace(".","")))
            except IndexError:
                products["discount_price"] = products["list_price"]
            print(products)
            csvfile.write(str(products["name"]) + "," + str(products["list_price"]) + "," + str(products["discount_price"])+ "\n")
        # Try clicking next page element
        try:    # TODO simplify xpath
            garbarino_chrome_driver.find_elements_by_xpath("/html/body/div[4]/div[3]/div[2]/nav/ul/li[4]/a")[0].click()
        except IndexError:
            break


csvfile = open("garbarinoReport.csv", "a")
start_time = time.time()
chrome_options = Options()
chrome_options.add_argument("--headless")
garbarino_chrome_driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)
garbarino_chrome_driver.set_window_size(1280, 720)  # load desktop version (macbook air res)---
csvfile.write(GARBARINO_CRAWLER_SETTINGS["company"] + "," + "list_price" + "," + "discount_price" + "\n")
for section in GARBARINO_WEBSITE_SECTIONS:
    garbarino_crawl(garbarino_chrome_driver, GARBARINO_WEBSITE+section, GARBARINO_CRAWLER_SETTINGS, csvfile)

print("Finished Garbarino")
garbarino_chrome_driver.close()
csvfile.close()
