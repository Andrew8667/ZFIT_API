from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
URL = os.environ.get("URL")
KEY = os.environ.get("KEY")
supabase = create_client(URL,KEY) #supabase connection

