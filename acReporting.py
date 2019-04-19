from models import AC
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)
Session = sessionmaker()
session = Session(bind=engine)

acs = session.query(AC).all()

csvfile = open("./samples/acReport.csv", "w")
csvfile.write("DISCOUNT_PRICE" + "," + "LIST_PRICE" + "," + "POWER" + "," + "BRAND" + "," + "COMPANY" + "," + "LINK" + "\n")
for ac in session.query(AC).order_by(AC.power).order_by(AC.discount_price):
    try:
        csvfile.write(str(ac.discount_price) + "," + str(ac.list_price) + "," + str(ac.power) + "," + ac.brand + "," + str(ac.company) + "," + ac.href + "\n")
    except Exception as err:
        print(ac)

csvfile.close()
