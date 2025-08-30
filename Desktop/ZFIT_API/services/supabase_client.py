from supabase import create_client

URL = 'https://sxazelezbxkqyjdghmyl.supabase.co'
KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN4YXplbGV6YnhrcXlqZGdobXlsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA5OTcyNDQsImV4cCI6MjA2NjU3MzI0NH0.ayQxxb5sSjXIEl7InS2GKWjVp5K8r-sL5hYgClnQcUg'
supabase = create_client(URL,KEY) #supabase connection

response = supabase.auth.sign_in_with_password(
    {
        "email": "andrew866799@gmail.com",
        "password": "Test123",
    }
)