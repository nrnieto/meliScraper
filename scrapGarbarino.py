from main import *


def garbarino_crawl(url, settings):
    # Initialize webdriver
    chrome_driver = get_driver()
    # Expensive
    chrome_driver.get(url)
    csvfile = open("garbarinoReport.csv", "a")
    while True:
        products = dict()
        # Find all info wrappers
        products_info_wrapper = chrome_driver.find_elements_by_class_name(settings["info_wrapper"])
        # Iterate though products and get names an prices
        for product in products_info_wrapper:
            products["name"] = product.find_element_by_class_name(settings["product_name_attribute"]).text
            try:
                products["list_price"] = float(delete_comma_cents(product.find_element_by_class_name(GARBARINO_WEBSITE_PRODUCT_PRICE_ATTRIBUTE).text.strip("$")).split()[0])
            except IndexError:
                products["list_price"] = float(delete_comma_cents(product.find_element_by_class_name(GARBARINO_WEBSITE_PRODUCT_PRICE_DISCOUNT_ATTRIBUTE).text.strip("$")))
            try:
                products["discount_price"] = float(delete_comma_cents(product.find_element_by_class_name(GARBARINO_WEBSITE_PRODUCT_PRICE_DISCOUNT_ATTRIBUTE).text.strip("$")))
            except IndexError:
                products["discount_price"] = None
            print(products)
            csvfile.write(str(products["name"]) + "," + str(products["list_price"]) + "," + str(products["discount_price"])+ "\n")
        # Try clicking next page element
        try:    # TODO simplify xpath
            chrome_driver.find_elements_by_xpath("/html/body/div[4]/div[3]/div[2]/nav/ul/li[4]/a")[0].click()
        except IndexError:
            csvfile.close()
            break


start_time = time.time()
print("Garbarino")
csvfile = open("garbarinoReport.csv", "a")
csvfile.write(GARBARINO_CRAWLER_SETTINGS["company"] + "," + "list_price" + "," + "discount_price" + "\n")
csvfile.close()
for section in GARBARINO_WEBSITE_SECTIONS:
    garbarino_crawl(GARBARINO_WEBSITE+section, GARBARINO_CRAWLER_SETTINGS)

elapsed_time = time.time() - start_time
print(elapsed_time)
