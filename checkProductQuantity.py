import requests
from bs4 import BeautifulSoup as BSoup
import string
import os
from models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)
Session = sessionmaker()
session = Session(bind=engine)

FRAVEGA_TV_SITEMAP = "https://www.fravega.com/sitemap-category-1000004-tv.xml"
os.environ['HTTPS_PROXY'] = ''
os.environ['HTTP_PROXY'] = ''

tv_bs_obj = BSoup(requests.get(FRAVEGA_TV_SITEMAP).content, 'lxml')


def fravega_check(url):
    bs_obj = BSoup(requests.get(url).content, "lxml")
    quantity = int(bs_obj.find("h4", {"class": "even"}).text.split(" ")[1].strip(string.punctuation))
    return quantity


def garbarino_check(url):
    bs_obj = BSoup(requests.get(url).content, "lxml")
    quantity = int(bs_obj.find("li", {"class": "breadcrumb-item--active"}).span.text.strip(string.punctuation).split(" ")[0])
    return quantity


print("GARBARINO AC", garbarino_check("https://www.garbarino.com/productos/aires-acondicionados-split/4278") == len(session.query(AC).filter(AC.company=="GARBARINO").all()))
print("GARBARINO TV", garbarino_check("https://www.garbarino.com/productos/tv-led-y-smart-tv/4342") == len(session.query(TV).filter(TV.company=="GARBARINO").all()))
print("FRAVEGA AC", fravega_check("https://www.fravega.com/climatizacion/aire-acondicionado/split/") == len(session.query(AC).filter(AC.company=="FRAVEGA").all()))
print("FRAVEGA TV", fravega_check(tv_bs_obj.find("loc").text) == len(session.query(TV).filter(TV.company=="FRAVEGA").all()))
