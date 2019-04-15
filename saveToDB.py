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
        tv_brand = ""
        tv_resolution = ""
        description_components = string_to_upper_list(product["description"])
        for component in description_components:
            if component in TV_COMMON_WORDS[product["company"]]["BRAND"]:
                tv_brand += component
            elif component in TV_COMMON_WORDS[product["company"]]["SIZE"]:
                tv = TV(id=product["company"] + description_components[-1] + str(component.strip('"')))
                tv.size = int(component.strip('"'))
            elif component in TV_COMMON_WORDS[product["company"]]["RESOLUTION"]:
                tv_resolution += component
                if tv_resolution == "4KULTRAHD" or tv_resolution == "4KUHD":
                    tv_resolution = "4K"
        tv.model = description_components[-1]
        tv.list_price = product["list_price"]
        tv.discount_price = product["discount_price"]
        tv.company = product["company"]
        tv.brand = tv_brand
        tv.resolution = tv_resolution
        tv.href = product["href"]
        save_tv_to_db(tv)
    except Exception:
        print("Can't save object")  # TODO hyundai product (1 element)


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
        ac_brand = ""
        ac_power = ""
        ac_split = False
        ac_heat = False
        description_components = string_to_upper_list(product["description"])
        for component in description_components:
            if component in AC_COMMON_WORDS[product["company"]]["BRAND"]:
                ac_brand += component
                continue
            elif component[-1] in AC_COMMON_WORDS[product["company"]]["POWER"]:
                ac_power = component[:-1]
            elif component in AC_COMMON_WORDS[product["company"]]["POWER"]:
                ac_power = description_components[description_components.index(component)-1]
            elif component in AC_COMMON_WORDS[product["company"]]["SPLIT"]:
                ac_split = True
            elif component in AC_COMMON_WORDS[product["company"]]["HEAT"]:
                ac_heat = True
        if description_components[-3] not in AC_COMMON_WORDS[product["company"]]["POWER"] and product["company"] != "GARBARINO":
               ac_model = description_components[-3]
        else:
            ac_model = None
        ac = AC(id=product["company"]+ac_brand+str(ac_model)+str(ac_power))
        ac.company = product["company"]
        ac.discount_price = product["discount_price"]
        ac.list_price = product["list_price"]
        ac.power = ac_power
        ac.split = ac_split
        ac.heat = ac_heat
        ac.brand = ac_brand
        ac.model = ac_model
        ac.href = product["href"]
        save_tv_to_db(ac)
    except Exception as err:
        print(str(err))

