from sqlalchemy import Column, BigInteger, String, Integer, Numeric
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String(50), unique=True, nullable=True)

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    ticker = Column(String(20), nullable=False)    #
    target_price = Column(Numeric(10, 2), nullable=True)