#file -> /backend/models/user.py

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Base = declarative_base()
from core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(15))
    registration_date = Column(Date, default=None)

    # Add this line for the relationship
    transactions = relationship("Transaction", back_populates="user")
