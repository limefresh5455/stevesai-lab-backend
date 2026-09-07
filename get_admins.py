import os
from dotenv import load_dotenv
load_dotenv("backend/.env")

from backend.app.database import SessionLocal
from backend.app.models.admin import Admin
import bcrypt

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

db = SessionLocal()
admins = db.query(Admin).all()
print(f"Total admins: {len(admins)}")
for admin in admins:
    print(f"Email: {admin.email}")
    print(f"Matches 'supersecret': {verify_password('supersecret', admin.hashed_password)}")
    print(f"Matches 'password123': {verify_password('password123', admin.hashed_password)}")
    print(f"Matches 'password': {verify_password('password', admin.hashed_password)}")
