from models import TV
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)
Session = sessionmaker()
session = Session(bind=engine)

tvs = session.query(TV).all()

csvfile = open("./samples/tvReport.csv", "w")
csvfile.write("DISCOUNT_PRICE" + "," + "LIST_PRICE" + "," + "SIZE" + "," + "BRAND" + "," + "RESOLUTION" + "," + "MODEL" + "," + "COMPANY" + "," + "LINK" + "\n")
for tv in session.query(TV).order_by(TV.size).order_by(TV.discount_price):
    csvfile.write(str(tv.discount_price) + "," + str(tv.list_price) + "," + str(tv.size) + "," + tv.brand + "," + tv.resolution + "," + tv.model + "," + tv.company + "," + tv.href + "\n")
csvfile.close()
