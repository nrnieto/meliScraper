from models import AC
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import grequests

Base = declarative_base()
engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)
Session = sessionmaker()
session = Session(bind=engine)

acs = session.query(AC).all()


urls = [ac.href for ac in session.query(AC)]
responses = grequests.map((grequests.get(u) for u in urls))
for r in responses:
    print(r)
