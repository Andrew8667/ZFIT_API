from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
URL = os.environ.get("URL")
KEY = os.environ.get("KEY")
supabase = create_client(URL,KEY) #supabase connection

response = supabase.auth.sign_in_with_password(
    {
        "email": "andrew866799@gmail.com",
        "password": "Test123",
    }
)