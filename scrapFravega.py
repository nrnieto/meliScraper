from main import *
import time
from bs4 import BeautifulSoup as BSoup


def fravega_crawl(fravega_chrome_driver, url, settings):
    fravega_chrome_driver.get(url)
    csvfile = open("fravegaReport.csv", "a")
    bs_obj = BSoup(fravega_chrome_driver.page_source, 'lxml')
    products_info_wrapper = bs_obj.find_all("div", {"name": settings["info_wrapper"]})
    while True:
        products = dict()
        # Find all info wrappers
        # Iterate though products and get names an prices
        for product in products_info_wrapper:
            products["name"] = product.find("h2", {"name": settings["product_name_attribute"]}).text
            products["list_price"] = float(delete_comma_cents(product.find("p", {"class": FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE}).text.split("$ ")[1:][0]))
            try:
                products["discount_price"] = float(delete_comma_cents(product.find("p", {"class": FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE}).text.split("$ ")[1:][1]))
            except IndexError:
                products["discount_price"] = None
            print(products)
            #csvfile.write(str(products["name"]) + "," + str(products["list_price"]) + "," + str(products["discount_price"])+ "\n")
        # Check if next page element exists
        if not check_if_element_exists_by_class_name("ant-pagination-disabled", fravega_chrome_driver):
            try:
                # Try clicking it
                fravega_chrome_driver.find_element_by_class_name(FRAVEGA_WEBSITE_NEXT_PAGE_CLASS).click()
            except NoSuchElementException:
                #csvfile.close()
                break
        else:
            #fravega_chrome_driver.close()
            #csvfile.close()
            break


start_time = time.time()
chrome_options = Options()
chrome_options.add_argument("--headless")
fravega_chrome_driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options)
fravega_chrome_driver.set_window_size(1280, 720)  # load desktop version (macbook air res)---
#csvfile = open("fravegaReport.csv", "a")
#csvfile.write(FRAVEGA_CRAWLER_SETTINGS["company"] + "," + "list_price" + "," + "discount_price" + "\n")
#csvfile.close()
for section in FRAVEGA_WEBSITE_SECTIONS:
    fravega_crawl(fravega_chrome_driver, FRAVEGA_WEBSITE+section, FRAVEGA_CRAWLER_SETTINGS)

print("Finished Garbarino")
fravega_chrome_driver.close()
