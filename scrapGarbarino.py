from main import *
import time
from bs4 import BeautifulSoup as BSoup
import string


def garbarino_crawl(garbarino_chrome_driver, url, settings):
    garbarino_chrome_driver.get(url)
    csvfile = open("garbarinoReport.csv", "a")
    bs_obj = BSoup(garbarino_chrome_driver.page_source, 'lxml')
    products_info_wrapper = bs_obj.find_all("div", {"class": settings["info_wrapper"]})
    while True:
        products = dict()
        # Find all info wrappers
        # Iterate though products and get names an prices
        for product in products_info_wrapper:
            products["name"] = product.find("h3", {"class": settings["product_name_attribute"]}).text
            try:
                products["list_price"] = float(delete_comma_cents(product.find("span", {"class": GARBARINO_WEBSITE_PRODUCT_PRICE_ATTRIBUTE}).text.strip("$"+string.punctuation+string.whitespace).split()[0]))
            except IndexError:
                products["list_price"] = None
            try:
                products["discount_price"] = float(delete_comma_cents(product.find("span", {"class": GARBARINO_WEBSITE_PRODUCT_PRICE_DISCOUNT_ATTRIBUTE}).text.strip("$"+string.punctuation+string.whitespace).split()[0]))
            except IndexError:
                products["discount_price"] = None
            print(products)
            #csvfile.write(str(products["name"]) + "," + str(products["list_price"]) + "," + str(products["discount_price"])+ "\n")
        # Try clicking next page element
        try:    # TODO simplify xpath
            garbarino_chrome_driver.find_elements_by_xpath("/html/body/div[4]/div[3]/div[2]/nav/ul/li[4]/a")[0].click()
        except IndexError:
            #csvfile.close()
            break


start_time = time.time()
chrome_options = Options()
chrome_options.add_argument("--headless")
garbarino_chrome_driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)
garbarino_chrome_driver.set_window_size(1280, 720)  # load desktop version (macbook air res)---
#csvfile = open("garbarinoReport.csv", "a")
#csvfile.write(GARBARINO_CRAWLER_SETTINGS["company"] + "," + "list_price" + "," + "discount_price" + "\n")
#csvfile.close()
for section in GARBARINO_WEBSITE_SECTIONS:
    garbarino_crawl(garbarino_chrome_driver, GARBARINO_WEBSITE+section, GARBARINO_CRAWLER_SETTINGS)

print("Finished Garbarino")
garbarino_chrome_driver.close()
