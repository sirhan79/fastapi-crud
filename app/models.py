from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Boolean
from sqlalchemy.sql import func


class Customers(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    marital_status = Column(String(10), nullable=False)
    phone = Column(String(15), nullable=True)
    email = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True))

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    
