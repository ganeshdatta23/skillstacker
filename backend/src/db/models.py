from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, TIMESTAMP, Numeric, Text, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True, index=True)
    store_id = Column(SmallInteger)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    email = Column(String(50), index=True)
    password_hash = Column(String, nullable=True)
    address_id = Column(SmallInteger)
    activebool = Column(Boolean, default=True)
    active = Column(Integer, default=1)
    is_admin = Column(Boolean, default=False)
    oauth_provider = Column(String, nullable=True)
    oauth_id = Column(String, nullable=True)
    create_date = Column(Date)
    last_update = Column(TIMESTAMP(timezone=True))

class Film(Base):
    __tablename__ = "film"
    film_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    release_year = Column(Integer)
    language_id = Column(SmallInteger)
    rental_duration = Column(SmallInteger, default=3)
    rental_rate = Column(Numeric(4, 2), default=4.99)
    length = Column(SmallInteger)
    replacement_cost = Column(Numeric(5, 2), default=19.99)
    rating = Column(String(10), default='G')
    special_features = Column(Text)
    last_update = Column(TIMESTAMP(timezone=True))

class Category(Base):
    __tablename__ = "category"
    category_id = Column(SmallInteger, primary_key=True, index=True)
    name = Column(String(25), nullable=False)
    last_update = Column(TIMESTAMP(timezone=True))

class Actor(Base):
    __tablename__ = "actor"
    actor_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False, index=True)
    last_update = Column(TIMESTAMP(timezone=True))

class Language(Base):
    __tablename__ = "language"
    language_id = Column(SmallInteger, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    last_update = Column(TIMESTAMP(timezone=True))

class Rental(Base):
    __tablename__ = "rental"
    rental_id = Column(Integer, primary_key=True, index=True)
    rental_date = Column(TIMESTAMP(timezone=True), nullable=False)
    inventory_id = Column(Integer, nullable=False)
    customer_id = Column(SmallInteger, nullable=False)
    return_date = Column(TIMESTAMP(timezone=True))
    staff_id = Column(SmallInteger, nullable=False)
    last_update = Column(TIMESTAMP(timezone=True))

class Payment(Base):
    __tablename__ = "payment"
    payment_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(SmallInteger, nullable=False)
    staff_id = Column(SmallInteger, nullable=False)
    rental_id = Column(Integer)
    amount = Column(Numeric(5, 2), nullable=False)
    payment_date = Column(TIMESTAMP(timezone=True), nullable=False)

class Inventory(Base):
    __tablename__ = "inventory"
    inventory_id = Column(Integer, primary_key=True, index=True)
    film_id = Column(SmallInteger, nullable=False)
    store_id = Column(SmallInteger, nullable=False)
    last_update = Column(TIMESTAMP(timezone=True))

# Legacy aliases for backward compatibility
Product = Film
Order = Rental