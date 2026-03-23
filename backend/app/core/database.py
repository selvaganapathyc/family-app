from functools import lru_cache
from supabase import create_client, Client
from app.core.config import settings


@lru_cache()
def get_supabase_client() -> Client:
    """Return a singleton Supabase client using the service role key."""
    client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return client


# Convenience singleton
supabase_client = get_supabase_client()
