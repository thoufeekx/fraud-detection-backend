from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.admin import Admin
from passlib.hash import bcrypt
import os

def seed_admin_user():
    db: Session = SessionLocal()
    try:
        # Check if the admin user already exists
        existing_admin = db.query(Admin).filter(Admin.username == "admin").first()
        if existing_admin:
            print("Admin user already exists.")
            return

        # Fetch the password from environment variables or use a default
        password = os.getenv("ADMIN_PASSWORD", "default_password")
        password_hash = bcrypt.hash(password)

        # Create the admin user without the email field
        admin_user = Admin(
            username="admin",
            password_hash=password_hash,
        )
        db.add(admin_user)
        db.commit()
        print("Admin user seeded successfully.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin_user()
