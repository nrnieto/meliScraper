from main import *


def fravega_crawl(url, settings):
    chrome_driver = get_driver()
    chrome_driver.get(url)
    csvfile = open("fravegaReport.csv", "a")
    chrome_driver.get(url)
    while True:
        products = dict()
        # Find all info wrappers
        products_info_wrapper = chrome_driver.find_elements_by_name(settings["info_wrapper"])
        # Iterate though products and get names an prices
        for product in products_info_wrapper:
            products["name"] = product.find_element_by_name(settings["product_name_attribute"]).text
            products["list_price"] = float(delete_comma_cents(product.find_element_by_name(FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE).text.split("$ ")[1:][0]))
            try:
                products["discount_price"] = float(delete_comma_cents(product.find_element_by_name(FRAVEGA_WEBSITE_PRODUCT_PRICE_ATTRIBUTE).text.split("$ ")[1:][1]))
            except IndexError:
                products["discount_price"] = None
            print(products)
            csvfile.write(str(products["name"]) + "," + str(products["list_price"]) + "," + str(products["discount_price"])+ "\n")
        # Check if next page element existst
        if not check_if_element_exists_by_class_name("ant-pagination-disabled", chrome_driver):
            try:
                # Try clicking it
                chrome_driver.find_element_by_class_name(FRAVEGA_WEBSITE_NEXT_PAGE_CLASS).click()
            except NoSuchElementException:
                csvfile.close()
                break
        else:
            chrome_driver.close()
            csvfile.close()
            break


start_time = time.time()
print("Fravega")
csvfile = open("fravegaReport.csv", "a")
csvfile.write(FRAVEGA_CRAWLER_SETTINGS["company"] + "," + "list_price" + "," + "discount_price" + "\n")
csvfile.close()
for section in FRAVEGA_WEBSITE_SECTIONS:
    fravega_crawl(FRAVEGA_WEBSITE+section, FRAVEGA_CRAWLER_SETTINGS)
