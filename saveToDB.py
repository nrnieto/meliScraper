from models import *
from sqlalchemy.exc import IntegrityError
from settings import TV_COMMON_WORDS, AC_COMMON_WORDS
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)
Session = sessionmaker()
session = Session(bind=engine)


def process_tv(product):
    try:
        tv = TV()
        tv.brand = ""
        tv.resolution = ""
        description_components = string_to_upper_list(product["description"])
        for component in description_components:
            if component in TV_COMMON_WORDS[product["company"]]["BRAND"]:
                tv.brand += component
            elif component in TV_COMMON_WORDS[product["company"]]["SIZE"]:
                tv.id = product["company"] + description_components[-1] + str(component.strip('"'))
                tv.size = int(component.strip('"'))
            elif component in TV_COMMON_WORDS[product["company"]]["RESOLUTION"]:
                tv.resolution += component
                if tv.resolution == "4KULTRAHD" or tv.resolution == "4KUHD":
                    tv.resolution = "4K"
        tv.model = description_components[-1]
        tv.list_price = product["list_price"]
        tv.discount_price = product["discount_price"]
        tv.company = product["company"]
        tv.href = product["href"]
        save_tv_to_db(tv)
    except Exception as err:
        print(str(err))


def product_to_db(product):
    for component in product["description"].split(" "):
        if component.upper() in TV_COMMON_WORDS[product["company"]]["NAME"]:
            process_tv(product)
            break
        elif component.upper() in AC_COMMON_WORDS[product["company"]]["NAME"]:
            process_ac(product)
            break
    session.close()


def save_tv_to_db(tv):
    session.add(tv)
    try:
        session.commit()
    except IntegrityError:  # repeated element
        print("Element already in DB")
        session.rollback()


def string_to_upper_list(description):
    return list(map(lambda x: x.upper(), (description.split(" "))))


def process_ac(product):
    try:
        ac = AC()
        ac.brand = ""
        description_components = string_to_upper_list(product["description"])
        for component in description_components:
            if component in AC_COMMON_WORDS[product["company"]]["BRAND"]:
                ac.brand += component
                continue
            elif component[-1] in AC_COMMON_WORDS[product["company"]]["POWER"]:
                ac.power = component[:-1]
            elif component in AC_COMMON_WORDS[product["company"]]["POWER"]:
                ac.power = description_components[description_components.index(component)-1]
            elif component in AC_COMMON_WORDS[product["company"]]["SPLIT"]:
                ac.split = True
            elif component in AC_COMMON_WORDS[product["company"]]["HEAT"]:
                ac.heat = True
        if description_components[-3] not in AC_COMMON_WORDS[product["company"]]["POWER"] and product["company"] != "GARBARINO":
                ac.model = description_components[-3]
        else:
            ac.model = None
        ac.id = product["company"]+ac.brand+str(ac.model)+str(ac.power)
        ac.company = product["company"]
        ac.discount_price = product["discount_price"]
        ac.list_price = product["list_price"]
        ac.href = product["href"]
        save_tv_to_db(ac)
    except Exception as err:
        print(str(err))

