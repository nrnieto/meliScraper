from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()


class Product(Base):
    __tablename__ = 'Product'
    id = Column(String, primary_key=True)
    brand = Column("brand", String)
    model = Column("model", String(64))
    list_price = Column("list_price", Integer)
    discount_price = Column("discount_price", Integer)
    company = Column("company", String)

    def __init__(self, id, model, brand, list_price, discount_price, company):
        self.id = id
        self.brand = brand
        self.model = model
        self.list_price = list_price
        self.discount_price = discount_price
        self.company = company


class TV(Product):
    __tablename__ = 'TV'
    id = Column(String, ForeignKey("Product.id"),  primary_key=True)
    size = Column("size", Integer)
    resolution = Column("resolution", String)  # TODO choices

    def __init__(self, id, size=None, resolution=None):
        Product.__init__(self, id, model=None, brand=None, list_price=None, discount_price=None, company=None)
        self.size = size
        self.resolution = resolution


class Heladera(Product):
    __tablename__ = 'Heladera'
    id = Column(String, ForeignKey("Product.id"), primary_key=True)
    no_frost = Column("no_frost", Boolean)
    capacity = Column("capacity", Integer)

    def __init__(self, id, model, brand, capacity, no_frost, list_price, discount_price, company):
        Product.__init__(self, id, brand, model, list_price, discount_price, company)
        self.capacity = capacity
        self.no_frost = no_frost


class Freezer(Product):
    __tablename__ = 'Freezer'
    id = Column(String, ForeignKey("Product.id"), primary_key=True)
    capacity = Column("capacity", Integer)

    def __init__(self, id, model, brand, capacity, list_price, discount_price, company):
        Product.__init__(self, id, brand, model, list_price, discount_price, company)
        self.capacity = capacity


class Lavarropas(Product):
    __tablename__ = 'Lavarropas'
    id = Column(String, ForeignKey("Product.id"), primary_key=True)
    capacity = Column("capacity", Integer)
    frontal_load = Column("frontal_load", Boolean)
    rpm = Column("rpm", Integer)

    def __init__(self, model, brand, capacity, frontal_load, rpm, list_price, discount_price, company):
        Product.__init__(self, brand, model, list_price, discount_price, company)
        self.capacity = capacity
        self.frontal_load = frontal_load
        self.rpm = rpm


class Secarropas(Product):
    __tablename__ = 'Secarropas'
    id = Column(String, ForeignKey("Product.id"), primary_key=True)
    capacity = Column("capacity", Integer)
    by_heat = Column("by_heat", Boolean)
    rpm = Column("rpm", Integer)

    def __init__(self, model, brand, capacity, by_heat, rpm, list_price, discount_price, company):
        Product.__init__(self, brand, model, list_price, discount_price, company)
        self.capacity = capacity
        self.by_heat = by_heat
        self.rpm = rpm


class AC(Product):
    __tablename__ = 'AC'
    id = Column(String, ForeignKey("Product.id"), primary_key=True)
    power = Column("power", Integer)
    split = Column("split", Boolean)
    heat = Column("heat", Boolean)

    def __init__(self, model, brand, power, split, heat, list_price, discount_price, company):
        Product.__init__(self, brand, model, list_price, discount_price, company)
        self.brand = brand
        self.model = model
        self.power = power
        self.split = split
        self.heat = heat
        self.list_price = list_price
        self.discount_price = discount_price

