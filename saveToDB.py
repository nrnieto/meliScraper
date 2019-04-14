import csv
from models import *
from sqlalchemy.exc import IntegrityError

# TODO get brands from web


TV_COMMON_WORDS = {
                    "FRAVEGA": {
                        "NAME": ["TV", "SMART", "LED"],
                        "BRAND": ["SAMSUNG", "KEN", "BROWN", "PHILIPS", "LG", "SONY", "HITACHI", "NOBLEX", "PHILCO", "HISENSE", "RCA", "SANYO", "TELEFUNKEN", "TCL",
                                  "TOSHIBA", "JVC", "ADMIRAL", "SKYWORTH", "HYUNDAI"
                                  ],
                        "SIZE": ['24"', '32"', '42"', '43"', '49"', '50"', '55"', '65"', '75"'],
                        "RESOLUTION": ["4K", "FULLHD", "FULL", "HD", "ULTRA", "UHD"],
                    },
                    "GARBARINO": {
                        "NAME": ["TV", "SMART", "LED"],
                        "BRAND": ["SAMSUNG", "KEN", "BROWN", "PHILIPS", "LG", "SONY", "HITACHI", "NOBLEX", "PHILCO", "HISENSE", "RCA", "SANYO", "TELEFUNKEN", "TCL",
                                  "TOSHIBA", "JVC", "ADMIRAL", "SKYWORTH", "HYUNDAI"
                                  ],
                        "SIZE": ['24', '32', '42', '43', '49', '50', '55', '65', '75'],
                        "RESOLUTION": ["4K", "FULLHD", "FULL", "HD", "ULTRA", "UHD"]
                    }
}

engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)
Session = sessionmaker()
session = Session(bind=engine)


# TODO workaround
def process_hyundai_tv(product_components, product):
    tv = TV(id=product["company"] + product_components[-1] + product_components[-1].strip("HYLED-"+"UDH"),
            model=product_components[-1],
            brand=product_components[-2],
            size=product_components[-1].strip("HYLED-"+"UDH"),
            resolution=product_components[2],
            discount_price=product["list_price"],
            list_price=product["discount_price"],
            company=product["company"])  # TODO refactor save to db
    session.add(tv)
    session.commit()


def process_tv(product):
    # upper all words
    item = {}
    product_components = list(map(lambda x: x.upper(), (product["description"].split(" "))))
    for component in product_components:
        if component in TV_COMMON_WORDS[product["company"]]["BRAND"]:
            if component == "HYUNDAI":
                process_hyundai_tv(product_components, product)  # TODO workaround
                return
            try:
                item["brand"] += component
            except KeyError:
                item["brand"] = component
        elif component in TV_COMMON_WORDS[product["company"]]["SIZE"]:
            item["size"] = int(component.strip('"'))
        elif component in TV_COMMON_WORDS[product["company"]]["RESOLUTION"]:
            try:
                item["resolution"] += component
            except KeyError:
                item["resolution"] = component
    try:
        tv = TV(id=product["company"]+product_components[-1]+str(item["size"]),
                model=product_components[-1],
                brand=item["brand"],
                size=item["size"],
                resolution=item["resolution"],
                discount_price=product["discount_price"],
                list_price=product["list_price"],
                company=product["company"])
    except Exception:  # TODO hyundai
        return
    session.add(tv)
    try:
        session.commit()
    except IntegrityError:  # repeated element
        session.rollback()


def product_to_db(product):
    for component in product["description"].split(" "):
        if component.upper() in TV_COMMON_WORDS[product["company"]]["NAME"]:
            process_tv(product)
            break
    session.close()
