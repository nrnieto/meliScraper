from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine('sqlite:///garbarino.db')

# TODO inheritance!!!!!


class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True)
    brand = Column("brand", String)
    model = Column("name", String(64))
    list_price = Column("list_price", Float)
    discount_price = Column("discount_price", Float)
    company = Column("company", String)

    def __init__(self, model, brand, list_price, discount_price, company):
        self.brand = brand
        self.model = model
        self.list_price = list_price
        self.discount_price = discount_price
        self.company = company


class TV(Product):
    __tablename__ = 'TV'
    id = Column(Integer, ForeignKey("Product.id"),  primary_key=True)
    size = Column("size", Integer)
    resolution = Column("resolution", String)  # TODO choices

    def __init__(self, model, brand, size, resolution, list_price, discount_price, company):
        Product.__init__(self, brand, model, list_price, discount_price, company)
        self.size = size
        self.resolution = resolution


class Heladera(Product):
    __tablename__ = 'Heladera'
    id = Column(Integer, ForeignKey("Product.id"), primary_key=True)
    no_frost = Column("no_frost", Boolean)
    capacity = Column("capacity", Integer)

    def __init__(self, model, brand, capacity, no_frost, list_price, discount_price, company):
        Product.__init__(self, brand, model, list_price, discount_price, company)
        self.capacity = capacity
        self.no_frost = no_frost


class Freezer(Product):
    __tablename__ = 'Freezer'
    id = Column(Integer, ForeignKey("Product.id"), primary_key=True)
    capacity = Column("capacity", Integer)

    def __init__(self, model, brand, capacity, list_price, discount_price, company):
        Product.__init__(self, brand, model, list_price, discount_price, company)
        self.capacity = capacity


class Lavarropas(Product):
    __tablename__ = 'Lavarropas'
    id = Column(Integer, ForeignKey("Product.id"), primary_key=True)
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
    id = Column(Integer, ForeignKey("Product.id"), primary_key=True)
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
    id = Column(Integer, ForeignKey("Product.id"), primary_key=True)
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


Base.metadata.create_all(engine)

Session = sessionmaker()
session = Session(bind=engine)


tv = TV("UN50MU6100", "Samsung", 50, "4K", 16400, 15400, "fravega")
session.add(tv)

heladera = Heladera("HPK135B01", "Patrick", 277, False, 16400, 15400, "fravega")
session.add(heladera)

freezer = Freezer("L290", "Gafa", 285, 16400, 15400, "fravega")
session.add(freezer)

lavarropas = Lavarropas("ELAF08W", "Electrolux", 8, False, 1200, 16400, 15400, "fravega")
session.add(lavarropas)

secarropas = Secarropas("AQUATISAQC9BF7T1AG", "Ariston", 9, True, None, 16400, 15400, "fravega")
session.add(secarropas)

ac = AC("HIS35WCO", "Hisense", 3000, True, True, 16400, 15400, "fravega")
session.add(ac)


session.commit()
session.close()
