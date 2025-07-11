from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)

    children = relationship("Child", back_populates="parent")
    bookings = relationship("Booking", back_populates="user")

class Child(Base):
    __tablename__ = "children"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    parent = relationship("User", back_populates="children")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    service = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    confirmed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="bookings")

class Consent(Base):
    __tablename__ = "consents"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    agreed_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
