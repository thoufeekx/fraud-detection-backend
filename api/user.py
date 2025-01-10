from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User


# update to get current admin
from api.auth import get_current_admin

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()                     # Create a session local for each req
    try:
        yield db                            # yield the session so the routes can interact with the database
    finally:
        db.close()                          # close the session after the req is processed

@router.post("/users/")
def create_user(name: str, email: str, phone_number: str, db: Session = Depends(get_db)):  #route handler
    # Check if the email already exists
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a new user
    new_user = User(
        name=name,
        email=email,
        phone_number=phone_number,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    # Retrieve a user by their ID
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users", dependencies=[Depends(get_current_admin)])
def get_all_users(db: Session = Depends(get_db)):
    # Retrieve all users
    users = db.query(User).all()
    return users
