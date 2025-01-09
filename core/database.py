from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

# Added for alembic error
# IMP***  To avoid duplication of Base definitions across multiple files (user.py, admin.py, etc.), move the Base declaration to a shared module like core/database.py:
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()                               # central base for all models

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
