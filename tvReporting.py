from models import TV
from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///products.db')
Base.metadata.create_all(engine)
Session = sessionmaker()
session = Session(bind=engine)

tvs = session.query(TV).all()


for tv in tvs:
    if tv.size == 32:
        print(tv.id)

