from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine('sqlite:///garbarino.db')


class TV(Base):
    __tablename__ = 'TV'
    id = Column(Integer, primary_key=True)
    model = Column("name", String(64))
    size = Column("size", Integer)
    resolution = Column("resolution", String)  # TODO choices
    brand = Column("brand", String)
    list_price = Column("list_price", Float)
    discount_price = Column("discount_price", Float)

    def __init__(self, model, size, resolution, brand, list_price, discount_price,):
        self.model = model
        self.size = size
        self.resolution = resolution
        self.brand = brand
        self.list_price = list_price
        self.discount_price = discount_price


Base.metadata.create_all(engine)

Session = sessionmaker()
session = Session(bind=engine)

tv = TV("UN50MU6100", 50, "4K", "Samsung", 16400, 15400)
session.add(tv)

session.commit()
session.close()
