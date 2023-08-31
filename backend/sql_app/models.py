
from sqlalchemy import  Column, ForeignKey, Integer, Numeric, String, DateTime, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from sql_app.database import Base
import datetime

class User(Base):
    """
    User of the platform.
    """
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), index=True, nullable=False)
    is_real_agent = Column(Boolean, nullable=False)
    bookings = relationship('Booking', back_populates='user')
    

class Message(Base):
    __tablename__="message"
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    receiver = Column(Integer,ForeignKey('users.user_id'), nullable=True)
    sender = Column(Integer,ForeignKey('users.user_id'), nullable=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    content = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    


class Booking(Base):
    __tablename__="booking"
    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    flight_date = Column(DateTime,nullable=False)
    flight_icao = Column(String(50), nullable=False)
    flight_number = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="bookings")
    price = Column(Numeric(5,2), nullable= False)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)


class Feedback(Base):
    __tablename__="feedback"
    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    rating = Column(Integer,nullable=False, default=0)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
