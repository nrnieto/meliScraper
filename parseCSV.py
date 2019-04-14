import csv
from models import *
from sqlalchemy.exc import IntegrityError

# TODO get brands from web
TV_COMMON_WORDS = {"NAME": ["TV", "SMART", "LED"],
                   "BRAND": ["SAMSUNG", "KEN", "BROWN", "PHILIPS", "LG", "SONY", "HITACHI", "NOBLEX", "PHILCO", "HISENSE", "RCA", "SANYO", "TELEFUNKEN", "TCL",
                             "TOSHIBA", "JVC", "ADMIRAL", "SKYWORTH", "HYUNDAI"],
                   "SIZE": ['24"', '32"', '42"', '43"', '49"', '50"', '55"', '65"', '75"'],
                   "RESOLUTION": ["4K", "FULLHD", "FULL", "HD", "ULTRA", "UHD"]}
HELADERA_COMMON_WORDS = {"NAME": ["HELADERA"],
                         "CAPACITY": ["LT", "LITROS", "LTS"]}
FREEZER_COMMON_WORDS = ["FREEZER"]
LAVARROPAS_COMMON_WORDS = ["LAVARROPAS"]
SECARROPAS_COMMON_WORDS = ["SECARROPAS"]
AC_COMMON_WORDS = ["AIRE", "ACONDICIONADO", "SPLIT", "VENTANA"]

tv_dict = {"FRAVEGA": {},
           "GARBARINO": {}}
HELADERA = dict()
FREEZER = dict()
LAVARROPAS = dict()
SECARROPAS = dict()
AC = dict()
UNKWOWN = []

engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)
Session = sessionmaker()
session = Session(bind=engine)


# TODO workaround
def process_hyunday_tv(product_components, value):
    tv = TV(id="FRAVEGA" + product_components[-1] + product_components[-1].strip("HYLED-"+"UDH"),
            model=product_components[-1],
            brand=product_components[-2],
            size=product_components[-1].strip("HYLED-"+"UDH"),
            resolution=product_components[2],
            discount_price=int(value[-1]),
            list_price=int(value[-2]),
            company="FRAVEGA")  # TODO refactor save to db
    session.add(tv)
    session.commit()


def process_fravega_tv(value):
    # upper all words
    item = {}
    product_components = list(map(lambda x: x.upper(), (value[0].split(" "))))
    for component in product_components:
        if component in TV_COMMON_WORDS["BRAND"]:
            if component == "HYUNDAI":
                process_hyunday_tv(product_components, value)  # TODO workaround
                return
            try:
                item["brand"] += component
            except KeyError:
                item["brand"] = component
        elif component in TV_COMMON_WORDS["SIZE"]:
            item["size"] = int(component.strip('"'))
        elif component in TV_COMMON_WORDS["RESOLUTION"]:
            try:
                item["resolution"] += component
            except KeyError:
                item["resolution"] = component
        else:
            item["list_price"] = int(value[-2])
            item["discount_price"] = int(value[-1])
    try:
        tv = TV(id="FRAVEGA"+product_components[-1]+str(item["size"]),
                model=product_components[-1],
                brand=item["brand"],
                size=item["size"],
                resolution=item["resolution"],
                discount_price=item["discount_price"],
                list_price=item["list_price"],
                company="FRAVEGA")
    except Exception:  # TODO hyundai
        return
    session.add(tv)
    try:
        session.commit()
    except IntegrityError:  # repeated element
        session.rollback()


with open("fravegaReport.csv", "r") as csvfile:
    products_file = csv.reader(csvfile, delimiter=",")
    for product in products_file:
        for word in product[0].split(" "):
            if word.upper() in TV_COMMON_WORDS["NAME"]:
                process_fravega_tv(product)
                break
    session.close()
