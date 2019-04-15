from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
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
    href = Column("href", String)

    def __init__(self, id, size=None, resolution=None, href=None):
        Product.__init__(self, id, model=None, brand=None, list_price=None, discount_price=None, company=None)
        self.size = size
        self.resolution = resolution
        self.href = href


class Heladera(Product):
    __tablename__ = 'Heladera'
    id = Column(String, ForeignKey("Product.id"), primary_key=True)
    no_frost = Column("no_frost", Boolean)
    capacity = Column("capacity", Integer)

    def __init__(self, id, capacity=None, no_frost=None, href=None):
        Product.__init__(self, id, model=None, brand=None, list_price=None, discount_price=None, company=None)
        self.capacity = capacity
        self.no_frost = no_frost
        self.href = href


class AC(Product):
    __tablename__ = 'AC'
    id = Column(String, ForeignKey("Product.id"), primary_key=True)
    power = Column("power", Integer)
    split = Column("split", Boolean)
    heat = Column("heat", Boolean)
    href = Column("href", String)

    def __init__(self, id, power=None, split=None, heat=None, href=None):
        Product.__init__(self, id, model=None, brand=None, list_price=None, discount_price=None, company=None)
        self.power = power
        self.split = split
        self.heat = heat
        self.href = href
