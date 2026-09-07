import os
import urllib.request
import json
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

req = urllib.request.Request(f"{url}/rest/v1/")
req.add_header("apikey", key)
req.add_header("Authorization", f"Bearer {key}")
req.add_header("Accept-Profile", "public")

with urllib.request.urlopen(req) as response:
    schema = json.loads(response.read().decode())

properties = schema["definitions"]["case_studies"]["properties"]
print("project_year type:", properties.get("project_year"))
