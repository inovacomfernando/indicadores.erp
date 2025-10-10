"""
Supabase client configuration
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv(https://qweqxsxexjjunsnrlqpq.supabase.co)
SUPABASE_KEY = os.getenv(eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3ZXF4c3hleGpqdW5zbnJscXBxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAxMDI5NjEsImV4cCI6MjA3NTY3ODk2MX0.llyCziDRRFBHJhjGbGhicRzmnED77so8pIOJoIocQFo)

def get_supabase_client() -> Client:
    """
    Get Supabase client instance

    Returns:
        Client: Supabase client
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase credentials not found in environment variables")

    return create_client(SUPABASE_URL, SUPABASE_KEY)


