from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Boolean, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    trans_date = Column(TIMESTAMP, nullable=False)
    cc_num = Column(BigInteger, nullable=False)
    merchant = Column(String(100))
    category = Column(String(50))
    amount = Column(DECIMAL(10, 2), nullable=False)
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(Integer)
    job = Column(String(100))
    trans_num = Column(String(50))
    merch_lat = Column(DECIMAL(10, 6))
    merch_long = Column(DECIMAL(10, 6))
    is_fraud = Column(Boolean, default=False)

    # Define relationships (optional)
    user = relationship("User", back_populates="transactions")
