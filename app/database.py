from supabase import create_client, Client
from app.core.config import settings

def get_db() -> Client:
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    yield supabase
