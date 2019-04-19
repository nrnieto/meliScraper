from models import *
from sqlalchemy.exc import IntegrityError
from settings import TV_COMMON_WORDS, AC_COMMON_WORDS, RESOLUTION_DICT
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import requests
from bs4 import BeautifulSoup as BSoup
import re
from utils import get_driver


engine = create_engine('sqlite:///products.db')
try:
    Base.metadata.create_all(engine)
except OperationalError:
    pass
Session = sessionmaker()
session = Session(bind=engine)


def populate_tv_object(product):
    tv = TV()
    list_of_tv_attributes = [attribute for attribute in dir(tv) if
                             not attribute.startswith("_") and attribute != "metadata" and attribute != "timestamp"]
    for attribute in list_of_tv_attributes:
        try:
            setattr(tv, attribute, product[attribute])
        except Exception:
            continue
    return tv


def populate_ac_object(product):
    ac = AC()
    list_of_ac_attributes = [attribute for attribute in dir(ac) if
                             not attribute.startswith("_") and attribute != "metadata" and attribute != "timestamp" and attribute != "model"]
    for attribute in list_of_ac_attributes:
        try:
            setattr(ac, attribute, product[attribute])
        except Exception as err:
            continue
    return ac


def process_hyundai_tv(product):  # workaround!!!!!
    description_components = string_to_upper_list(product["description"])
    tv = TV()
    list_of_tv_attributes = [attribute for attribute in dir(tv) if not attribute.startswith("_") and attribute != "metadata" and attribute != "timestamp"]
    product["brand"] = description_components[-2]
    product["size"] = description_components[-1].split("-")[1][:2]
    product["model"] = description_components[-1].replace("-", "")
    product["resolution"] = description_components[2]
    product["id"] = product["href"].split("-")[-1]
    for attribute in list_of_tv_attributes:
        setattr(tv, attribute, product[attribute])
    save_tv_to_db(tv)


def process_tv(product):
    try:
        product["brand"] = str()
        product["resolution"] = str()
        description_components = string_to_upper_list(product["description"])
        for component in description_components:
            if component in TV_COMMON_WORDS[product["company"]]["BRAND"]:
                if component == "HYUNDAI":
                    process_hyundai_tv(product)
                product["brand"] += component
            elif component in TV_COMMON_WORDS[product["company"]]["SIZE"]:
                product["size"] = int(component.strip('"').strip('”'))
            elif component in TV_COMMON_WORDS[product["company"]]["RESOLUTION"]:
                product["resolution"] += component
        if product["resolution"] in RESOLUTION_DICT["4K"]:
            product["resolution"] = "4K"
        product["model"] = description_components[-1].replace("-", "")
        product["id"] = product["href"].split("-")[-1]
        tv = populate_tv_object(product)
        return tv
    except Exception as err:
        raise err


def process_and_save_to_db(product):
    for component in product["description"].split(" "):
        if component.upper() in TV_COMMON_WORDS[product["company"]]["NAME"]:
            tv = process_tv(product)
            save_tv_to_db(tv)
            break
        elif component.upper() in AC_COMMON_WORDS[product["company"]]["NAME"]:
            ac = process_ac(product)
            save_ac_to_db(ac)
            break


def save_to_db(element):
    session.add(element)
    session.commit()
    session.close()


def save_tv_to_db(element):
    session.rollback()
    if not session.query(TV).filter_by(id=element.id).first():
        print("New element", element.id, element.company, element.href)
        save_to_db(element)
    else:
        session.query(TV).filter_by(id=element.id).delete()
        session.query(Product).filter_by(id=element.id).delete()
        print("Element exists", element.id, element.company, element.href)
        save_to_db(element)


def save_ac_to_db(element):
    session.rollback()
    if not session.query(AC).filter_by(id=element.id).first():
        print("New element", element.id, element.company, element.href)
        save_to_db(element)
    else:
        session.query(AC).filter_by(id=element.id).delete()
        session.query(Product).filter_by(id=element.id).delete()
        print("Element exists", element.id, element.company, element.href)
        save_to_db(element)


def string_to_upper_list(description):
    return list(map(lambda x: x.upper(), (description.split(" "))))


def process_ac(product):
    try:
        product["brand"] = str()
        description_components = string_to_upper_list(product["description"])
        if "" in description_components:
            description_components.remove("")
        for component in description_components:
            if component in AC_COMMON_WORDS[product["company"]]["BRAND"]:
                if product["brand"]:
                    product["brand"] += component
                else:
                    product["brand"] = component
                continue
            elif component[-1] in AC_COMMON_WORDS[product["company"]]["POWER"] and len(component[:-1]) != 0:
                product["power"] = component[:-1]
            elif component in AC_COMMON_WORDS[product["company"]]["POWER"]:
                product["power"] = description_components[description_components.index(component)-1]
            elif component in AC_COMMON_WORDS[product["company"]]["HEAT"]:
                product["heat"] = True
            else:
                if "FG" in component:
                    product["power"] = component.strip("FG")
        if description_components[-3] not in AC_COMMON_WORDS[product["company"]]["POWER"] and product["company"] != "GARBARINO":
            product["model"] = description_components[-3].replace("-", "")
        product["id"] = product["href"].split("-")[-1]
        ac = populate_ac_object(product)
        return ac
    except Exception as err:
        raise err
