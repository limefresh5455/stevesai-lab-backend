import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.models.admin import Admin

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

engine = create_engine("sqlite:///backend/cms.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

admins = db.query(Admin).all()
print(f"Total admins in sqlite: {len(admins)}")
for admin in admins:
    print(f"Email: {admin.email}")
    print(f"Matches 'supersecret': {verify_password('supersecret', admin.hashed_password)}")
    print(f"Matches 'password123': {verify_password('password123', admin.hashed_password)}")
    print(f"Matches 'password': {verify_password('password', admin.hashed_password)}")
