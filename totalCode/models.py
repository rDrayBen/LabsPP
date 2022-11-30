import enum
import datetime
import sqlalchemy.orm
import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import alembic

sql_engine = create_engine('mysql://root:1234@localhost:3306/online_store', echo=False)
# Session = sessionmaker(bind=sql_engine)
# session = Session()
SessionFactory = sessionmaker(bind=sql_engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()
metadata = Base.metadata
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    login = Column(String(45), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    phone = Column(String(10), unique=True, nullable=False)
    email = Column(String(45), unique=True, nullable=False)
    address = Column(String(45), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

class Vendor(Base):
    __tablename__ = 'vendor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(45), nullable=False, unique=True)
    location = Column(String(45), nullable=False, )
    good = sqlalchemy.orm.relationship("Good", cascade='all, delete')

class Good_Category(Base):
    __tablename__ = 'good_category'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(45), nullable=False, unique=True)
    good = sqlalchemy.orm.relationship("Good", cascade='all, delete')


class Good(Base):
    __tablename__ = 'good'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vendor_id = Column(Integer, ForeignKey("vendor.id"), primary_key=True, nullable=False)
    category_id = Column(Integer, ForeignKey("good_category.id"), nullable=False)
    name = Column(String(45), nullable=False)
    description = Column(Text)
    cost = Column(Integer, nullable=False)
    num_in_stock = Column(Integer, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    is_reserved = Column(Boolean, nullable=False, default=0)

    order = sqlalchemy.orm.relationship("Order", backref="Good", uselist=False, cascade='all, delete')

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    good_id = Column(Integer, ForeignKey('good.id'), primary_key=True, nullable=False)
    buy_date = Column(DateTime, nullable=False, default=datetime.datetime.now())
    delivery = sqlalchemy.orm.relationship("Delivery", backref="Order", uselist=False, cascade='all, delete')

class Delivery(Base):
    __tablename__ = 'delivery'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True, nullable=False)
    type = Column(Enum('self pickup', 'courier'), nullable=False)
    to = Column(Integer, nullable=False)
