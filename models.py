from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
import uuid
import time


class Product(Base):
    __tablename__ = 'Product'
    id = Column(String, primary_key=True)
    brand = Column("brand", String)
    model = Column("model", String(64))
    list_price = Column("list_price", Integer)
    discount_price = Column("discount_price", Integer)
    company = Column("company", String)
    timestamp = Column("timestamp", Integer)

    def __init__(self, id=None, model=None, brand=None, list_price=None, discount_price=None, company=None):
        self.id = id
        self.brand = brand
        self.model = model
        self.list_price = list_price
        self.discount_price = discount_price
        self.company = company
        self.timestamp = int(time.time())


class TV(Product):
    __tablename__ = 'TV'
    id = Column(String, ForeignKey("Product.id"),  primary_key=True)
    size = Column("size", Integer)
    resolution = Column("resolution", String)  # TODO choices
    href = Column("href", String)

    def __init__(self, size=None, resolution=None, href=None):
        Product.__init__(self, id=None, model=None, brand=None, list_price=None, discount_price=None, company=None)
        self.size = size
        self.resolution = resolution
        self.href = href


class AC(Product):
    __tablename__ = 'AC'
    id = Column(String, ForeignKey("Product.id"), primary_key=True)
    power = Column("power", Integer)
    heat = Column("heat", Boolean)
    href = Column("href", String)

    def __init__(self, power=None, heat=False, href=None):
        Product.__init__(self, id=None, model=None, brand=None, list_price=None, discount_price=None, company=None)
        self.power = power
        self.heat = heat
        self.href = href
