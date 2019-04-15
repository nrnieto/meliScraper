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

csvfile = open("acReport.csv", "w")


for ac in session.query(AC).order_by(AC.discount_price).order_by(AC.power):
    try:
        csvfile.write(str(ac.discount_price) + "," + str(ac.power) + "F" + "," + ac.brand + "," + str(ac.model) + "," + ac.company + "," + ac.href + "\n")
    except Exception as err:
        print(str(err))

csvfile.close()
