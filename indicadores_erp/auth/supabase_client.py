"""
Supabase client configuration
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("VITE_SUPABASE_URL")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY")

def get_supabase_client() -> Client:
    """
    Get Supabase client instance

    Returns:
        Client: Supabase client
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase credentials not found in environment variables")

    return create_client(SUPABASE_URL, SUPABASE_KEY)
