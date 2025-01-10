from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.admin import Admin
from dotenv import load_dotenv
import os

from fastapi.security import OAuth2PasswordRequestForm
from .auth_utils import create_access_token, verify_password

# Load environment variables
load_dotenv()

# Secret key and algorithm from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for extracting the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

# Initialize router
router = APIRouter()

# # Utility functions
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

def get_current_admin(token: str = Depends(oauth2_scheme)):
    username = verify_access_token(token)
    return username

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Admin login endpoint
# @router.post("/admin/login")
# def admin_login(username: str, password: str, db: Session = Depends(get_db)):
#     admin = db.query(Admin).filter(Admin.username == username).first()
#     if not admin or not verify_password(password, admin.password_hash):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password",
#         )
#     access_token = create_access_token(data={"sub": admin.username})
#     return {"access_token": access_token, "token_type": "bearer"}

@router.post("/admin/login")
def admin_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == form_data.username).first()
    if not admin or not verify_password(form_data.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    access_token = create_access_token(data={"sub": admin.username})
    return {"access_token": access_token, "token_type": "bearer"}
