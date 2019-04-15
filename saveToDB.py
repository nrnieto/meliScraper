from models import *
from sqlalchemy.exc import IntegrityError
from settings import TV_COMMON_WORDS, HELADERA_COMMON_WORDS

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
        tv.model = description_components[-1]
        tv.list_price = product["list_price"]
        tv.discount_price = product["discount_price"]
        tv.company = product["company"]
        tv.brand = tv_brand
        tv.resolution = tv_resolution
        save_tv_to_db(tv)
    except Exception:
        print("Can't save object")  # TODO hyundai product (1 element)


def product_to_db(product):
    for component in product["description"].split(" "):
        if component.upper() in TV_COMMON_WORDS[product["company"]]["NAME"]:
            process_tv(product)
            break
        #elif component.upper() in HELADERA_COMMON_WORDS[product["company"]["NAME"]]:
        #    pass
    session.close()


def save_tv_to_db(tv):
    session.add(tv)
    try:
        session.commit()
    except IntegrityError:  # repeated element
        print("Repeated element")
        session.rollback()


def string_to_upper_list(description):
    return list(map(lambda x: x.upper(), (description.split(" "))))


def process_heladera(product):
    pass
