import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from supabase import create_client
from app.core.auth import get_password_hash
from app.core.config import settings

def seed():
    # Use environment variables if set, otherwise from config
    url = os.environ.get("SUPABASE_URL") or settings.SUPABASE_URL
    key = os.environ.get("SUPABASE_KEY") or settings.SUPABASE_KEY
    
    if not url or not key:
        print("Missing SUPABASE_URL or SUPABASE_KEY")
        sys.exit(1)
        
    db = create_client(url, key)
    
    res = db.table("admins").select("*").eq("email", settings.ADMIN_EMAIL).execute()
    
    if not res.data:
        new_admin = {
            "email": settings.ADMIN_EMAIL,
            "hashed_password": get_password_hash(settings.ADMIN_INITIAL_PASSWORD),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        db.table("admins").insert(new_admin).execute()
        print(f"Admin {settings.ADMIN_EMAIL} created.")
    else:
        print("Admin already exists.")

if __name__ == "__main__":
    seed()
