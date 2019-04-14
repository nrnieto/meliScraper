from utils import *
import time
from bs4 import BeautifulSoup as BSoup


def fravega_crawl(fravega_chrome_driver, url, settings, csvfile):
    fravega_chrome_driver.get(url)
    while True:
        fravega_chrome_driver.get(fravega_chrome_driver.current_url)
        bs_obj = BSoup(fravega_chrome_driver.page_source, 'lxml')
        products_info_wrapper = bs_obj.find_all("div", {"name": settings["info_wrapper"]})
        for product in products_info_wrapper:
            products = dict()
            products["name"] = product.find("h2", {"name": settings["product_name_attribute"]}).text
            products["list_price"] = int(delete_comma_cents(product.find("p", {"class": FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE}).text.split("$ ")[1:][0].replace(".","")))
            try:
                products["discount_price"] = int(delete_comma_cents(product.find("p", {"class": FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE}).text.split("$ ")[1:][1].replace(".","")))
            except IndexError:
                products["discount_price"] = products["list_price"]
            print(products)
            csvfile.write(str(products["name"]) + "," + str(products["list_price"]) + "," + str(products["discount_price"])+ "\n")
            # Check if next page element exists
        if not check_if_element_exists_by_class_name("ant-pagination-disabled", fravega_chrome_driver):
            fravega_chrome_driver.find_element_by_class_name(FRAVEGA_WEBSITE_NEXT_PAGE_CLASS).click()
        else:
            break


csvfile = open("fravegaReport.csv", "a")
start_time = time.time()
chrome_options = Options()
chrome_options.add_argument("--headless")
fravega_chrome_driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)
fravega_chrome_driver.set_window_size(1280, 720)  # load desktop version (macbook air res)---
csvfile.write(FRAVEGA_CRAWLER_SETTINGS["company"] + "," + "list_price" + "," + "discount_price" + "\n")
#csvfile = open("fravegaReport.csv", "a")
#csvfile.write(FRAVEGA_CRAWLER_SETTINGS["company"] + "," + "list_price" + "," + "discount_price" + "\n")
#csvfile.close()
for section in FRAVEGA_WEBSITE_SECTIONS:
    fravega_crawl(fravega_chrome_driver, FRAVEGA_WEBSITE+section, FRAVEGA_CRAWLER_SETTINGS, csvfile)

print("Finished Fravega")
fravega_chrome_driver.close()
csvfile.close()
