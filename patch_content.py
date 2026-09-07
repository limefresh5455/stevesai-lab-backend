import re

with open("app/api/v1/content.py", "r") as f:
    content = f.read()

# 1. Add uuid import at the top
if "import uuid" not in content:
    content = content.replace("from fastapi import APIRouter", "import uuid\nfrom fastapi import APIRouter")

# 2. Fix update/delete endpoints which use id: int
def fix_update_delete(match):
    return match.group(0).replace("id: int", "id: str")

content = re.sub(r'def (?:update|delete)_[a-z_]+\(id: int,.*?\):', fix_update_delete, content)

# 3. Replace the body of update and delete functions that use identifier
for table, item_name in [("blog_posts", "Blog"), ("services", "Service")]:
    bad_body = f"""    if identifier.isdigit():
        res = db.table("{table}").select("*").eq("id", int(identifier)).execute()
    else:
        res = db.table("{table}").select("*").eq("slug", identifier).execute()"""
    
    good_body = f"""    res = db.table("{table}").select("*").eq("id", id).execute()"""
    content = content.replace(bad_body, good_body)

# 4. For get_admin_* functions, replace the isdigit check with a uuid check
for table in ["case_studies", "services", "blog_posts"]:
    bad_get = f"""    if identifier.isdigit():
        res = db.table("{table}").select("*").eq("id", int(identifier)).execute()
    else:
        res = db.table("{table}").select("*").eq("slug", identifier).execute()"""
        
    good_get = f"""    try:
        uuid.UUID(identifier)
        res = db.table("{table}").select("*").eq("id", identifier).execute()
    except ValueError:
        res = db.table("{table}").select("*").eq("slug", identifier).execute()"""
    
    content = content.replace(bad_get, good_get)

# 5. Fix pages endpoints
content = content.replace("def get_admin_page(id: int", "def get_admin_page(id: str")
content = content.replace("def update_page(id: int", "def update_page(id: str")
content = content.replace("def delete_page(id: int", "def delete_page(id: str")

with open("app/api/v1/content.py", "w") as f:
    f.write(content)
