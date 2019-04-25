from utils import get_driver, delete_comma_cents
from bs4 import BeautifulSoup as BSoup
import requests


driver = get_driver()
FRAVEGA_TV_SITEMAP = "https://www.fravega.com/sitemap-category-1000004-tv.xml"
FRAVEGA_AC_SITEMAP = "https://www.fravega.com/sitemap-category-1000129-aire-acondicionado.xml"

tv_bs_obj = BSoup(requests.get(FRAVEGA_TV_SITEMAP).content, 'lxml')
FRAVEGA_TV_URL = tv_bs_obj.find("loc").text
ac_bs_obj = BSoup(requests.get(FRAVEGA_AC_SITEMAP).content, 'lxml')
FRAVEGA_AC_URL = ac_bs_obj.find("loc").text
print(FRAVEGA_AC_URL, FRAVEGA_TV_URL)
i=1
products = []

while True:
    url = FRAVEGA_TV_URL + "#" + str(i)
    tv_bs_obj = BSoup(requests.get(url).content, 'lxml')
    products_info_wrapper = tv_bs_obj.find_all("div", {"class": "wrapData"})
    if products_info_wrapper:
        for product in products_info_wrapper:
            product_dict = {"description": product.find("h2").text}
            product_dict["list_price"] = int(delete_comma_cents(product.find("em", {"class": "ListPrice"}).text.split("$ ")[1:][0].replace(".","")))
            try:
                product_dict["discount_price"] = int(delete_comma_cents(
                    product.find("em", {"class": "BestPrice"}).text.split("$ ")[1:][0].replace(
                        ".", "")))
            except IndexError:
                product_dict["discount_price"] = product_dict["list_price"]
            product_dict["company"] = "FRAVEGA"
            product_dict["href"] = product.find("a")["href"]
            products.append(product_dict)
        i+=1
    else:
        break

print(products)
