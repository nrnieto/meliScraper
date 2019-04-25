import grequests
import time
import os
from models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup as BSoup
from bs4 import SoupStrainer

from lxml.html import fromstring, tostring
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)
Session = sessionmaker()
session = Session(bind=engine)


def simple_request(url):
    page = requests.get(url)
    return page


ac_urls = session.query(AC.href).all()
tv_urls = session.query(TV.href).all()

print(len(ac_urls)+len(tv_urls), "products")
start_time = time.time()
acs = (grequests.get(u[0]) for u in ac_urls)
print(grequests.map(acs))
tvs = (grequests.get(u[0]) for u in tv_urls)
mapped_tvs = grequests.map(tvs)

only_product_title = SoupStrainer("h1")
for tv in mapped_tvs:
    tree = fromstring(str(tv.content))
    fixed_html = tostring(tree, pretty_print=True)
    if tree.xpath("//h1")[0].text:
        print(tree.xpath("//h1")[0].text)
    else:
        print(tree.xpath('//*[contains(@class, "productName")]')[0].text)

print(int(time.time()-start_time), "seconds")
print(len(ac_urls)+len(tv_urls)//int(time.time()-start_time), "url/sec")

