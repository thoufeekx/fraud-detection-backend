from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.transactions import Transaction
from models.user import User
from datetime import datetime

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new transaction
@router.post("/transactions/")
def create_transaction(
    user_id: int,
    trans_date: datetime,
    cc_num: int,
    merchant: str,
    category: str,
    amount: float,
    city: str,
    state: str,
    zip_code: int,
    job: str,
    trans_num: str,
    merch_lat: float,
    merch_long: float,
    is_fraud: bool = False,
    db: Session = Depends(get_db),
):
    # Check if user exists
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create the transaction
    transaction = Transaction(
        user_id=user_id,
        trans_date=trans_date,
        cc_num=cc_num,
        merchant=merchant,
        category=category,
        amount=amount,
        city=city,
        state=state,
        zip_code=zip_code,
        job=job,
        trans_num=trans_num,
        merch_lat=merch_lat,
        merch_long=merch_long,
        is_fraud=is_fraud,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

# Fetch all transactions
@router.get("/transactions")
def get_all_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return transactions
