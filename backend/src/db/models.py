from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, TIMESTAMP, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=True)  # For local auth
    address_id = Column(Integer, nullable=True)
    activebool = Column(Boolean, default=True)
    active = Column(Integer, default=1)
    is_admin = Column(Boolean, default=False)
    oauth_provider = Column(String, nullable=True)  # google, github, etc
    oauth_id = Column(String, nullable=True)
    create_date = Column(Date, nullable=True)
    last_update = Column(TIMESTAMP(timezone=True), nullable=True)

class Order(Base):
    __tablename__ = "rental"
    rental_id = Column(Integer, primary_key=True, index=True)
    rental_date = Column(DateTime)
    inventory_id = Column(Integer)
    customer_id = Column(Integer)
    return_date = Column(DateTime)
    staff_id = Column(Integer)
    last_update = Column(DateTime)

class Payment(Base):
    __tablename__ = "payment"
    payment_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer)
    staff_id = Column(Integer)
    rental_id = Column(Integer)
    amount = Column(Numeric(10, 2))
    payment_date = Column(DateTime)

class Product(Base):
    __tablename__ = "film"
    film_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    release_year = Column(Integer)
    language_id = Column(Integer)
    rental_duration = Column(Integer)
    rental_rate = Column(String)
    length = Column(Integer)
    replacement_cost = Column(String)
    rating = Column(String)

# Alias for backward compatibility
Film = Product

